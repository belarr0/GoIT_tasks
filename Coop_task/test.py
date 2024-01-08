# text = 'add Leha, loh'
# first_split = text.split(', ')
# first_word = first_split[0].split()[1]
# second_word = first_split[1]
#
# print(first_split, '\n', first_word, '\n', second_word)

# class Adres:
#     def out(self):
#         return "out def"
#
# class sec_Adres(Adres):
#     def sec_out(self):
#         return self.out()
#
# def main():
#     instance = sec_Adres()
#     result = instance.sec_out()
#     print(result)
#
# if __name__ == "__main__":
#     main()


# ANSI escape codes for text colors
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

def print_colored(text, color):
    print(color + text)

# Example usage
print_colored("This is red text", Colors.RED)
print_colored("This is green text", Colors.GREEN)
print_colored("This is blue text", Colors.BLUE)




