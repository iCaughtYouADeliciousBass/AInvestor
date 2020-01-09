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
    change_array = ['0']
    upward_array = []
    downward_array = []
    upward_average = []
    downward_average = []
    relative_strength = []
    RSI = []
    for i in range(count):
        close_array.append(data[count].c)

    for i in len(close_array)-2:
        change = close_array[i+1] - close_array[i]
        change_array.append(change)
        if change >= 0:
            upward_array.append(abs(change))
            downward_array.append('0')
        if change <= 0:
            downward_array.append(abs(change))
            upward_array.append('0')

    temp_up_avg = upward_array[average-1:]
    temp_down_avg = downward_array[average-1:]
    length_of_movement = len(upward_array)-average+1
    if length_of_movement > 0:
        for i in range(length_of_movement):
            if i == 0:
                upward_average.append(sum(upward_array[i:average+i]))
            else:
                upward_average.append((upward_average[i - 1] * (average - 1) + upward_array[average + i]) / average)

        for i in range(length_of_movement1):
            if i==0:
                downward_average.append(sum(downward_array[i:average+i]))
            else:
                downward_average.append((downward_average[i - 1] * (average - 1) + downward_array[average + i]) / average)

        for i in len(upward_average):
            relative_strength.append(upward_average[i] / downward_average[i])

        for i in len(relative_strength):
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
    pass

def EMA(data, count, interval):
    pass

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
