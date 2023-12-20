import os

exit_words = ["good bye", "close", "exit", "bye"]

class NoteManager:
    def __init__(self, exit_words=None):
        self.notes = {}
        self.exit_words = exit_words or []
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.data_file_path = os.path.join(current_directory, "data.txt")

    def add_note(self, name, title):
        self.notes[name] = title
        self.save_notes_to_file()
        return f"Note added: {name}, {title}"

    def edit_note(self, name, new_title):
        if name in self.notes:
            self.notes[name] = new_title
            self.save_notes_to_file()
            return f"Note for {name} edited: {new_title}"
        else:
            return f"Note for {name} not found."

    def delete_note(self, name):
        if name in self.notes:
            del self.notes[name]
            self.save_notes_to_file()
            return f"Note for {name} deleted."
        else:
            return f"Note for {name} not found."

    def save_notes_to_file(self):
        with open(self.data_file_path, "w") as file:
            for name, title in self.notes.items():
                file.write(f"{name}, {title}\n")

    def load_notes_from_file(self):
        try:
            with open(self.data_file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    name, title = line.strip().split(', ')
                    self.notes[name] = title
        except FileNotFoundError:
            pass

    def get_note_by_name(self, name):
        if name in self.notes:
            return f"Note for {name}: {self.notes[name]}"
        else:
            return f"Note for {name} not found."

    def handle_command(self, command):
        if command.lower() == 'hello':
            return 'How can I help you?'
        elif command.lower() in self.exit_words:
            return "Good bye!"
        elif command.lower().startswith('add'):
            first_split = command.split(', ')
            note_name = first_split[0].split()[1]
            title = first_split[1]
            return self.add_note(note_name, title)
        elif command.lower().startswith('edit'):
            edit_split = command.split(', ')
            note_name = edit_split[0].split()[1]
            new_title = edit_split[1]
            return self.edit_note(note_name, new_title)
        elif command.lower().startswith('delete'):
            name_to_delete = command.split(' ')[1]
            return self.delete_note(name_to_delete)
        elif command.lower().startswith('get'):
            name_to_get = command.split(' ')[1]
            return self.get_note_by_name(name_to_get)
        else:
            return "Unknown command. Please try again."

def main():
    bot = NoteManager(exit_words)
    bot.load_notes_from_file()

    while True:
        user_input = input("Enter a command: ")

        if user_input.lower() in exit_words:
            bot.save_notes_to_file()
            print(bot.handle_command(user_input))
            break

        response = bot.handle_command(user_input)
        print(response)

if __name__ == "__main__":
    main()
