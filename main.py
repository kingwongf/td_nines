import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf

def recurv_count(a):
    '''
    assume window of 4 consecutives
    a = [-1,-1,-1,-1,-1,1,1,1,1]

    :return:
    '''


def td_nines(df):
    '''

    :param df: with columns ['Open', 'Low', 'High', 'Close']
    :return:
    '''

    count=0
    ind=[np.nan]*4
    close_list = df.Close.values.tolist()
    high_list = df.High.values.tolist()
    low_list = df.Low.values.tolist()
    ideal = pd.Series()
    for i, el in enumerate(close_list):
        if i <4:
            continue
        if el >close_list[i-4] and count >= 0:
            count+=1
        elif el <close_list[i-4] and count <= 0:
            count-=1
        else:
            count=0
        ind.append(count)


        ## ideal sell when highs of 6 and 7 < highs of 8 and 9
        if max(high_list[i-3:i-1]) < min(high_list[i-1:i+1]) and count == 9:
            ideal[df.iloc[i].name]= 'sell'
            count = 0
        ## ideal buy when lows of 6 and 7 > lows of 8 and 9
        if min(low_list[i-3:i-1]) > max(low_list[i-1:i+1]) and count == -9:
            ideal[df.iloc[i].name]= 'buy'
            count = 0

    print(ideal)

    kwargs = dict(warn_too_much_data=1000000)
    fig, axs = mpf.plot(df,show_nontrading=False, returnfig=True, **kwargs)

    _addlabelmpfplot(axs[0], df, ind, ideal)
    plt.show()





def _addlabelmpfplot(ax, ohlc, label_li, ideal):
    transform = ax.transData.inverted()
    text_pad = transform.transform((0, 10))[1] - transform.transform((0, 0))[1]
    kwargs = dict(horizontalalignment='center')
    for i,label in enumerate(label_li):
        if i > 4:
            # ideal_candle = ideal.get(ohlc.iloc[i].name.strftime("Y-%m-%d"), None)
            c = 'r' if abs(label)==9 else 'k'
            if label <0:

                # label = f"{label} {ideal_candle}" if isinstance(ideal_candle, str) else label
                ax.text(i, ohlc.iloc[i].High + text_pad, label, verticalalignment='bottom',c=c, **kwargs)
            elif label > 0:
                # label = f"{label} {ideal_candle}" if isinstance(ideal_candle, str) else label
                ax.text(i, ohlc.iloc[i].Low - text_pad, label, verticalalignment='bottom', c=c, **kwargs)




# td_nines(pd.read_csv('EURUSD.csv', index_col=["Date"], parse_dates=['Date']).sort_index())
td_nines(pd.read_csv('BTCGBP.csv', index_col=["Date"], parse_dates=['Date']).sort_index())