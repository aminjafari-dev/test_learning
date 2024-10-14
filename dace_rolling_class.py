import random

class Dice:
    def roll(self):
        first_number = random.randint(1,6)
        second_number = random.randint(1,6)
        print(f'({first_number}, {second_number})')


dice = Dice()

dice.roll()