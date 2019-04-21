#!/usr/bin/env python3
import sys,csv

#/Users/tongchuan/louplus
#./calculator.py -c /home/shiyanlou/test.cfg -d /home/shiyanlou/user.csv -o /tmp/gongzi.csv
#./calculator.py -c /Users/tongchuan/louplus/test.cfg -d /Users/tongchuan/louplus/user.csv -o /tmp/gongzi.csv


class Args:
	def __init__(self,params):
		self._params = params

	def get_param_value(self,param):
		index = self._params.index(param)
		value_index = index+1
		if 0 < value_index < len(self._params):
			return self._params[value_index]
		else:
			print('Params Error')
			sys.exit(-1)

	@property
	def confit_path(self):
		return self.get_param_value('-c')

	@property
	def salarys_path(self):
		return self.get_param_value('-d')

	@property
	def output_path(self):
		return self.get_param_value('-o')


class Config:
	def __init__(self,path):
		self._path = path

	@property
	def data(self):
		ret = {}
		with open(self._path) as f:
			for i in f:
				item = i.split('=')
				if len(item) == 2:
					ret[item[0].strip()] = float(item[1].strip())
				else:
					print('config file \'s content is invalid')
		return ret


class Salarys:
	def __init__(self,path):
		self._path = path

	@property
	def data(self):
		with open(self._path) as f:
			ret = list(csv.reader(f))
		return ret

class User:
	def __init__(self,code,salary,sb_count,tax_count,salary_real):
		self.code = code
		self.salary = salary
		self.sb_count ='{:.2f}'.format(sb_count)
		self.tax_count ='{:.2f}'.format(tax_count)
		self.salary_real ='{:.2f}'.format(salary_real)



	def dist(self,path):
		with open(path,'a') as f:
			csv.writer(f).writerow([self.code,self.salary,self.sb_count,self.tax_count,self.salary_real])



#JiShuL,JiShuH,YangLao,YiLiao,ShiYe,GongShang,ShengYu,GongJiJin
class Calculator:
	def __init__(self,JiShuL,JiShuH,YangLao,YiLiao,ShiYe,GongShang,ShengYu,GongJiJin):
		self.JiShuL = JiShuL
		self.JiShuH = JiShuH
		self.YangLao = YangLao
		self.YiLiao = YiLiao
		self.ShiYe = ShiYe
		self.GongShang = GongShang
		self.ShengYu = ShengYu
		self.GongJiJin = GongJiJin

	def calculate(self,salary):
		tax_base = 5000
		base = salary
		if salary < self.JiShuL:
			base = JiShuL
		if salary > self.JiShuH:
			base = JiShuH

		Shebao_count = base * (self.YangLao + self.YiLiao + self.ShiYe + self.GongShang + self.ShengYu )
		GongJiJin_count = base * self.GongJiJin

		taxable = salary  - Shebao_count - GongJiJin_count - tax_base
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

		salary_real = salary - Shebao_count - GongJiJin_count - tax
		return (salary,Shebao_count+GongJiJin_count,tax,salary_real)

if __name__ == '__main__':
	params = sys.argv[1:]
	args = Args(params)
	print(args.confit_path)
	print(args.salarys_path)
	print(args.output_path)

	config = Config(args.confit_path)
	config_data = config.data

	salarys = Salarys(args.salarys_path)
	##JiShuL,JiShuH,YangLao,YiLiao,ShiYe,GongShang,ShengYu,GongJiJin
	calculator = Calculator(config_data.get('JiShuL'),config_data.get('JiShuH'),config_data.get('YangLao'),config_data.get('YiLiao'),config_data.get('ShiYe'),config_data.get('GongShang'),config_data.get('ShengYu'),config_data.get('GongJiJin'))
	users_salary = salarys.data
	for i in users_salary:
		if len(i) != 2:
			print('{} salarys file is invalid'.format(args.salarys_path))
			sys.exit(-1)
		else:
			salary = int(i[1])
			code = i[0]
			salary,sb_count,tax_count,salary_real = calculator.calculate(salary)
			user = User(code,salary,sb_count,tax_count,salary_real)
			user.dist(args.output_path)

