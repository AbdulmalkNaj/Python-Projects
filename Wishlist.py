owned =[]
ownedbook = input("Enter the name of a book you own: ").lower()
owned.append(ownedbook)
anotherOwnedBook = input("Enter the name of another book you own (or press 'Enter' to skip): ").lower()
if anotherOwnedBook:
    owned.append(anotherOwnedBook)
    print(f"Your Library: {owned}")
    print()
else:
    print(f"Your Library: {owned}")
    print()

wish = []
wishBook = input("Enter the name of a book you wish to have in the future: ").lower()
wish.append(wishBook)
anotherWishBook = input("Enter name of another book you wish to have (or press 'Enter' to skip): ").lower()
if anotherWishBook:
    wish.append(anotherWishBook)
    print(f"Your Wishlist: {wish}")
    print()
else:
    print(f"Your Wishlist: {wish}")
    print()

acquireBook = input("Enter the name of a book from your wishlist that you've acquired (or press 'Enter' to skip): ").lower()
if acquireBook:
    wish.remove(acquireBook)
    owned.append(acquireBook)
    print(f"Updated Library: {owned}")
    print(f"Updated Wishlist: {wish}")
    print()
else:
    print(f"Updated Library: {owned}")
    print(f"Updated Wishlist: {wish}")
    print()

donate = input("Enter the name of a book from your library you wish to donate (or press 'Enter' to skip): ").lower()
if donate:
    owned.remove(donate)
    print(f"Final Library after Donations: {owned}")
else:
    print(f"Final Library after Donations: {owned}")