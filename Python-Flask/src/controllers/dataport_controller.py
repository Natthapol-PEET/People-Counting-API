from datetime import datetime
from flask import request, abort
from threading import Thread

# config
from configs import config

# CRC-16/MODBUS
from utils.crc16 import crc16Encode
from utils.dataport import datetime_now, checkLenHex, hexToInt, \
                            hexToIntCheckDigits, convertSN, strToDatetime, \
                            strToTime, manageYear, checkDigitsHex

# model
from models.db import db
from models.getsetting import GetSetting
from models.getsetting_response import GetSettingResponse
from models.cache_data import CacheData
from models.cache_status import CacheStatus
from models.cache_response import CacheResponse
from models.device import Device
# from models.match import Match


remember = {
    "SN": {
        "DateTime": datetime.now()
    }
}


def dataport():
    try:
        cmd = request.values.to_dict()["cmd"]
        print(cmd)

        if cmd == "cache":
            result = cache(request.values.to_dict())

        if cmd == "getsetting":
            result = getsetting(request.values.to_dict())

        return f"result={result}"
    except:
        abort(404)


def cache(valuesDict):
    '''
        Area Enter  [in] ---> [out]
        Area Stay   [in] ---> [out]
    '''
    global remember
    
    status = valuesDict["status"]       # 24 + 4
    data = valuesDict["data"]           # 30 + 4

    crcStatus = checkDigitsHex(crc16Encode(status[0:24]).lower())
    # print(crcStatus)
    # print(status[24:28].lower())
    
    crcData = checkDigitsHex(crc16Encode(data[0:30]).lower())
    # print(crcData)
    # print(data[30:34].lower())

    if crcStatus != status[24:28].lower() or crcData != data[30:34].lower():
        result = cache_response("00")
        print("failed")
    else:
        print("success")
        # cache data
        year = data[0:2]
        month = data[2:4]
        day = data[4:6]
        hour = data[6:8]
        minuts = data[8:10]
        second = data[10:12]

        focus = hexToInt(data[12:14])
        dxIN1 = data[14:16]
        dxIN2 = data[16:18]
        dxIN3 = data[18:20]
        dxIN4 = data[20:22]
        dxIN = dxIN4 + dxIN3 + dxIN2 + dxIN1

        dxOUT1 = data[22:24]
        dxOUT2 = data[24:26]
        dxOUT3 = data[26:28]
        dxOUT4 = data[28:30]
        dxOUT = dxOUT4 + dxOUT3 + dxOUT2 + dxOUT1

        SN = status[4:12]
        year = manageYear(year)
        DateTime = strToDatetime(day, month, year, hour, minuts, second)

        inKey = remember.get(SN)
        if inKey is not None:
            dateTimeCheck = inKey.get("DateTime")

            if dateTimeCheck == DateTime:
                result = cache_response("01")
                return result

        print(f"datetime >> {DateTime}")
        print(f"dxIN {dxIN} >> {hexToInt(dxIN)}")
        print(f"dxOUT {dxOUT} >> {hexToInt(dxOUT)}")

        # update datetime -> SN
        t = {SN: {"DateTime": DateTime}}
        remember.update(t)

        # insert data to table cache_data
        cache_data = CacheData(valuesDict["flag"], DateTime, focus, hexToInt(dxIN), 
                                hexToInt(dxOUT), hexToInt(valuesDict["count"]), valuesDict["Tend"])
        db.session.add(cache_data)
        db.session.commit()

        # cache status
        version = status[0:4]       # 2 byte
        SN = status[4:12]           # 4 byte
        # 1 byte    [0x00 normal, 0x01 out of focus]
        focus = status[12:14]
        batterry_voltage1 = status[14:16]    # 2 byte
        batterry_voltage2 = status[16:18]
        batterry_voltage = batterry_voltage2 + batterry_voltage1
        voltage_percentage = status[18:20]   # 1 byte
        # 1 byte    [0x00 not charged, 0x02 beging charged]
        charge = status[20:22]
        res = status[22:24]         # 1 byte

        # insert data to table cache_status
        cache_status = CacheStatus(cache_data.Data_ID, version, convertSN(SN), hexToInt(focus), hexToInt(batterry_voltage),
                                    hexToInt(voltage_percentage), hexToInt(charge), res)
        db.session.add(cache_status)
        db.session.commit()

        # update counting by device
        th = Thread(target=update_counting, args=(SN, dxIN, dxOUT))
        th.start()
        
        # result = cache_response("01")
        result = cache_response("01", cache_data.Data_ID)

    return result


