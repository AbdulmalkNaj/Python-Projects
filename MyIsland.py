print(""" _;~)                  (~;_
(   |                  |   )
 ~', ',    ,''~'',   ,' ,'~
     ', ','       ',' ,'
       ',: {'} {'} :,'
         ;   /^\\   ;
          ~\\  ~  /~
        ,' ,~~~~~, ',
      ,' ,' ;~~~; ', ',
    ,' ,'    '''    ', ',
  (~  ;               ;  ~)
   -;_)               (_;-""")
print("Welcome to my island!\nThere are two doors in front of you. a red door 🚪 and a blue door 🚪")
door = input("Which door do you want to open? ").lower()
if door == "blue":
    print("Oops! You chose the crocodile door.\nGame over!🐊🐊🐊")
elif door == "red":
    print("Great! now you entered a room.\nyou found three boxes: white 🎁, black🎁, green🎁")
    box = input("Which box do you want to open? ").lower()
    if box == "white":
        print("Oops! You opened a box filled with snakes🐍🐍🐍")
    elif box == "green":
        print("Congratulations! You found the treasure! 🪙🪙🪙")
    elif box == "black":
        print("Oops! You opened a box filled with spiders🕸️🕸️🕸️")
    else:
        print("Invalid choice! 🤷‍♂️")
else:
    print("Invalid choice! 🤷‍♂️")
