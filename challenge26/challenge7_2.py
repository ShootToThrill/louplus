import pandas as pd
import matplotlib.pyplot as plt
def data_handle(df):
    df.set_index('Country code',inplace=True)
    df.drop(df.columns[:5],inplace=True,axis=1)
    df.replace('..',pd.np.nan,inplace=True)
    df = df.fillna(method='ffill',axis=1).fillna(method='bfill',axis=1)
    df.replace(pd.np.nan,0,inplace=True)
    s = df.sum(axis=1)
    # return (s-s.min())/(s.max()-s.min())
    return s

def co2_gdp_plot():
    data = pd.read_excel('ClimateChange.xlsx',sheetname='Data')
    gdp = data[data['Series code']=='NY.GDP.MKTP.CD']
    co2 = data[data['Series code']=='EN.ATM.CO2E.KT']
    country_index_map = gdp['Country code'].to_frame()
    country_index_map.index = pd.np.arange(len(country_index_map))
    print(country_index_map)
    gdp_fill = data_handle(gdp)
    co2_fill = data_handle(co2)
    gdp_min_max = (gdp_fill-gdp_fill.min())/(gdp_fill.max()-gdp_fill.min())
    co2_min_max = (co2_fill-co2_fill.min())/(co2_fill.max()-co2_fill.min())
    x_labels = ['CHN', 'USA', 'GBR', 'FRA','RUS']
    x_labels_index = [ country_index_map[country_index_map['Country code'] == i ].index.values[0] for i in x_labels]
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_title('GDP-CO2')
    ax.set_xlabel('Countries')
    ax.set_ylabel('Values')
    val1 = gdp_min_max.values
    val2 = co2_min_max.values
    x_val = pd.np.arange(len(gdp_min_max))
    ax.plot(x_val,val1,label='GDP-SUM')
    ax.plot(x_val,val2,label='CO2-SUM')
    ax.legend()
    plt.xticks(x_labels_index,x_labels,rotation='vertical')
    fig = plt.gca()
    china = [float('%.3f' % co2_min_max.CHN),float('%.3f' % gdp_min_max.CHN)]
    return fig, china

print(co2_gdp_plot())