def update_counting(SN, dxIN, dxOUT):
    print(f"SN >> {convertSN(SN)}")

    # update table device
    device_query = Device.query.filter_by(SN=convertSN(SN)).first()
    
    if device_query is not None:
        device_query.In = device_query.In + hexToInt(dxIN)
        device_query.Out = device_query.Out + hexToInt(dxOUT)
        # device_query.Current = device_query.In - device_query.Out

        new_count = device_query.Current + (hexToInt(dxIN) - hexToInt(dxOUT))

        if new_count < 0:
            device_query.Current = 0
        else:
            device_query.Current = device_query.Current + (hexToInt(dxIN) - hexToInt(dxOUT))

        device_query.Update_DateTime = datetime.now()
        db.session.commit()

    print(f"update_counting >> {datetime.now()}")

    # Find Device All in Position
    device_all = Device.query.filter_by(SN=convertSN(SN)).all()

    count = 0
    Room_ID = ""
    for i in device_all:
        count += i.Current
        Room_ID = i.RoomKey

    # Query Room_ID in match
    # Room_ID = Match.query.filter_by(Position=device_query.Position).first()
    print(f'Room_ID >> {Room_ID}')

    # WebHook
    import requests
    requests.post(
                url='http://localhost:5000/people_counting/callback', 
                json={
                    "roomId": Room_ID,
                    "count": count,
                })


def cache_response(answerType, dataID=None):
    # ---------------- create dummy -> server response -------------------------
    answerType = answerType                       # 00 failed, 01 success
    flags = "0000"
    commandType = "03"                      # [01, 02, 03]
    year, month, day, hour, minuts, second, week = datetime_now()
    openHour = checkLenHex(hex(config.openHour)[2:])      # 8:00
    openMinuts = checkLenHex(hex(config.openMinute)[2:])
    closeHour = checkLenHex(hex(config.closeHour)[2:])    # 20:00
    closeMinuts = checkLenHex(hex(config.closeMinute)[2:])

    hex_string = answerType + flags + commandType + year + month + day + \
        hour + minuts + second + week + openHour + openMinuts + \
        closeHour + closeMinuts

    if dataID is not None:
        # insert data to table cache_response
        year = manageYear(year)
        datetime = strToDatetime(day, month, year, hour, minuts, second)
        openTime = strToTime(openHour, openMinuts)
        closeTime = strToTime(closeHour, closeMinuts)

        cache_response = CacheResponse(dataID, hexToInt(answerType), flags, hexToInt(commandType), datetime, 
                                        hexToInt(week), openTime, closeTime)
        db.session.add(cache_response)
        db.session.commit()

    return hex_string + crc16Encode(hex_string)


