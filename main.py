import pandas as pd
import matplotlib.pyplot as plt
import math


def ema(n, d):
    result = []
    for j in range(len(d)):
        numerator = 0
        denominator = 0
        alfa = 2 / (n + 1)
        for i in range(n):
            if j - i >= 0:
                numerator += (1 - alfa) ** i * d[j - i]
                denominator += (1 - alfa) ** i
        result.append(numerator / denominator)

    return result


data = pd.read_csv('apator.csv')
data = data.head(1000)
x = data['Data']
y = data['Zamkniecie']
x_axis = []
for i in range(0, len(data), len(data)//10):
    x_axis.append(i)
x_axis.append(len(data)-1)
long_avg_span = 200
long_avg = ema(long_avg_span, y)
plt.xticks(x_axis)

# plt.plot(x, long_avg)
plt.plot(x, y)
plt.show()

# MACD ---------------------------------------------
long_ema_span = 26
short_ema_span = 12
macd_ema_span = 9

ema12 = ema(short_ema_span, y)
ema26 = ema(long_ema_span, y)
macd = []
for i in range(len(ema26)):
    macd.append(ema12[i] - ema26[i])

signal = ema(macd_ema_span, macd)

plt.xticks(x_axis)
plt.plot(x, signal)
plt.plot(x, macd)
plt.legend(["SIGNAL", "MACD"])
plt.show()

# SIMPLE SIMULATION -----------------------------
capital = 1000
money = 0
mc_below = 0
start_point = long_avg_span
print("start capital as money: " + str(capital * y[start_point]))
if macd[start_point] < signal[start_point]:
    mc_below = 1

for i in range(start_point, len(data)):
    if signal[i] <= macd[i] and mc_below == 1:
        mc_below = 0
        capital += math.floor(money/y[i] * 100)/100
        money = 0
    elif macd[i] <= signal[i] and mc_below == 0:
        mc_below = 1
        money += math.floor(capital * y[i] * 100) / 100
        capital = 0
money += math.floor(capital * y[len(y)-1] * 100) / 100
print("simple simulation end money: " + str(money))
print()

# ENHANCED SIMULATION --------------------------------------
capital = 1000
money = 0
mc_below = 0
stop_loss = long_avg[start_point]
profit_cap = y[start_point] + (y[start_point] - stop_loss) * 1.5
print("start capital as money: " + str(capital * y[start_point]))
if macd[start_point] < signal[start_point]:
    mc_below = 1

for i in range(start_point, len(data)):
    if signal[i] <= macd[i] < 0 and mc_below == 1 and long_avg[i] < y[i] and money != 0:
        capital += math.floor(money/y[i] * 100)/100
        money = 0
        stop_loss = long_avg[i]
        profit_cap = y[i] + (y[i] - stop_loss) * 1.5
        # print("bought : money: " + str(money) + "   for: " + str(y[i]) + "  on: " + str(x[i]))
    elif macd[i] < signal[i] > 0 and mc_below == 0 and long_avg[i] > y[i] and money == 0:
        money += math.floor(capital * y[i] * 100) / 100
        capital = 0
        # print("sold : money: " + str(money) + "   for: " + str(y[i]) + "  on: " + str(x[i]))

    if money == 0 and y[i] >= profit_cap != 0:
        money += math.floor(capital * y[i] * 100) / 100
        capital = 0
        # print("success : money: " + str(money) + "   for: " + str(y[i]) + "  on: " + str(x[i]))
    if money == 0 and y[i] <= stop_loss:
        money += math.floor(capital * y[i] * 100) / 100
        capital = 0
        # print("emergency : money: " + str(money) + "   for: " + str(y[i]) + "  on: " + str(x[i]))

    if signal[i] <= macd[i] and mc_below == 1:
        mc_below = 0
    elif macd[i] <= signal[i] and mc_below == 0:
        mc_below = 1


money += math.floor(capital * y[len(y)-1] * 100)/100
print("enhanced simulation end money: " + str(money))


# EXAMPLES SIMPLE INVESTMENT ------------------
ex1_x = x.head(928)
ex1_x = ex1_x.tail(16)
x_axis = [0, 15]
ex1_y = y.head(928)
ex1_y = ex1_y.tail(16)
plt.xticks(x_axis)
plt.plot(ex1_x, ex1_y)
plt.show()
ex1_macd = macd[:928]
ex1_macd = ex1_macd[-16:]
ex1_signal = signal[:928]
ex1_signal = ex1_signal[-16:]
plt.xticks(x_axis)
plt.plot(ex1_x, ex1_signal)
plt.plot(ex1_x, ex1_macd)
plt.legend(["SIGNAL", "MACD"])
plt.show()

ex1_x = x.head(852)
ex1_x = ex1_x.tail(5)
x_axis = [1, 4]
ex1_y = y.head(852)
ex1_y = ex1_y.tail(5)
plt.xticks(x_axis)
plt.plot(ex1_x, ex1_y)
plt.show()
ex1_macd = macd[:852]
ex1_macd = ex1_macd[-5:]
ex1_signal = signal[:852]
ex1_signal = ex1_signal[-5:]
plt.xticks(x_axis)
plt.plot(ex1_x, ex1_signal)
plt.plot(ex1_x, ex1_macd)
plt.legend(["SIGNAL", "MACD"])
plt.show()
