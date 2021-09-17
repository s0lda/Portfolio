from tkinter import *
from tkinter import ttk
import os, json

current_path = os.path.dirname(__file__)
json_file = f'{current_path}\\balances.json'


# check or create json file to keep balances
def check_json(json_file):
    if os.path.isfile(json_file) == True and os.stat(json_file).st_size != 0:
        pass
    else:
        with open(json_file, 'w+') as f:
            file_data = {
                "salary": 0,
                "gift": 0,
                "investments": 0,
                "other": 0,
                "house": 0,
                "transport": 0,
                "health": 0,
                "ent": 0,
                "active": 0,
                "loans": 0,
                "totinc": 0,
                "totexp": 0,
                "balance": 0,
            }
            json.dump(file_data, f, sort_keys= True, indent= 4)

check_json(json_file)


# read balance
def read_json(json_file, balance):
    with open(json_file, 'r') as f:
        data = json.load(f)
        for key, value in data.items():
            if key == balance:
                return value


# calculate total income
def do_totinc(json_file):
    inc_elem = ['salary', 'gift', 'investments', 'other']
    total = []
    with open(json_file, 'r') as f:
        data = json.load(f)
        for key, value in data.items():
            if key in inc_elem:
                total.append(value)
    
    data['totinc'] = sum(total)
    with open(json_file, 'w') as f:
        json.dump(data, f, sort_keys= True, indent= 4)

do_totinc(json_file)


# calculate total expenses
def do_totexp(json_file):
    exp_elem = ['house', 'transport', 'health', 'ent', 'active', 'loans']
    total = []
    with open(json_file, 'r') as f:
        data = json.load(f)
        for key, value in data.items():
            if key in exp_elem:
                total.append(value)
    
    data['totexp'] = sum(total)
    with open(json_file, 'w') as f:
        json.dump(data, f, sort_keys= True, indent= 4)

do_totexp(json_file)


