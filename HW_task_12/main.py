from collections import UserDict
from datetime import datetime, timedelta
import pickle

class Field:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    @staticmethod
    def validate_phone(value):
        return len(value) == 10 and value.isdigit()

    def __init__(self, value):
        value = self.validate_phone(value)
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value=None):
        self.value = self.validate_birthday(value)

    def validate_birthday(self, value):
        if value is not None:
            try:
                datetime.strptime(value, "%Y-%m-%d")
                return value
            except ValueError:
                raise ValueError("Invalid birthday format. Please use YYYY-MM-DD.")
        return value

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, index):
        del self.phones[index]

    def edit_phone(self, index, new_phone):
        self.phones[index].value = Phone.validate_phone(new_phone)

    def find_phone(self, phone):
        for index, existing_phone in enumerate(self.phones):
            if existing_phone.value == phone:
                return index
        return -1

    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.now().date()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()
            return (next_birthday - today).days
        return None

    def validate_phone(self, value):
        if not Phone.validate_phone(value):
            raise ValueError("Invalid phone number format")
        return value

    def __str__(self):
        phones_str = ", ".join(str(phone) for phone in self.phones)
        return f"Name: {self.name}, Birthday: {self.birthday}, Phones: {phones_str}"

class AddressBookIterator:
    def __init__(self, records, chunk_size):
        self.records = list(records.values())
        self.chunk_size = chunk_size
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index >= len(self.records):
            raise StopIteration

        chunk = self.records[self.current_index:self.current_index + self.chunk_size]
        self.current_index += self.chunk_size
        return chunk

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record):
        self.data[record.name.value] = record

    def search_records(self, **kwargs):
        result = []
        for record in self.values():
            match = all(getattr(record, key).value == value for key, value in kwargs.items())
            if match:
                result.append(record)
        return result

    def iterator(self, chunk_size=5):
        return AddressBookIterator(self.data, chunk_size)

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Помилка: {str(e)}"

    return wrapper

    def save_to_file(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                self.data = pickle.load(file)
        except (FileNotFoundError, pickle.UnpicklingError):
            self.data = {}

    def search_contacts(self, search_str):
        result = []
        for record in self.values():
            if (
                    search_str.lower() in record.name.value.lower()
                    or any(search_str in phone.value for phone in record.phones)
            ):
                result.append(record)
        return result


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
    def save_to_file(self, command):
        _, file_path = command.split()
        self.contacts.save_to_file(file_path)
        return f"Address book saved to {file_path}"

    @input_error
    def load_from_file(self, command):
        _, file_path = command.split()
        self.contacts.load_from_file(file_path)
        return f"Address book loaded from {file_path}"

    @input_error
    def search_contacts(self, command):
        _, search_str = command.split(maxsplit=1)
        found_contacts = self.contacts.search_contacts(search_str)
        if found_contacts:
            result = "Found contacts:\n"
            for record in found_contacts:
                result += str(record) + "\n"
            return result.strip()
        else:
            return "No matching contacts found."

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
