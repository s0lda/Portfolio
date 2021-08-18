import random

def eight_ball():
    answers = ['It is certain.', 'It is decidedly so.', 'Yes.', 'Reply hazy try again.', 'Ask again later.', 
    'Concentrate and ask again.', 'My reply is no.', 'Outlook not so good.']


    print('You can ask multiple questions. To exit type exit.')
    valid = False
    while valid == False:
        try:
            print('What is your question?')
            question = input('>> ')
            if question.lower() == 'exit':
                valid = True
                print('Bye Bye.')
            else:
                print(answers[random.randint(0, 7)])
        finally:
            pass

if __name__ == '__main__':
    eight_ball()
