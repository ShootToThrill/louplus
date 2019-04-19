import sys

def calculate(data):
	base = 5000
	if data.count(':') != 1 or data.startswith(':') or data.endswith(':'):
		return 'Parameter Error'

	code, salary = data.split(':')

	try:
		salary_num = int(salary)
	except ValueError:
		return 'Parameter Error'
		
	insurance_num = insurance(salary_num)
	taxable = salary_num - base - insurance_num
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

	return (code,salary_num - tax - insurance_num)
	

def insurance(salary):
	return  salary * (8+2+0.5+6)/100


if __name__ == '__main__':

	datas = sys.argv[1:]
	for data in datas:
		ret = calculate(data)
		if isinstance(ret, str):
			print(ret)
			continue
		(code, rel_salary) = calculate(data)
		print('{}:{:.2f}'.format(code, rel_salary))

