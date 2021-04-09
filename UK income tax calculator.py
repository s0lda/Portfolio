income = int(input('Enter your salary: ''\n'))
# Tax Free Allowance
tax_free = 12500
taxpayable = 0
# Tax Bands
std_amount = 50000
higher_amount = 100000
adv_amount = 150000
# in UK over 100k income will reduce tax free allowance. every £2 will reduce allowance by £1
allowance_reduction = (income - higher_amount) / 2
# over 100k you start loosing allowance, that's the end of it.
allowance_stop = tax_free * 2

#NI contribution
weekly_wage = income / 52
ni1 = 183
ni2 = 962

# calculating the amount of tax owed

# tax free amount
if income <= tax_free:
    taxpayable = 0
# 20% rate
elif income <= std_amount:
    taxpayable = (income - tax_free) * 20 / 100
# 40% rate
elif income <= adv_amount:
    # 40% rate for below 100k income
    if income > std_amount and income <= higher_amount:
        taxpayable = ((std_amount - tax_free) * 20 / 100) + ((income - std_amount) * 40 / 100)
    # 40% rate for over 100k with reducing tax allowance
    elif income > higher_amount and income <= (higher_amount + allowance_stop):
        # lower band(including tax allowance) @ 20% + income - higher band @ 40% + allowance reduction @ 40%
        taxpayable = ((std_amount - tax_free) * 20 / 100) + ((higher_amount - std_amount) * 40 / 100 ) + ((income - higher_amount + allowance_reduction) * 40 / 100)
    # 40% rate for over 100k with no tax allowance left
    elif income > (higher_amount + allowance_stop) and income <= adv_amount:
        # higher band + tax allowance * 2 = no Tax free allowance anymore 
        taxpayable = ((std_amount - tax_free) * 20 / 100) + ((income - std_amount) * 40 / 100) + (tax_free * 40 / 100)
# calculating 45% rate
elif income > adv_amount:
    taxpayable = ((std_amount - tax_free) * 20 / 100) + ((adv_amount - std_amount) * 40 / 100) + (tax_free * 40 / 100) + ((income - adv_amount) * 45 / 100)

# calculating National Insurance contribution

# NI rate free amount
if weekly_wage <= ni1:
    ni = 0
# calculating 12 % NI rate
elif weekly_wage > ni1 and weekly_wage <= ni2:
    ni = ((weekly_wage - ni1) * 12 / 100) * 52
# calculating 2% NI rate
elif weekly_wage > ni2:
    ni = ((((weekly_wage - ni1) - abs(ni2 - weekly_wage)) * 12 / 100) + ((weekly_wage - ni2) * 2 / 100)) * 52

# total deductions and home take
total_deductions = taxpayable + ni
home = income - total_deductions
weekly_home = home / 52

print('Total tax to pay is:      ', taxpayable)
print('You NI contribution is:   ', round(ni, 2))
print('Total deductions:         ', total_deductions)
print('Your home take is:        ', round(home, 2))
print('Your weekly home take is: ', round(weekly_home,2))