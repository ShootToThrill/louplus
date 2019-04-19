import sys

base = 5000

if len(sys.argv) != 2:
	print('Parameter Error')
	raise ValueError('Parameter Error')

salary = sys.argv[1]

try:
	salary_num = int(salary)
except ValueError:
	print('Parameter Error')
	exit()

taxable = salary_num - base
tax = 0

if 0 < taxable <= 3000:
	tax = taxable * 3e-2 - 0
elif 3000 < taxable <= 12000:
	tax = taxable * 10e-2 - 210
elif 12000 < taxable <= 25000:
	tax = taxable * 20e-2 -1410
elif 25000 < taxable <= 35000:
	tax = taxable * 25e-2 - 2660
elif 35000 < taxable <= 55000:
	tax = taxable * 30e-2 - 4410
elif 55000 < taxable <= 80000:
	tax = taxable * 35e-2 -7160
elif taxable > 80000:
	tax = taxable * 40e-2 - 15160

print('{:.2f}'.format(tax))