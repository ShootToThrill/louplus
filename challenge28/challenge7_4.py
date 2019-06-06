import pandas as pd
from sklearn.linear_model import LinearRegression

def Temperature():

	ghg = pd.read_csv('GreenhouseGas.csv').set_index('Year')
	tmp = pd.read_csv('GlobalSurfaceTemperature.csv').set_index('Year')
	co2 = pd.read_csv('CO2ppm.csv').set_index('Year')
	combind = pd.concat([ghg,co2,tmp],axis=1)
	feature = combind.loc[1980:].iloc[:,:-3].interpolate()
	train_feature = feature.loc[1980:2010]
	test_feature = feature.loc[2011:]
	train_target = combind.loc[1980:2010].iloc[:,-3:]
	train_target_m = train_target.iloc[:,0]
	train_target_u = train_target.iloc[:,1]
	train_target_l = train_target.iloc[:,2]

	model_m = LinearRegression()
	model_m.fit(train_feature,train_target_m)
	ret_m = model_m.predict(test_feature)

	model_u = LinearRegression()
	model_u.fit(train_feature,train_target_u)
	ret_u = model_u.predict(test_feature)

	model_l = LinearRegression()
	model_l.fit(train_feature,train_target_l)
	ret_l = model_l.predict(test_feature)

	return list(ret_u), list(ret_m), list(ret_l),

print(Temperature())