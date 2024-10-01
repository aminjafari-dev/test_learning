import random

##Loop
while True:
        # Ask Question and wait for input user
    dice = input('Roll the dice? (Y/N): ').lower()
        # If user Press y we have to generate 2 random number
    if dice == 'y':
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)
        print(f'({die1}, {die2})')
    elif dice == 'n':
        print("Thanks for playing this game")
        break

    else:
        print('Invalid Choice!!')
    # show them to the user
    # If press N we should exite the game