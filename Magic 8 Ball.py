import random
answers = ['It is certain.', 'It is decidedly so.', 'Yes.', 'Reply hazy try again.', 'Ask again later.', 
'Concentrate and ask again.', 'My reply is no.', 'Outlook not so good.']

r = random.randint(0, 7)
print(answers[r])
