# ------------------------Dependencies----------------------------------------------------------------------------------
import statistics

# ------------------------Clamp-----------------------------------------------------------------------------------------


def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)

# ------------------------Momentum--------------------------------------------------------------------------------------


def momentum(data):

    try:
        mom = (data[len(data) - 1].c - data[0].c) / data[0].c

    except ValueError:
        print('Momentum calculation failed -- Interval Out of Range')
        mom = None

    finally:
        return mom

# ------------------------Relative Strength Index-----------------------------------------------------------------------


def RSI(data, average):
    count = len(data)
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
            change = close_array[i] - close_array[i - 1]
            change_array.append(change)
            if change >= 0.0:
                upward_array.append(abs(change))
                downward_array.append(0.0)
            if change <= 0.0:
                downward_array.append(abs(change))
                upward_array.append(0.0)

    length_of_movement = count - average
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
                downward_average.append(
                    (downward_average[i - 1] * (average - 1) + downward_array[average + i - 1]) / average)
        try:
            for i in range(len(upward_average)):
                # If the array contains a zero, append with last data point or median of last 2 points
                if upward_average[i] == 0:
                    if i == len(upward_average)-1:
                        upward_average[i] = upward_average[i-1]
                    else:
                        upward_average[i] = (upward_average[i-1] + upward_average[i+1]) / 2
                if downward_average[i] == 0:
                    if i == len(downward_average)-1:
                        downward_average[i] = downward_average[i-1]
                    else:
                        downward_average[i] = (downward_average[i-1] + downward_average[i+1]) / 2
                relative_strength.append(upward_average[i] / downward_average[i])
        except ZeroDivisionError:
            print("Uh-oh! RSI Calc failed - zero downward average")

        for i in range(len(relative_strength)):
            RSI.append(100 - 100 / (relative_strength[i] + 1))

        return RSI

    else:
        print('Not Enough Points in Data Array to Generate RSI -- Points: {}, Average: {}, Length: {}'.format(count,
                                                                                                              average,
                                                                                                              length_of_movement))
        return 0

# ------------------------Moving Average Convergence Divergence---------------------------------------------------------


def MACD(data, interval_a: int = 12, interval_b: int = 26):
    MACD_array = []
    twelve_day_EMA = EMA(data, interval_a)
    twentysix_day_EMA = EMA(data, interval_b)
    for i in range(len(twentysix_day_EMA)):
        MACD_array.append(twelve_day_EMA[i]-twentysix_day_EMA[i])

    return MACD_array

# ------------------------Bollinger Bands-------------------------------------------------------------------------------


def BollingerBands(data):
    pass

# ------------------------Moving Average--------------------------------------------------------------------------------


def MA(data):
    count = len(data)
    MA_array = []
    for i in range(count):
        MA_array.append(data[-i + 1].c)
    return sum(MA_array) / len(MA_array)

# ------------------------Exponential Moving Average--------------------------------------------------------------------


def EMA(data, smoothing):
    EMA_Array = []
    count = len(data)
    smoothing_factor = 2 / (smoothing + 1)
    count = len(data)
    for i in range(count):
        if i == 0:
            EMA_Array.append(data[i].c)
        else:
            EMA_val = (data[i].c - data[i - 1].c) * smoothing_factor + data[i - 1].c
            EMA_Array.append(EMA_val)

    return EMA_Array

# ------------------------Fibbonaci Retracement-------------------------------------------------------------------------


def FibbonaciRetracement(data):
    close_val_array = []
    count = len(data)
    for i in range(count):
        close_val_array.append(data[i].c)
    min_val = min(close_val_array)
    max_val = max(close_val_array)
    difference = max_val - min_val
    out_dict = {'0%': min_val, '23.6%': 0.236 * difference + min_val, '38.2%': 0.382 * difference + min_val,
                '50.0%': 0.5 * difference + min_val,
                '61.8%': 0.618 * difference + min_val, '100%': max_val}
    return out_dict

# ------------------------On Balance Volume-----------------------------------------------------------------------------


def OBV(data):
    pass

# ------------------------Ichimoku Cloud--------------------------------------------------------------------------------


def IchimokuCloud(data):
    pass

# ------------------------Average Direction Index-----------------------------------------------------------------------


def AvgDirIndex(data):
    pass

# ------------------------Stochastic Oscillator-------------------------------------------------------------------------


def StochasticOscillator(data):
    pass

# ------------------------Standard Deviation----------------------------------------------------------------------------


def StdDeviation(data):
    pass
