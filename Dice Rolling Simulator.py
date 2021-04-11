import random

number_of_dices = int(input('Please select how many dices do you want to use: '))

rolls = []
def dice_roll(number_of_dices):
    for i in range(number_of_dices):
        dice_roll = random.randint(1, 6)
        rolls.append(dice_roll)
        print(dice_roll, end=' ')

print(dice_roll(number_of_dices))
print('\nTotal number is: ',sum(rolls))
