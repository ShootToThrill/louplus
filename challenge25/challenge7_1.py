import pandas as pd
def co2():
    data = pd.read_excel('ClimateChange.xlsx')
    data = data[data['Series code']=='EN.ATM.CO2E.KT']
    data.set_index(data.columns[0],inplace=True)
    data.drop(data.columns[:5],axis=1,inplace=True)
    data.replace('..',pd.np.nan,inplace=True)
    data = data.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1)
    data.dropna(how='all', inplace=True)
    sum = data.sum(axis=1).to_frame()
    country = pd.read_excel('ClimateChange.xlsx',sheetname='Country')
    country.set_index(country.columns[0],inplace=True)
    country = country[['Country name','Income group']]
    combine = pd.concat([sum,country],axis=1)
    combine.rename(columns={combine.columns[0]:'Sum emissions'},inplace=True)
    column1 = combine.groupby('Income group').sum()
    sort1 = combine.sort_values(by=combine.columns[0],ascending=False).groupby('Income group').head(1)
    sort1 = sort1.set_index('Income group')
    column1['Highest emission country'] = sort1['Country name']
    column1['Highest emissions'] = sort1['Sum emissions']
    sort2 = combine.sort_values(by=combine.columns[0],ascending=True).groupby('Income group').head(1)
    sort2 = sort2.set_index('Income group')
    column1['Lowest emission country'] = sort2['Country name']
    column1['Lowest emissions'] = sort2['Sum emissions']
    return column1

if __name__ == '__main__':
    print(co2())
