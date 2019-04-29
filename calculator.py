#!/usr/bin/env python3
import sys,csv,getopt
from multiprocessing import Queue,Process,Pool

#/Users/tongchuan/louplus
#./calculator.py -c /home/shiyanlou/test.cfg -d /home/shiyanlou/user.csv -o /tmp/gongzi.csv
#./calculator.py -c /Users/tongchuan/louplus/test.cfg -d /Users/tongchuan/louplus/user.csv -o /tmp/gongzi.csv
#./calculator.py -c test.cfg -d user.csv -o gongzi.csv
#./calculator.py -C Chengdu -c test.cfg -d user.csv -o gongzi.csv



class Args:
	_short = ['-C:', '-c:' '-d:', '-o:','-h']
	_long = ['help']
	_help_info = 'Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata'

	def __init__(self,params):
		opts = getopt.getopt(params,''.join(self._short),self._long)
		self._map = dict(opts[0])
		if '-h' in self._map or '--help' in self._map:
			print(self._help_info)

	def get_param_value(self,param):
		return self._map.get(param,None)

	@property
	def config_path(self):
		return self.get_param_value('-c')

	@property
	def salarys_path(self):
		return self.get_param_value('-d')

	@property
	def output_path(self):
		return self.get_param_value('-o')

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



class Calculator(object):
	config_keys = ['JiShuL','JiShuH','YangLao','YiLiao','ShiYe','GongShang','ShengYu','GongJiJin']

	def __init__(self,config_path):
		self.config_path = config_path
		self.get_config()

	def get_config(self):
		ret = {}
		with open(self.config_path) as f:
			for i in f:
				item = i.split('=')
				if len(item) == 2:
					ret[item[0].strip()] = float(item[1].strip())
				else:
					print('config file \'s content is invalid')

		for key in self.config_keys:
			if key not in ret:
				print('config file dismiss {} value'.format(key))
				sys.exit(-1)

			else:
				self.__dict__[key] = ret[key]

	def calculate(self,salary):
		tax_base = 5000
		base = salary
		if salary < self.JiShuL:
			base = self.JiShuL
		if salary > self.JiShuH:
			base = self.JiShuH

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
		return [salary,'{:.2f}'.format(Shebao_count+GongJiJin_count),'{:.2f}'.format(tax),'{:.2f}'.format(salary_real)]

def get_salary_task(path,q):
	with open(path) as f:
			ret = list(csv.reader(f))
	q.put(ret)

def calculate_task(calculator,q1,q2):
	salarys = q1.get()
	ret = []
	for i in salarys:
		code,salary_str = i
		salary = int(salary_str)
		salary_tax = calculator.calculate(salary)
		salary_tax.insert(0,code)
		ret.append(salary_tax)
	q2.put(ret)

def dist_task(q,output_path):
	data = q.get()
	with open(output_path,'w') as f:
			csv.writer(f).writerows(data)

if __name__ == '__main__':
	params = sys.argv[1:]
	args = Args(params)
	# print(args.config_path)
	# print(args.salarys_path)
	# print(args.output_path)

	# calculator = Calculator(args.confit_path)

	# q1 = Queue()
	# q2 = Queue()

	# p_list = []

	# p_list.append(Process(target=get_salary_task, args=(args.salarys_path,q1,)))
	# p_list.append(Process(target=calculate_task, args=(calculator,q1,q2)))
	# p_list.append(Process(target=dist_task,args=(q2,args.output_path)))
	
	# for i in p_list:
	# 	i.start()

	# for i in p_list:
	# 	i.join()




	# users_salary = get_salary_data(args.salarys_path)

	
	# for i in users_salary:
	# 	if len(i) != 2:
	# 		print('{} salarys file is invalid'.format(args.salarys_path))
	# 		sys.exit(-1)
	# 	else:
	# 		salary = int(i[1])
	# 		code = i[0]
	# 		salary,sb_count,tax_count,salary_real = calculator.calculate(salary)
	# 		user = User(code,salary,sb_count,tax_count,salary_real)
	# 		user.dist(args.output_path)


