from datetime import datetime, date


def datetime_now():
    x = datetime.now()
    year = hex(int(str(x.year)[2:]))[2:]
    month = checkLenHex(hex(x.month)[2:])
    day = checkLenHex(hex(x.day)[2:])
    hour = checkLenHex(hex(x.hour)[2:])
    minuts = checkLenHex(hex(x.minute)[2:])
    second = checkLenHex(hex(x.second)[2:])
    week = checkLenHex(
        hex(int(date(x.year, x.month, x.day).strftime("%V")))[2:])

    return year, month, day, hour, minuts, second, week


def checkLenHex(data):
    if len(data) == 1:
        data = "0" + data
    return data


def hexToInt(hex):
    an_integer = int(hex, 16)
    return an_integer


def hexToIntCheckDigits(hex):
    an_integer = int(hex, 16)
    if len(str(an_integer)) == 1:
        an_integer = "0" + str(an_integer)
    return an_integer


def manageYear(year):
    y = str(hexToInt(year))

    if len(y) == 2:
        year = hexToInt(year)
    else:
        year = y[1:3]

    return year


def convertSN(sn):
    sn1 = sn[0:2]
    sn2 = sn[2:4]
    sn3 = sn[4:6]
    sn4 = sn[6:8]

    return sn4 + sn3 + sn2 + sn1


def strToDatetime(day, month, year, hour, minuts, second):
    date_time_str = f"{hexToInt(day)}/{hexToInt(month)}/{year} {hexToInt(hour)}:{hexToInt(minuts)}:{hexToInt(second)}"
    return datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')


def strToTime(Hour, Minuts):
    time_str = f"{hexToInt(Hour)}::{hexToInt(Minuts)}::00"
    return datetime.strptime(time_str, '%H::%M::%S').time()

def checkDigitsHex(crc):
    while len(crc) < 4:
        crc = "0" + crc
    
    return crc
