import statistics

def momentum(data, interval, count):
    mom = 0
    try:
        mom = (data[count-1].c - data[0].c) / data[0].c
        print('momentum = {} over the last {} {}s'.format(mom, count, interval))

    except:
        print('Momentum calculation failed -- Interval Out of Range')

    finally:
        return mom

def RSI(data, count, interval, average):
    close_array = []
    change_array = []
    upward_array = []
    downward_array = []
    upward_average = []
    downward_average = []
    relative_strength = []
    RSI = []
    for i in range(count):
        close_array.append(data[i].c)

    for i in range(len(close_array)):
        if i != 0:
            change = close_array[i] - close_array[i-1]
            change_array.append(change)
            if change >= 0.0:
                upward_array.append(abs(change))
                downward_array.append(0.0)
            if change <= 0.0:
                downward_array.append(abs(change))
                upward_array.append(0.0)

    length_of_movement = count-average
    if length_of_movement > 0:
        for i in range(length_of_movement):
            if i == 0:
                upward_average.append(statistics.mean(upward_array[i:average]))
            else:
                upward_average.append((upward_average[i - 1] * (average - 1) + upward_array[average + i - 1]) / average)

        for i in range(length_of_movement):
            if i == 0:
                downward_average.append(statistics.mean(downward_array[i:average]))
            else:
                downward_average.append((downward_average[i - 1] * (average - 1) + downward_array[average + i - 1]) / average)

        for i in range(len(upward_average)):
            relative_strength.append(upward_average[i] / downward_average[i])

        for i in range(len(relative_strength)):
            RSI.append(100-100/(relative_strength[i]+1))

        return RSI

    else:
        print('Not Enough Points in Data Array to Generate RSI -- Points: {}, Average: {}, Length: {}'.format(count, average, length_of_movement))
        return 0

def MACD(data, count, interval):
    pass

def BollingerBands(data, count, interval):
    pass

def MA(data, count, interval):
    MA_array = []
    for i in range(count):
        MA_array.append(data[-i+1].c)
    return sum(MA_array) / len(MA_array)

def EMA(data, count, interval):
    MA_Array = MA(data, count, interval)
    EMA_Array = []
    smoothing_factor = 2/(count+1)

    for i in range(count):
        if i == 0:
            EMA_Array.append(data[i].c)
        else:
            EMA_val = (data[i].c - data[i-1].c)*smoothing_factor + data[i-1].c
            EMA_Array.append(EMA_val)

    return EMA_Array

def FibbonaciRetracement(data, count, interval):
    pass

def OBV(data, count, interval):
    pass

def IchimokuCloud(data, count, interval):
    pass

def AvgDirIndex(data, count, interval):
    pass

def StochasticOscillator(data, count, interval):
    pass

def StdDeviation(data, count, interval):
    pass
