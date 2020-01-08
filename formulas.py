def momentum(data, interval, count):
    mom = (data[count-1].c - data[0].c) / data[0].c
    print('momentum = {} over the last {} {}'.format(mom, interval, count))
    return mom