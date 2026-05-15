import random, string
print("Welcome to the Password Generator!")
tot = int(input("Enter the total number of characters in the password (Must be >= 8): "))
if tot < 8:
    print("Too low")
else:
    lowerLetters = string.ascii_lowercase
    upperLetters = string.ascii_uppercase
    Digits = string.digits
    Symbols = "@#$"
    passwordList = [
        random.choice(lowerLetters),
        random.choice(upperLetters),
        random.choice(Digits),
        random.choice(Symbols)
    ]
    allCombined = lowerLetters + upperLetters + Digits + Symbols
    remaining_length = tot - len(passwordList)
    passwordList += random.choices(allCombined, k=remaining_length)
    random.shuffle(passwordList)
    password = "".join(passwordList)

    print("-" * 30)
    print(f"Generated Password: {password}")
    print("-" * 30)