import numpy as np
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime


# Haetaan aineisto
symbols = ['MSFT', 'AMZN', 'AAPL', 'GOOG', 'FB']
start_date = '2019-1-1'
end_date = '2019-7-1'
stock_data = web.get_data_yahoo(symbols, start_date, end_date)

# Muokataan aineistoa
dt = [str(pd.Timestamp(i).date()) for i in stock_data.index.values]
stock_data = stock_data.reset_index()
stock_data['date'] = dt
adj_stock_data = stock_data[['Adj Close', 'date']]

print(stock_data.head())
print(adj_stock_data.head())


# Visualisoidaan yrityksien pörssikurssit käyttäen kurssien päätöshintaa.
# Kuvien x-akselin merkit ja niiden sijainti.
xtila = pd.date_range(start_date, '2019-08-01', freq='1M')-pd.offsets.MonthBegin(1)
xtila = [str(pd.Timestamp(i).date()) for i in xtila]
xtiloc = np.arange(0, 130.2+1, 20)

# Y-akselin merkit ja niiden sijainti.
ytiloc = np.arange(-0.15, 0.16, 0.05)
ytilab = [f'{str(round(x*100))} %' for x in ytiloc]

# Kuvien käyttämät värit
colors = []
co = plt.rcParams["axes.prop_cycle"]()
for i in range(5):
    col = next(co)['color']
    colors.append(col)



# Osakekurssit
plt.figure(num = 1, figsize=(12,12))
ax = plt.subplot(1,1,1)
for symbol in symbols:
    plt.plot(stock_data['date'], stock_data['Adj Close'][symbol], label = symbol)
ax.set_xticks(xtiloc)
ax.set_xticklabels(xtila)
plt.legend()
plt.xlabel('Päivämäärä', fontsize = 14)
plt.ylabel('Osakeen päätöshinta $', fontsize = 14)
plt.title('Teknologiayhtiöiden osakekurssi', fontsize = 16)
plt.show()



# Yksinkertainen tuottoaste (ROR), jokaiselle yritykselle
plt.figure(num=2, figsize=(12,12))
ax = plt.subplot(1,1,1)
for symbol in symbols:
    plt.plot(stock_data['date'], stock_data['Adj Close'][symbol].pct_change(), label = symbol)
ax.set_xticks(xtiloc)
ax.set_xticklabels(xtila)
ax.set_yticks(ytiloc)
ax.set_yticklabels(ytilab)
plt.legend()
plt.xlabel('Päivämäärä', fontsize = 14)
plt.ylabel('Tuottoaste (ROR) %', fontsize = 14)
plt.title('Teknologia yhtiöiden tuottoaste (ROR)', fontsize = 16)
plt.show()


# Yksinkertainen tuottoaste yhtiöittäin
plt.figure(num=3,figsize=(16,12))
index = 1
for symbol in symbols:
    c = colors[index-1]
    plt.subplot(2,3,index)
    plt.plot(stock_data['date'], stock_data['Adj Close'][symbol].pct_change(), label = symbol, color = c)
    plt.xticks(xtiloc, xtila, rotation = 30)
    plt.yticks(ytiloc, ytilab)
    plt.legend()
    index+=1
plt.suptitle('Teknologia yhtiöiden tuottoaste % yhtiöittäin', fontsize = 16)
plt.show()


# Keskimääräinen päivittäinen tuotto

plt.figure(num=4, figsize=(10,8))
mean_ror = adj_stock_data['Adj Close'].pct_change().mean()
plt.bar(symbols, mean_ror, color = colors)
plt.yticks(np.arange(0.0, 0.0040 , 0.0005), [f'{str(round(x*100,3))} %' for x in np.arange(0.0, 0.0040 , 0.0005)])
plt.title('Päivittäisen tuottoasteen keskiarvo % yhtiöittäin', fontsize = 16)
plt.show()


# Keskimääräinen päivittäisen tuoton varianssi
plt.figure(num=5, figsize=(10,8))
var_ror = adj_stock_data['Adj Close'].pct_change().var()
plt.bar(symbols, var_ror, color = colors)
plt.title('Päivittäisen tuottoasteen varianssi yhtiöittäin', fontsize  =16)
plt.show()



# Keskimääräisen päivittäisen tuoton keskihajonta
plt.figure(num=6, figsize=(10,8))
std_ror = adj_stock_data['Adj Close'].pct_change().std()
plt.bar(symbols, std_ror, color = colors)
plt.title('Päivittäisen tuottoasteen keskihajonta yhtiöittäin', fontsize = 16)
plt.show()



# Korrelaatiot

corr_ror = adj_stock_data['Adj Close'].pct_change().corr()
print(corr_ror)