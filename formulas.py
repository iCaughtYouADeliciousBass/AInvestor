def momentum(data, interval, count):
    mom = 0
    try:
        mom = (data[count-1].c - data[0].c) / data[0].c
        print('momentum = {} over the last {} {}'.format(mom, interval, count))

    except:
        print('Momentum calculation failed -- Interval Out of Range')

    finally:
        return mom

def RSI():
    pass