

import random

random_number = random.randint(1, 100)
while True:
    try:
        user_number = int(input('Guess the number between 1 to 100: '))
        if user_number > random_number:
            print('High!')
        elif user_number < random_number:
            print('Low!')
        else:
            print('Cangoratulations! you got it')
            break

    except ValueError:
        print('Please enter a valid number')



