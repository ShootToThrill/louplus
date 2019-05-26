import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#wget http://labfile.oss.aliyuncs.com/courses/764/user_study.json

def data_plot():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    df = pd.read_json('user_study.json')
    ax.plot(df[['user_id','minutes']].groupby('user_id').sum())
    ax.set_xticks(np.arange(0,230000,50000))
    ax.set_title('StudyData')
    ax.set_xlabel('User ID')
    ax.set_ylabel('Study Time')
    plt.show()
    return ax

if __name__ == '__main__':
    data_plot()
