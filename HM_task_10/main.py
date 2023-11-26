from collections import UserDict

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    def validate_phone(self, value):
        # Ваша логіка валідації номера телефону. Приклад: довжина 10 цифр.
        return len(value) == 10 and value.isdigit()

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, index):
        del self.phones[index]

    def edit_phone(self, index, new_phone):
        self.phones[index].value = new_phone

    def find_phone(self, phone):
        for index, existing_phone in enumerate(self.phones):
            if existing_phone.value == phone:
                return index
        return -1

    def __str__(self):
        phones_str = ", ".join(str(phone) for phone in self.phones)
        return f"Name: {self.name}, Phones: {phones_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def search_records(self, **kwargs):
        result = []
        for record in self.values():
            match = all(getattr(record, key).value == value for key, value in kwargs.items())
            if match:
                result.append(record)
        return result

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Помилка: {str(e)}"

    return wrapper

class ContactBot:
    def __init__(self):
        self.contacts = AddressBook()

    @input_error
    def hello(self):
        return "How can I help you?"

    @input_error
    def add_contact(self, command):
        _, name, phone = command.split()
        if name in self.contacts:
            record = self.contacts[name]
            record.add_phone(phone)
        else:
            record = Record(name)
            record.add_phone(phone)
            self.contacts.add_record(record)
        return f"Contact {name} added with phone {phone}"

    @input_error
    def change_contact(self, command):
        _, name, old_phone, new_phone = command.split()
        record = self.contacts[name]
        index = record.find_phone(old_phone)
        if index != -1:
            record.edit_phone(index, new_phone)
            return f"Phone number for {name} changed from {old_phone} to {new_phone}"
        else:
            raise ValueError(f"Phone number {old_phone} not found for {name}")

    @input_error
    def phone_number(self, command):
        _, name = command.split()
        record = self.contacts[name]
        return f"The phone numbers for {name} are {', '.join(str(phone) for phone in record.phones)}"

    @input_error
    def show_all_contacts(self):
        if not self.contacts:
            return "No contacts available."
        result = "All contacts:\n"
        for record in self.contacts.values():
            result += str(record) + "\n"
        return result.strip()

    def good_bye(self):
        return "Good bye!"

    def handle_command(self, command):
        if command.lower() == "hello":
            return self.hello()
        elif command.lower().startswith("add"):
            return self.add_contact(command)
        elif command.lower().startswith("change"):
            return self.change_contact(command)
        elif command.lower().startswith("phone"):
            return self.phone_number(command)
        elif command.lower() == "show all":
            return self.show_all_contacts()
        elif command.lower() in ["good bye", "close", "exit"]:
            return self.good_bye()
        else:
            return "Unknown command. Please try again."

def main():
    bot = ContactBot()

    while True:
        user_input = input("Enter a command: ")

        if user_input.lower() in ["good bye", "close", "exit"]:
            print(bot.handle_command(user_input))
            break

        response = bot.handle_command(user_input)
        print(response)

if __name__ == "__main__":
    main()
