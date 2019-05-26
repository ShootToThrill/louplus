import pandas as pd

#wget http://labfile.oss.aliyuncs.com/courses/764/apple.csv

def quarter_volume():
	data = pd.read_csv('apple.csv')
	data.index = pd.to_datetime(data.Date)
	rank = data.Volume.resample('Q').sum().sort_values(ascending=False)
	second_volum = rank[1]
	print(second_volum)
	return second_volum

if __name__ == '__main__':
	quarter_volume()