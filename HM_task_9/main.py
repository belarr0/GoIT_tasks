def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Помилка: {str(e)}"

    return wrapper


class ContactBot:
    def __init__(self):
        self.contacts = {}

    @input_error
    def hello(self):
        return "How can I help you?"

    @input_error
    def add_contact(self, command):
        _, name, phone = command.split()
        self.contacts[name] = phone
        return f"Contact {name} added with phone {phone}"

    @input_error
    def change_contact(self, command):
        _, name, phone = command.split()
        if name in self.contacts:
            self.contacts[name] = phone
            return f"Phone number for {name} changed to {phone}"
        else:
            raise KeyError(f"Contact {name} not found")

    @input_error
    def phone_number(self, command):
        _, name = command.split()
        if name in self.contacts:
            return f"The phone number for {name} is {self.contacts[name]}"
        else:
            raise KeyError(f"Contact {name} not found")

    @input_error
    def show_all_contacts(self):
        if not self.contacts:
            return "No contacts available."
        result = "All contacts:\n"
        for name, phone in self.contacts.items():
            result += f"{name}: {phone}\n"
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
