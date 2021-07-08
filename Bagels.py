import random

num_digits = 3
max_guess = 10

def get_secret_number():
    numbers = list(range(10))
    random.shuffle(numbers)
    secret_num = ''
    for i in range(num_digits):
        secret_num += str(numbers[i])
    return secret_num

def get_clues(guess, secret_num):
    if guess == secret_num:
        return 'You got it'

    clues = []
    for i in range(len(guess)):
        if guess[i] == secret_num[i]:
            clues.append('Fermi')
        elif guess[i] in secret_num:
            clues.append('Pico')
    if len(clues) == 0:
        return 'Bagels'

    clues.sort()
    return ' '.join(clues)

def is_only_digits(num):
    if num == '':
        return False

    for i in num:
        if i not in ' 0 1 2 3 4 5 6 7 8 9'.split():
            return False
    return True

print('The clues I give are...')
print(' When I say:    That means:')
print(' Bagels         None of the digits is correct.')
print(' Pico           One digit is correct but in the wrong position.')
print(' Fermi          One digit is correct and in the right position.')

while True:
    secret_num = get_secret_number()
    print('I have thought you a number. You have %s guesses to it.' %(max_guess))
    
    guess_taken = 1
    while guess_taken <= max_guess:
        guess = ''
        while len(guess) != num_digits or not is_only_digits:
            print('Guess #%s: ' % (guess_taken))
            guess = input()
        
        print(get_clues(guess, secret_num))
        guess_taken += 1

        if guess == secret_num:
            break
        if guess_taken > max_guess:
            print('You ran out of guesses. The answer was %s.' % (secret_num))

    print('Do you want to play again? y or n')
    if not input().lower().startswith('y'):
        break

