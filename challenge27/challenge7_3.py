import pandas as pd
from functools import reduce
import matplotlib.pyplot as plt

def data_fix(df):
    df.set_index('Country code',inplace=True)
    df.drop(df.columns[:5],inplace=True,axis=1)
    df.replace('..',pd.np.nan,inplace=True)
    df = df.fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    df.replace(pd.np.nan,0,inplace=True)
    return df

def climate_plot():
	tmp = pd.read_excel('GlobalTemperature.xlsx')
	clt = pd.read_excel('ClimateChange.xlsx',sheetname='Data')
	codes = ['EN.ATM.CO2E.KT','EN.ATM.METH.KT.CE','EN.ATM.NOXE.KT.CE','EN.ATM.GHGO.KT.CE','EN.CLC.GHGR.MT.CE']
	clts = [clt[clt['Series code'] == code] for code in codes]
	clts_fix = [data_fix(clt) for clt in clts]
	clts_all = reduce(lambda x,y:x+y,clts_fix)
	clts_sum = clts_all.sum()
	clts_sum = clts_sum.iloc[:-1]
	clts_sum_min_max = (clts_sum-clts_sum.min())/(clts_sum.max()-clts_sum.min())

	tmp.replace(pd.np.nan,0,inplace=True)
	tmp['Date'] = pd.to_datetime(tmp['Date'])
	tmp.set_index('Date',inplace=True)

	tmp_year = tmp.resample('A').sum()
	tmp_year.index = tmp_year.index.year
	tmp_year = tmp_year.loc[1990:2010]
	tmp_min_max = (tmp_year-tmp_year.min())/(tmp_year.max()-tmp_year.min())

	p1 = pd.concat([clts_sum_min_max,tmp_min_max.drop(tmp_min_max.columns[1:3],axis=1)],axis=1)
	p1.rename(columns={p1.columns[0]:'Total GHG'},inplace=True)

	fig = plt.figure(figsize=(16,10))
	ax1 = fig.add_subplot(2,2,1)
	ax1 =p1.plot(ax=ax1,legend=True, grid=True,kind='line')
	ax1.set_xlabel('Years')
	ax1.set_ylabel('Values')
	ax1.set_xticks(list(map(lambda x: int(x), ax1.get_xticks())))

	ax2 = fig.add_subplot(2,2,2)
	ax2 =p1.plot(ax=ax2,legend=True, grid=True,kind='bar')

	p3_data = tmp.drop(tmp.columns[1:3],axis=1).resample('Q').sum()
	ax3 = fig.add_subplot(2,2,3)
	ax3 =p3_data.plot(ax=ax3,legend=True, grid=True,kind='area')

	ax4 = fig.add_subplot(2,2,4)
	ax5 =p3_data.plot(ax=ax4,legend=True, grid=True,kind='kde')

	# fig.show()

	return fig.gca()