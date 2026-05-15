import random
HANGMANPICS = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========''']
words = [
    "apple", "beach", "brain", "bread", "brush", "chair", "chest", "chord", "click", "clock",
    "cloud", "dance", "diary", "drink", "earth", "feast", "field", "fruit", "glass", "grape",
    "green", "ground", "guard", "heart", "house", "juice", "light", "lemon", "money", "music",
    "night", "ocean", "party", "piano", "pilot", "plane", "phone", "pizza", "plant", "radio",
    "river", "robot", "shirt", "shoes", "smile", "snake", "space", "spoon", "storm", "table",
    "tiger", "train", "truck", "voice", "water", "watch", "whale", "world", "write", "zebra",
    "actor", "angry", "animal", "answer", "apple", "area", "army", "baby", "back", "ball",
    "bank", "bath", "bed", "beer", "bird", "blood", "boat", "body", "bone", "book",
    "box", "boy", "building", "burn", "bus", "cake", "call", "camp", "car", "card",
    "cat", "center", "city", "clean", "coat", "cold", "cook", "cool", "corn", "corner",
    "cup", "cut", "dark", "day", "desk", "dog", "door", "dream", "dress", "dry",
    "duck", "dust", "ear", "east", "eat", "egg", "eye", "face", "fall", "farm",
    "fast", "father", "fire", "fish", "five", "flag", "floor", "fly", "food", "foot",
    "forest", "fork", "game", "garden", "girl", "goat", "gold", "good", "gray", "hair",
    "hand", "hat", "head", "help", "hill", "home", "hope", "horse", "hotel", "ice",
    "iron", "island", "jail", "jelly", "jump", "key", "king", "knee", "knife", "lake",
    "lamp", "land", "leaf", "leg", "library", "line", "lion", "lip", "list", "love",
    "map", "meat", "milk", "mind", "moon", "mother", "mouth", "move", "name", "neck",
    "nest", "net", "news", "nose", "note", "nurse", "oil", "orange", "page", "pan",
    "paper", "park", "pen", "pencil", "person", "picture", "pig", "pin", "pink", "pipe",
    "plate", "play", "pool", "pot", "queen", "quick", "rain", "read", "rice", "ride",
    "ring", "road", "rock", "roof", "room", "root", "rope", "rose", "salt", "sand",
    "school", "seat", "seed", "sheep", "ship", "shoe", "shop", "show", "side", "silk",
    "silver", "sing", "sister", "size", "skin", "sky", "sleep", "slow", "snow", "soap",
    "sock", "soft", "son", "song", "soup", "star", "step", "stick", "stone", "stop",
    "sugar", "sun", "swim", "tall", "tea", "team", "teeth", "tent", "test", "time",
    "top", "town", "tree", "unit", "user", "view", "wall", "war", "wash", "way",
    "west", "wheel", "window", "wine", "wing", "winter", "wire", "wood", "yard", "year"
]

random_word = random.choice(words)

display = ["_"] * len(random_word)
print(" ".join(display))
guessedLet = []
print(HANGMANPICS[0])
tries = 6

while "_" in display and tries > 0:
    print("#" * 10)
    guessed = input("Please guess a letter: ").lower()

    if guessed in guessedLet:
        print("You already guessed that letter")
        print(f"You have {tries} more tries left")
        continue

    guessedLet.append(guessed)

    if guessed not in random_word:
        tries -= 1
        print(HANGMANPICS[6-tries])
    else:
        for position in range(len(random_word)):
            if guessed == random_word[position]:
                display[position] = guessed

    print(display)
    print(f"You have {tries} more tries left")

if tries == 0:
    print(HANGMANPICS[-1])
    print("""
           ********
           YOU LOSE!!
           ********
    """)
else:
    print("""
           ********
           YOU WIN
           ********
    """)