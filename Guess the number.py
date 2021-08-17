import random

print('Do you want to guess the number or do you want me to guess?')
choice = input('Choose H for Human if you want to guess or C for Computer if you want computer to guess. ')

if choice.upper() == 'H':
    guess = 0
    number = random.randint(1, 100)
    attempts = 0

    print('Guess the number.')
    while guess != number:
        guess = int(input('Is it.. '))
        if guess == number:
            print('Got it.')
        elif guess < number:
            attempts += 1
            print('Too low.')
        else:
            attempts += 1
            print('Too high.')

    print('Took you %s attempts to get it right.' % (attempts))
elif choice.upper() == 'C':
    secret_number = int(input('OK, pick a number between 1 and 100 and let Computer guess it. '))
    attempts = 0
    computer_choice = random.randint(1, 100)
    higher = 101
    lower = 0
    
    while computer_choice != secret_number:
        if computer_choice > secret_number:
            print('Computer is guessing it could be : %d' % (computer_choice))
            higher = computer_choice
            computer_choice = random.randint(lower + 1, higher - 1)
        else:
            print('Computer is guessing it could be : %d' % (computer_choice))
            lower = computer_choice
            computer_choice = random.randint(lower + 1, higher - 1)
        
        attempts += 1
    print('Computer guessed your number in %d attempts.' % (attempts))
    
else:
    print('You need to choose Human or Computer.')
