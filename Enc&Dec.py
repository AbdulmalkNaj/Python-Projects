import string
def encryption(word, key):
    alphabet = string.ascii_lowercase

    encrypted_message = ""

    for letter in word:
        if letter.lower() in alphabet:
            original_position = alphabet.index(letter.lower())
            new_position = (original_position + key) % len(alphabet)
            encrypted_letter = alphabet[new_position]

            if letter.isupper():
                encrypted_letter = encrypted_letter.upper()

            encrypted_message += encrypted_letter
        else:
            encrypted_message += letter

    print(f"Here is the encrypted message: {encrypted_message}")

def decryption(word, key):
    alphabet = string.ascii_lowercase

    encrypted_message = ""

    for letter in word:
        if letter.lower() in alphabet:
            original_position = alphabet.index(letter.lower())
            new_position = (original_position - key) % len(alphabet)
            encrypted_letter = alphabet[new_position]

            if letter.isupper():
                encrypted_letter = encrypted_letter.upper()

            encrypted_message += encrypted_letter
        else:
            encrypted_message += letter

    print(f"Here is the original message: {encrypted_message}")
choice = int(input("""
1. Encrypt
2. Decrypt
"""))
if choice == 1:
    message = input("Enter a message: ")
    key = int(input("Enter a key: "))
    encryption(message, key)
elif choice == 2:
    message = input("Enter a message: ")
    key = int(input("Enter a key: "))
    decryption(message, key)
else:
    print("Wrong input. Try again.")