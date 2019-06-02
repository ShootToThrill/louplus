import pandas as pd
import matplotlib.pyplot as plt
def data_handle(df):
    df.set_index('Country code',inplace=True)
    df.drop(df.columns[:5],inplace=True,axis=1)
    df.replace('..',pd.np.nan,inplace=True)
    df = df.fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    df.replace(pd.np.nan,0,inplace=True)
    s = df.sum(axis=1)
    return (s-s.min())/(s.max()-s.min())

def co2_gdp_plot():
    data = pd.read_excel('ClimateChange.xlsx',sheetname='Data')
    gdp = data[data['Series code']=='NY.GDP.MKTP.CD']
    co2 = data[data['Series code']=='EN.ATM.CO2E.KT']
    gdp_min_max = data_handle(gdp)
    co2_min_max = data_handle(co2)
    fig = plt.subplot()
    gdp_min_max.plot()
    co2_min_max.plot()
    plt.show()

co2_gdp_plot()