# calculate balance
def do_balance(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    totinc = data['totinc']
    totexp = data['totexp']
    data['balance'] = totinc - totexp
    with open(json_file, 'w') as f:
        json.dump(data, f, sort_keys= True, indent= 4)
    return totinc - totexp

do_balance(json_file)

# get data from input and add it to right balance
def retrive_value(name, json_name, json_file):
    input_value = name.get()

    if input_value.isdigit():
        input_value = int(input_value)
    else:
        input_value = 0

    with open(json_file, 'r') as f:
        data = json.load(f)
    
    data[json_name] += input_value
    with open(json_file, 'w') as f:
        json.dump(data, f, sort_keys= True, indent= 4)

    name.delete(0, END)



root = Tk()
root.title('Expense Tracker')
root.geometry('720x650')
root.iconbitmap(f'{current_path}\icon.ico')


# tabs style
tabs_style = ttk.Style()
tabs_style.configure('Custom.TNotebook.Tab', font= ('Arial', 12, 'bold'), padding= [50, 10])

# tab content style
t_content_style = ttk.Style()
t_content_style.configure('Main.TLabel', font= ('Arial', 12, 'bold'))
money_negative = ttk.Style()
money_negative.configure('Negative.TLabel', font= ('Arial', 12, 'bold'), foreground= 'red')
money_positive = ttk.Style()
money_positive.configure('Positive.TLabel', font= ('Arial', 12, 'bold'), foreground= 'green')


def balance_colour(amount):
    if amount == 0:
        return 'Main.TLabel'
    elif amount > 0:
        return 'Positive.TLabel'
    else:
        return 'Negative.TLabel'


# tabs for summary, income, expenses
tab_control = ttk.Notebook(root, height= 550, width= 700, style= 'Custom.TNotebook')

# tabs
summary = ttk.Frame(tab_control)
income = ttk.Frame(tab_control)
expenses = ttk.Frame(tab_control)

tab_control.add(summary, text= 'Summary')
tab_control.add(income, text= 'Income')
tab_control.add(expenses, text= 'Expenses')

tab_control.grid(row= 0, column= 0)


# balances income
salary_value_int = read_json(json_file, 'salary')
gift_value_int = read_json(json_file, 'gift')
investments_value_int = read_json(json_file, 'investments')
other_value_int = read_json(json_file, 'other')

# balances expenses
house_value_int = read_json(json_file, 'house')
transport_value_int = read_json(json_file, 'transport')
health_value_int = read_json(json_file, 'health')
ent_value_int = read_json(json_file, 'ent')
active_value_int = read_json(json_file, 'active')
loans_value_int = read_json(json_file, 'loans')


# total expenses
totexp_int = read_json(json_file, 'totexp')
# total income
totinc_int = read_json(json_file, 'totinc')
# balance = total income - total expenses
balance_int = read_json(json_file, 'balance')


# summary tab
summary_label_totexp = ttk.Label(summary, text= 'Expenses:', style= 'Main.TLabel')
summary_label_totexp.grid(row= 1, column= 0, ipadx= 5, ipady= 5, padx= 5, pady= 20, sticky= 'w')
totalexp_value = ttk.Label(summary, text= f'£{totexp_int}', style= 'Main.TLabel')
totalexp_value.grid(row= 1, column= 1, ipadx= 0, ipady= 5, padx= 300, pady= 20, sticky= 'e')


summary_label_totinc = ttk.Label(summary, text= 'Income:', style= 'Main.TLabel')
summary_label_totinc.grid(row= 2, column= 0, ipadx= 5, ipady= 0, padx= 5, pady= 20, sticky= 'w')
totalinc_value = ttk.Label(summary, text= f'£{totinc_int}', style= 'Main.TLabel')
totalinc_value.grid(row= 2, column= 1, ipadx= 0, ipady= 5, padx= 300, pady= 20, sticky= 'e')


summary_label_balance = ttk.Label(summary, text= 'BALANCE:', style= 'Main.TLabel')
summary_label_balance.grid(row= 3, column= 0, ipadx= 5, ipady= 0, padx= 5, pady= 70, sticky= 'w')
balance_value = ttk.Label(summary, text= f'£{balance_int}', style= balance_colour(do_balance(json_file)))
balance_value.grid(row= 3, column= 1, ipadx= 0, ipady= 5, padx= 300, pady= 70, sticky= 'e')


# income tab
income_label_salary = ttk.Label(income, text= 'Salary:', style= "Main.TLabel")
income_label_salary.grid(row= 1, column= 0, ipadx= 0, ipady= 0, padx= 5, pady= 20, sticky= 'w')
salary_value = ttk.Label(income, text= f'£{salary_value_int}', style= "Main.TLabel")
salary_value.grid(row= 1, column= 3, ipadx= 0, ipady= 5, padx= 110, pady= 20, sticky= 'e')
salary_entry = ttk.Entry(income, width= 10)
salary_entry.grid(row= 1, column= 1, ipadx= 0, ipady= 5, padx= 0, pady= 20)
salary_button = ttk.Button(income, text= '+', command= lambda: retrive_value(salary_entry, 'salary', json_file))
salary_button.grid(row= 1, column= 2, ipadx= 0, ipady= 5, padx= 0, pady= 20)



income_label_gift = ttk.Label(income, text= 'Gifts:', style= 'Main.TLabel')
income_label_gift.grid(row= 2, column= 0, ipadx= 5, ipady= 0, padx= 5, pady= 20, sticky= 'w')
gift_value = ttk.Label(income, text= f'£{gift_value_int}', style= "Main.TLabel")
gift_value.grid(row= 2, column= 3, ipadx= 0, ipady= 5, padx= 110, pady= 20, sticky= 'e')
gift_entry = ttk.Entry(income, width= 10)
gift_entry.grid(row= 2, column= 1, ipadx= 0, ipady= 5, padx= 0, pady= 20)
gift_button = ttk.Button(income, text= '+', command= lambda: retrive_value(gift_entry, 'gift', json_file))
gift_button.grid(row= 2, column= 2, ipadx= 0, ipady= 5, padx= 0, pady= 20)


income_label_investments = ttk.Label(income, text= 'Investments:', style= 'Main.TLabel')
income_label_investments.grid(row= 3, column= 0, ipadx= 5, ipady= 0, padx= 5, pady= 20, sticky= 'w')
investment_value = ttk.Label(income, text= f'£{investments_value_int}', style= "Main.TLabel")
investment_value.grid(row= 3, column= 3, ipadx= 0, ipady= 5, padx= 110, pady= 20, sticky= 'e')
investment_entry = ttk.Entry(income, width= 10)
investment_entry.grid(row= 3, column= 1, ipadx= 0, ipady= 5, padx= 0, pady= 20)
investment_button = ttk.Button(income, text= '+', command= lambda: retrive_value(investment_entry, 'investments', json_file))
investment_button.grid(row= 3, column= 2, ipadx= 0, ipady= 5, padx= 0, pady= 20)


income_label_other = ttk.Label(income, text= 'Other:', style= 'Main.TLabel')
income_label_other.grid(row= 4, column= 0, ipadx= 5, ipady= 0, padx= 5, pady= 20, sticky= 'w')
other_value = ttk.Label(income, text= f'£{other_value_int}', style= "Main.TLabel")
other_value.grid(row= 4, column= 3, ipadx= 0, ipady= 5, padx= 110, pady= 20, sticky= 'e')
other_entry = ttk.Entry(income, width= 10)
other_entry.grid(row= 4, column= 1, ipadx= 0, ipady= 5, padx= 110, pady= 20)
other_button = ttk.Button(income, text= '+', command= lambda: retrive_value(other_entry, 'other', json_file))
other_button.grid(row= 4, column= 2, ipadx= 0, ipady= 5, padx= 0, pady= 20)


income_label_total = ttk.Label(income, text= 'TOTAL:', style= 'Main.TLabel')
income_label_total.grid(row= 5, column= 0, ipadx= 5, ipady= 0, padx= 5, pady= 70, sticky= 'w')
totinc_value = ttk.Label(income, text= f'£{totinc_int}', style= "Main.TLabel")
totinc_value.grid(row= 5, column= 2, ipadx= 0, ipady= 5, padx= 0, pady= 70, sticky= 'e')


# expenses tab
expenses_label_house = ttk.Label(expenses, text= 'House:', style= 'Main.TLabel')
expenses_label_house.grid(row= 1, column= 0, ipadx= 5, ipady= 5, padx= 5, pady= 20, sticky= 'w')
house_value = ttk.Label(expenses, text= f'£{house_value_int}', style= "Main.TLabel")
house_value.grid(row= 1, column= 3, ipadx= 0, ipady= 5, padx= 110, pady= 20, sticky= 'e')
house_entry = ttk.Entry(expenses, width= 10)
house_entry.grid(row= 1, column= 1, ipadx= 0, ipady= 5, padx= 0, pady= 20)
house_button = ttk.Button(expenses, text= '+', command= lambda: retrive_value(house_entry, 'house', json_file))
house_button.grid(row= 1, column= 2, ipadx= 0, ipady= 5, padx= 0, pady= 20)


expenses_label_transport = ttk.Label(expenses, text= 'Transport:', style= 'Main.TLabel')
expenses_label_transport.grid(row= 2, column= 0, ipadx= 5, ipady= 0, padx= 4, pady= 20, sticky= 'w')
transport_value = ttk.Label(expenses, text= f'£{transport_value_int}', style= "Main.TLabel")
transport_value.grid(row= 2, column= 3, ipadx= 0, ipady= 5, padx= 110, pady= 20, sticky= 'e')
transport_entry = ttk.Entry(expenses, width= 10)
transport_entry.grid(row= 2, column= 1, ipadx= 0, ipady= 5, padx= 0, pady= 20)
transport_button = ttk.Button(expenses, text= '+', command= lambda: retrive_value(transport_entry, 'transport', json_file))
transport_button.grid(row= 2, column= 2, ipadx= 0, ipady= 5, padx= 0, pady= 20)


expenses_label_health = ttk.Label(expenses, text= 'Healthcare:', style= 'Main.TLabel')
expenses_label_health.grid(row= 3, column= 0, ipadx= 5, ipady= 0, padx= 5, pady= 20, sticky= 'w')
health_value = ttk.Label(expenses, text= f'£{health_value_int}', style= "Main.TLabel")
health_value.grid(row= 3, column= 3, ipadx= 0, ipady= 5, padx= 110, pady= 20, sticky= 'e')
health_entry = ttk.Entry(expenses, width= 10)
health_entry.grid(row= 3, column= 1, ipadx= 0, ipady= 5, padx= 0, pady= 20)
health_button = ttk.Button(expenses, text= '+', command= lambda: retrive_value(health_entry, 'health', json_file))
health_button.grid(row= 3, column= 2, ipadx= 0, ipady= 5, padx= 0, pady= 20)


expenses_label_ent = ttk.Label(expenses, text= 'Entertainment:', style= 'Main.TLabel')
expenses_label_ent.grid(row= 4, column= 0, ipadx= 5, ipady= 0, padx= 5, pady= 20, sticky= 'w')
ent_value = ttk.Label(expenses, text= f'£{ent_value_int}', style= "Main.TLabel")
ent_value.grid(row= 4, column= 3, ipadx= 0, ipady= 5, padx= 110, pady= 20, sticky= 'e')
ent_entry = ttk.Entry(expenses, width= 10)
ent_entry.grid(row= 4, column= 1, ipadx= 0, ipady= 5, padx= 0, pady= 20)
ent_button = ttk.Button(expenses, text= '+', command= lambda: retrive_value(ent_entry, 'ent', json_file))
ent_button.grid(row= 4, column= 2, ipadx= 0, ipady= 5, padx= 0, pady= 20)


expenses_label_active = ttk.Label(expenses, text= 'Activities:', style= 'Main.TLabel')
expenses_label_active.grid(row= 5, column= 0, ipadx= 5, ipady= 0, padx= 5, pady= 20, sticky= 'w')
active_value = ttk.Label(expenses, text= f'£{active_value_int}', style= "Main.TLabel")
active_value.grid(row= 5, column= 3, ipadx= 0, ipady= 5, padx= 110, pady= 20, sticky= 'e')
active_entry = ttk.Entry(expenses, width= 10)
active_entry.grid(row= 5, column= 1, ipadx= 0, ipady= 5, padx= 0, pady= 20)
active_button = ttk.Button(expenses, text= '+', command= lambda: retrive_value(active_entry, 'active', json_file))
active_button.grid(row= 5, column= 2, ipadx= 0, ipady= 5, padx= 0, pady= 20)


expenses_label_loans = ttk.Label(expenses, text= 'Loans:', style= 'Main.TLabel')
expenses_label_loans.grid(row= 6, column= 0, ipadx= 5, ipady= 0, padx= 5, pady= 20, sticky= 'w')
loans_value = ttk.Label(expenses, text= f'£{loans_value_int}', style= "Main.TLabel")
loans_value.grid(row= 6, column= 3, ipadx= 0, ipady= 5, padx= 110, pady= 20, sticky= 'e')
loans_entry = ttk.Entry(expenses, width= 10)
loans_entry.grid(row= 6, column= 1, ipadx= 0, ipady= 5, padx= 100, pady= 20)
loans_button = ttk.Button(expenses, text= '+', command= lambda: retrive_value(loans_entry, 'loans', json_file))
loans_button.grid(row= 6, column= 2, ipadx= 0, ipady= 5, padx= 0, pady= 20)


expenses_label_total = ttk.Label(expenses, text= 'TOTAL:', style= 'Main.TLabel')
expenses_label_total.grid(row= 7, column= 0, ipadx= 5, ipady= 0, padx= 5, pady= 70, sticky= 'w')
totexp_value = ttk.Label(expenses, text= f'£{totexp_int}', style= "Main.TLabel")
totexp_value.grid(row= 7, column= 3, ipadx= 0, ipady= 5, padx= 0, pady= 70)


def update():
    salary_value['text'] = read_json(json_file, 'salary')
    gift_value['text'] = read_json(json_file, 'gift')
    investment_value['text'] = read_json(json_file, 'investments')
    other_value['text'] = read_json(json_file, 'other')
    house_value['text'] = read_json(json_file, 'house')
    transport_value['text'] = read_json(json_file, 'transport')
    health_value['text'] = read_json(json_file, 'health')
    ent_value['text'] = read_json(json_file, 'ent')
    active_value['text'] = read_json(json_file, 'active')
    loans_value['text'] = read_json(json_file, 'loans')

    do_totinc(json_file)
    do_totexp(json_file)
    do_balance(json_file)

    totalexp_value['text'] = read_json(json_file, 'totexp')
    totalinc_value['text'] = read_json(json_file, 'totinc')
    totexp_value['text'] = read_json(json_file, 'totexp')
    totinc_value['text'] = read_json(json_file, 'totinc')
    balance_value['text'] = read_json(json_file, 'balance')

    balance_value['style'] = balance_colour(do_balance(json_file))

    root.after(1000, update)
update()

if __name__ == '__main__':
    root.mainloop()
