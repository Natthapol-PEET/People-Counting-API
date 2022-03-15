from flask import Flask, request, jsonify
from flask_cors import CORS

from time import time
from datetime import datetime, date

# CRC-16/MODBUS
from utils.crc16 import crc16Encode

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET', 'POST'])
def hello():
    return {"msg": "Hello, from flask"}


t1 = time()


@app.route('/dataport', methods=['GET', 'POST'])
def dataport():
    global t1

    t2 = time()
    print(f"time: {t2-t1}")
    t1 = t2

    print(f"request.method: {request.method}")
    print(request.values.to_dict())

    if request.method == 'GET':
        return 'Hello, from flask'

    if request.method == 'POST' and request.values.to_dict()["cmd"] == "cache":
        print("************************************************")

        data = request.values.to_dict()["data"]
        # server request

        year = hexToInt(data[0:2])
        month = hexToIntCheckDigits(data[2:4])
        day = hexToIntCheckDigits(data[4:6])
        hour = hexToIntCheckDigits(data[6:8])
        minuts = hexToIntCheckDigits(data[8:10])
        second = hexToIntCheckDigits(data[10:12])
        focus = hexToIntCheckDigits(data[12:14])
        dxIN1 = data[14:16]
        dxIN2 = data[16:18]
        dxIN3 = data[18:20]
        dxIN4 = data[20:22]
        dxOUT1 = data[22:24]
        dxOUT2 = data[24:26]
        dxOUT3 = data[26:28]
        dxOUT4 = data[28:30]

        print(
            f"datetime >> {year + 2000}-{month}-{day} {hour}:{minuts}:{second}")
        # print(f"focus >> {focus}")
        print(
            f"dxIN1 {dxIN4 + dxIN3 + dxIN2 + dxIN1} >> {hexToInt(dxIN4 + dxIN3 + dxIN2 + dxIN1)}")
        print(
            f"dxOUT1 {dxOUT4 + dxOUT3 + dxOUT2 + dxOUT1} >> {hexToInt(dxOUT4 + dxOUT3 + dxOUT2 + dxOUT1)}")
        # print(f'count >> {request.values.to_dict()["count"]}')

        # server response
        x = datetime.now()

        answerType = "01"   # 00 failed, 01 success
        flags = "0000"
        commandType = "03"    # [01, 02, 03]
        year = hex(int(str(x.year)[2:]))[2:]
        month = checkLenHex(hex(x.month)[2:])
        day = checkLenHex(hex(x.day)[2:])
        hour = checkLenHex(hex(x.hour)[2:])
        minuts = checkLenHex(hex(x.minute)[2:])
        second = checkLenHex(hex(x.second)[2:])
        week = checkLenHex(
            hex(int(date(x.year, x.month, x.day).strftime("%V")))[2:])
        openHour = checkLenHex(hex(8)[2:])   # 8
        openMinuts = "00"  # 00
        closeHour = checkLenHex(hex(20)[2:])
        closeMinuts = "00"

        hex_string = answerType + flags + commandType + year + month + day + \
            hour + minuts + second + week + openHour + openMinuts + \
            closeHour + closeMinuts

        result = hex_string + crc16Encode(hex_string)
        print(result)
        # return {"result": result}
        return f"result={result}"

    # if request.method == 'GET':
    #     print(request)

    if request.values.to_dict()["cmd"] == "getsetting":
        # print(f"form: {request.form.to_dict()}")
        # print(request.form.to_dict()["cmd"])
        # print(request.form.to_dict()["flag"])
        # print(request.form.to_dict()["data"])

        # print(f"values: {request.values.to_dict()}")
        # print(request.values.to_dict()["cmd"])
        # print(request.values.to_dict()["flag"])
        valuesDict = request.values.to_dict()
        cmd = valuesDict["cmd"]
        # flag = valuesDict["flag"]
        data = valuesDict["data"]

        print(f"cmd     >> {cmd}")
        # print(f"flag    >> {flag}")
        # print(f"data    >> {data}")

        SN = data[0:8]              # 4 byte
        commondType = data[8:10]    # 1 byte
        # speed = data[10:12]         # 1 byte
        # recordingCycle = data[12:14]    # 1 byte
        # uploadCycle = data[14:16]       # 1 byte
        # fixedTimeUpload = data[16:18]   # 1 byte
        # uploadHour1 = data[18:20]       # 1 byte
        # uploadMinute1 = data[20:22]     # 1 byte
        # uploadHour2 = data[22:24]       # 1 byte
        # uploadMinute2 = data[24:26]     # 1 byte
        # uploadHour3 = data[26:28]       # 1 byte
        # uploadMinute3 = data[28:30]     # 1 byte
        # uploadHour4 = data[30:32]       # 1 byte
        # uploadMinute4 = data[32:34]     # 1 byte
        # model = data[34:36]             # 1 byte
        # disableType = data[36:38]       # 1 byte
        # macAddress1 = data[38:52]       # 7 byte
        # macAddress2 = data[52:66]       # 7 byte
        # macAddress3 = data[66:80]       # 7 byte
        year = data[80:82]          # 1 byte
        month = data[82:84]         # 1 byte
        day = data[84:86]           # 1 byte
        hour = data[86:88]          # 1 byte
        minuts = data[88:90]        # 1 byte
        second = data[90:92]        # 1 byte
        week = data[92:94]          # 1 byte
        openHour = data[94:96]      # 1 byte
        openMinuts = data[96:98]    # 1 byte
        closeHour = data[98:100]     # 1 byte
        closeMinuts = data[100:102]   # 1 byte
        # crc16 = data[102:106]        # 2 byte

        # print(f"SN: {SN}")
        # print(f"commondType: {commondType}")
        # print(f"commondType: {strToInt(commondType)}")
        # print(f"speed: {speed}")
        # print(f"recordingCycle: {recordingCycle}")
        # print(f"uploadCycle: {uploadCycle}")
        # print(f"fixedTimeUpload: {fixedTimeUpload}")
        # print(f"uploadHour1: {uploadHour1}")
        # print(f"uploadMinute1: {uploadMinute1}")
        # print(f"crc16: {crc16}")

        '''
            {
                'cmd': 'getsetting', 
                'flag': '84B8', 
                'data': 'D27ECDAA030004050000000000000000000A0200FFFFFFFF000000000802000006020000FFFFFFFF150B090735280008001400E089'}
        '''

        # print(jsonify(request.values))
        print("")

        responseType = "05"  # 04 new
        flag = "0000"
        sn = SN
        commondType = commondType   # [00, 01, 02, 03]
        speed = "01"    # 00 low, 01 high
        recordingCycle = "00"   # [00, FF]
        uploadCycle = "00"  # [00, Other]
        fixTimeUpload = "00"  # 0 not use [0, 1-4]
        uploadHour1 = "00"
        uploadMinute1 = "00"
        uploadHour2 = "00"
        uploadMinute2 = "00"
        uploadHour3 = "00"
        uploadMinute3 = "00"
        uploadHour4 = "00"
        uploadMinute4 = "00"
        model = "00"    # 00 online, 01 stand-alone
        # 00 การนับไม่แสดงบนจอ, 01 แสดงการนับทิศทางเดียว, 02 แสดงการนับแบบทวิภาคี
        disableType = "00"
        macAddress1 = "00000000000000"
        macAddress2 = "00000000000000"
        macAddress3 = "00000000000000"
        year = year
        month = month
        day = day
        hour = hour
        minuts = minuts
        second = second
        week = week
        openHour = openHour
        openMinuts = openMinuts
        closeHour = closeHour
        closeMinuts = closeMinuts
        res1 = "00"
        res2 = "00"

        # print(f"SN: {sn}")
        # print(f"commondType: {commondType}")
        # print(f"year: {int(year, 16)}")
        # print(f"month: {int(month, 16)}")
        # print(f"day: {int(day, 16)}")
        # print(f"hour: {int(hour, 16)}")
        # print(f"minuts: {int(minuts, 16)}")
        # print(f"second: {int(second, 16)}")
        # print(f"week: {week}")
        # print(f"openHour: {openHour}")
        # print(f"openMinuts: {openMinuts}")
        # print(f"closeHour: {closeHour}")
        # print(f"closeMinuts: {closeMinuts}")

        hex_string = responseType + flag + sn + commondType + speed + recordingCycle + \
            uploadCycle + fixTimeUpload + uploadHour1 + uploadMinute1 + uploadHour2 + \
            uploadMinute2 + uploadHour3 + uploadMinute3 + uploadHour4 + uploadMinute4 + \
            model + disableType + macAddress1 + macAddress2 + macAddress3 + \
            year + month + day + hour + minuts + second + week + \
            openHour + openMinuts + closeHour + closeMinuts + res1 + res2

        result = hex_string + crc16Encode(hex_string)
        print(result)
        print(len(result))      # 56 + 2
        print("")

        # return jsonify({"result": result})
        return f"result={result}"
        # return {"result": result}


def checkLenHex(data):
    if len(data) == 1:
        data = "0" + data
    return data


def hexToIntCheckDigits(hex):
    an_integer = int(hex, 16)
    if len(str(an_integer)) == 1:
        an_integer = "0" + str(an_integer)
    return an_integer


def hexToInt(hex):
    an_integer = int(hex, 16)
    return an_integer


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
