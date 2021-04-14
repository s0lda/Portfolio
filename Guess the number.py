import random
guess = random.randint(0, 100)
number = random.randint(0, 100)
print('Guess the number.')
while guess != number:
    guess = int(input('Is it.. '))
    if guess == number:
        print('Thats\'s right.')
    elif guess < number:
        print('It\'s bigger.')
    elif guess > number:
        print('It\'s smaller.')