def getsetting(valuesDict):
    cmd = valuesDict["cmd"]
    flag = valuesDict["flag"]
    data = valuesDict["data"]

    SN = data[0:8]                  # 4 byte
    commandType = data[8:10]        # 1 byte
    speed = data[10:12]             # 1 byte
    recordingCycle = data[12:14]    # 1 byte
    uploadCycle = data[14:16]       # 1 byte
    fixedTimeUpload = data[16:18]   # 1 byte
    uploadHour1 = data[18:20]       # 1 byte
    uploadMinute1 = data[20:22]     # 1 byte
    uploadHour2 = data[22:24]       # 1 byte
    uploadMinute2 = data[24:26]     # 1 byte
    uploadHour3 = data[26:28]       # 1 byte
    uploadMinute3 = data[28:30]     # 1 byte
    uploadHour4 = data[30:32]       # 1 byte
    uploadMinute4 = data[32:34]     # 1 byte
    model = data[34:36]             # 1 byte
    disableType = data[36:38]       # 1 byte
    macAddress1 = data[38:52]       # 7 byte
    macAddress2 = data[52:66]       # 7 byte
    macAddress3 = data[66:80]       # 7 byte
    year = data[80:82]              # 1 byte
    month = data[82:84]             # 1 byte
    day = data[84:86]               # 1 byte
    hour = data[86:88]              # 1 byte
    minuts = data[88:90]            # 1 byte
    second = data[90:92]            # 1 byte
    week = data[92:94]              # 1 byte
    openHour = data[94:96]          # 1 byte
    openMinuts = data[96:98]        # 1 byte
    closeHour = data[98:100]        # 1 byte
    closeMinuts = data[100:102]     # 1 byte
    crc16 = data[102:106]           # 2 byte

    # insert or update data to getsetting table
    year = manageYear(year)
    date_time = strToDatetime(day, month, year, hour, minuts, second)
    openTime = strToTime(openHour, openMinuts)
    closeTime = strToTime(closeHour, closeMinuts)

    getsetting = GetSetting(flag, convertSN(SN),  hexToInt(commandType), hexToInt(speed), hexToInt(recordingCycle), 
                            hexToInt(uploadCycle), hexToInt(fixedTimeUpload), hexToInt(uploadHour1),
                            hexToInt(uploadMinute1), hexToInt(uploadHour2), hexToInt(uploadMinute2),
                            hexToInt(uploadHour3), hexToInt(uploadMinute3), hexToInt(uploadHour4), 
                            hexToInt(uploadMinute4), hexToInt(model), hexToInt(disableType), 
                            macAddress1, macAddress2, macAddress3, date_time, 
                            hexToInt(week), openTime, closeTime)

    # query getsetting
    setting = GetSetting.query.filter_by(SN=convertSN(SN)).first()

    if not setting:
        # insert
        db.session.add(getsetting)
        db.session.commit()
    else:
        # update
        getsetting.update(db, setting)

    # --------------------- create dummy -> server response -----------------------------
    responseType = "05"  # 04 new
    flag = "0000"
    sn = SN
    commandType = commandType   # [00, 01, 02, 03]
    speed = "01"                # 00 low, 01 high
    recordingCycle = "00"       # [00, FF]
    uploadCycle = "00"          # [00, Other]
    fixTimeUpload = "00"        # 0 not use [0, 1-4]
    uploadHour1 = "00"
    uploadMinute1 = "00"
    uploadHour2 = "00"
    uploadMinute2 = "00"
    uploadHour3 = "00"
    uploadMinute3 = "00"
    uploadHour4 = "00"
    uploadMinute4 = "00"
    model = "00"                # 00 online, 01 stand-alone
    # 00 การนับไม่แสดงบนจอ, 01 แสดงการนับทิศทางเดียว, 02 แสดงการนับแบบทวิภาคี
    disableType = "02"
    macAddress1 = "00000000000000"
    macAddress2 = "00000000000000"
    macAddress3 = "00000000000000"
    year, month, day, hour, minuts, second, week = datetime_now()
    openHour = checkLenHex(hex(config.openHour)[2:])      # 8:00
    openMinuts = checkLenHex(hex(config.openMinute)[2:])
    closeHour = checkLenHex(hex(config.closeHour)[2:])    # 20
    closeMinuts = checkLenHex(hex(config.closeMinute)[2:])
    res1 = "00"
    res2 = "00"

    hex_string = responseType + flag + sn + commandType + speed + recordingCycle + \
        uploadCycle + fixTimeUpload + uploadHour1 + uploadMinute1 + uploadHour2 + \
        uploadMinute2 + uploadHour3 + uploadMinute3 + uploadHour4 + uploadMinute4 + \
        model + disableType + macAddress1 + macAddress2 + macAddress3 + \
        year + month + day + hour + minuts + second + week + \
        openHour + openMinuts + closeHour + closeMinuts + res1 + res2

    result = hex_string + crc16Encode(hex_string)

    # insert or update data to getsetting_response table
    year = manageYear(year)
    date_time = strToDatetime(day, month, year, hour, minuts, second)
    openTime = strToTime(openHour, openMinuts)
    closeTime = strToTime(closeHour, closeMinuts)

    getsetting_response = GetSettingResponse(setting.Getsetting_ID, hexToInt(responseType), flag, 
                                            convertSN(sn), hexToInt(commandType), hexToInt(speed), 
                                            hexToInt(recordingCycle), hexToInt(uploadCycle), hexToInt(fixedTimeUpload), 
                                            hexToInt(uploadHour1), hexToInt(uploadMinute1), hexToInt(uploadHour2), 
                                            hexToInt(uploadMinute2), hexToInt(uploadHour3), hexToInt(uploadMinute3), 
                                            hexToInt(uploadHour4), hexToInt(uploadMinute4), hexToInt(model), hexToInt(disableType), 
                                            macAddress1, macAddress2, macAddress3, date_time, openTime, closeTime, res1, res2)

    # query getsetting -> check is have in db
    setting_response = GetSettingResponse.query.filter_by(SN=convertSN(SN)).first()

    if not setting_response:
        # insert
        db.session.add(getsetting_response)
        db.session.commit()
    else:
        # update
        getsetting_response.update(db, setting, setting.Getsetting_ID)

    return result
