import random
import os
import sys


def game():
    while True:
        try:
            number_of_dices = int(input('Please select how many dices do you want to use: '))
        except ValueError:
            print('Please enter a number')
            continue
        break

    while True:
        try:
            s = int(input('How many sides on your dice? '))
        except ValueError:
            print('Number of sides must be a number.')
            continue
        break

    def dice_roll(number_of_dices):
        _rolls = []
        for i in range(number_of_dices):
            dice_roll = random.randint(1, s)
            _rolls.append(dice_roll)
            print(dice_roll, end=' ')
        return _rolls


    rolls = dice_roll(number_of_dices)
    print('\nTotal number is: ',sum(rolls))

while True:
    game()
    restart = input('Do you want to restart? Y/N ')
    if restart == 'N' or 'n':
        continue
    elif restart == 'Y' or 'y':
        os.execl(sys.executable, ['Dice Rolling Simulator'], *sys.argv)
