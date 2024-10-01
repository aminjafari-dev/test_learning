
import random

choices = ('r', 'p', 's')
emojis = {
    'r' : '🪨',
    'p' : '📄',
    's' : '✂️',
}

while True:

    user_choice = input('Rock, paper, or scissors? (r/p/s): ')
    if user_choice not in choices:
        print('Please Enter a valid number')
        continue

    else:
        computer_choice = random.choice(choices)

        print(f'Your choice: {emojis[user_choice]}')
        print(f'Computer choice: {emojis[computer_choice]}')

        if user_choice == computer_choice:
            print('Tie!')
        elif (
        (user_choice == 'r' and computer_choice == 's') or 
        (user_choice == "p" and computer_choice == 'r') or 
        (user_choice == 's' and computer_choice == 'p')):

            print('You Win')
        
        else:
            print('You Loose')
            

# Ask the users to make a choice

# generate Random for Computer

# 