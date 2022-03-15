from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from datetime import datetime, time
from sqlalchemy import func
import requests

# model
from models.db import db
from models.summary import Summary
from models.device import Device

# config
from configs import config


def read_room_api():
    url = config.current_counting_api
    response = requests.get(url)
    print(f"read_room_api: {response.status_code}")

    if response.status_code == 200:
        return response.json()
    else:
        return []


def summaryManage(now):
    data = db.session.query(Device.RoomName,
                            func.sum(Device.In),
                            func.sum(Device.Out),
                            func.sum(Device.Current)) \
        .group_by(Device.RoomName).all()

    # insert data to table summary
    summary = Summary(data[0][0], now, data[0][1], data[0][2], data[0][3])
    db.session.add(summary)
    db.session.commit()


def clearSqlite(now):
    deviceAll = Device.query.all()

    for device in deviceAll:
        # clear In, Out and Current in table device
        device.In = 0
        device.Out = 0
        device.Current = 0
        device.Update_DateTime = now
        db.session.commit()


def clearAPI():
    rooms = Device.query.all()

    for room in rooms:
        # print(f"RoomKey: {room.RoomKey}")

        # WebHook
        import requests
        requests.post(
            url='http://localhost:5000/people_counting/callback',
            json={
                "roomId": room.RoomKey,
                "count": 0,
            })


def clearTableInDatabase():
    try:
        del_cache_data = db.session.execute(
            "DELETE FROM cache_data WHERE Create_DateTime <= date('now','-1 day')")
        del_cache_response = db.session.execute(
            "DELETE FROM cache_response WHERE Create_DateTime <= date('now','-1 day')")
        del_cache_status = db.session.execute(
            "DELETE FROM cache_status WHERE Create_DateTime <= date('now','-1 day')")
        del_summary = db.session.execute(
            "DELETE FROM summary WHERE DateTime <= date('now','-10 day')")
    except:
        pass


def syncDataTableRoom():
    device = Device.query.all()
    rooms = read_room_api()

    for room in rooms:
        for i in device:
            # print(i.RoomKey)
            # print(room['room_name'])
            if i.RoomKey == room['id']:
                # print("update")
                i.RoomName = room['room_name']
                i.OpenTime = room['opened']
                i.closeTime = room['closed']
                db.session.commit()


def time_in_range(start, end, current):
    """Returns whether current is in the range [start, end]"""
    return start <= current <= end


def historyToStrapiEveryOneHour(now, hour):
    ''' 
    -- Format Data

    roomKeyData = {
        RoomKey1: {
            dxIN: 1,
            dxOUT: 1,
        }
    }
    '''

    date = now.date()
    startDateTime = f"{date} {hour}:00"
    # print(f"startDateTime: {startDateTime}")

    stopDateTime = f"{date} {int(hour) + 1}:00"
    # print(f"stopDateTime: {stopDateTime}")

    day = date.strftime('%A')  # => Tuesday
    # print(f"day: {day}")

    sql = f'''
        SELECT d.RoomKey, 
        d.SN, 
        IFNULL(ds.DxIN, 0) as dxIN, 
        IFNULL(ds.DxOUT, 0) as dxOUT, 
        IFNULL(ds.Count, 0) as dxCOUNT,
        ds.Datetime,
        d.OpenTime,
        d.CloseTime
            FROM device AS d
            LEFT JOIN 
            (
                SELECT cs.Device_SN, cd.DxIN, cd.DxOUT, cd.Count, cd.Datetime
                FROM cache_status AS cs
                LEFT JOIN cache_data AS cd
                    ON cs.Data_ID = cd.Data_ID
            ) ds
            ON d.SN = ds.Device_SN
            WHERE ds.Datetime BETWEEN '{startDateTime}' AND '{stopDateTime}'
            -- WHERE ds.Datetime BETWEEN '2021-11-12 02:00' AND '2021-11-12 03:00'
                OR ds.Datetime IS NULL
            ORDER BY d.RoomKey ASC;
    '''
    data = db.session.execute(sql)

    roomKeyData = {}

    for d in data:
        # print(d.RoomKey, d.SN, d.dxIN, d.dxOUT, d.dxCOUNT, d.Datetime)
        if d.RoomKey not in roomKeyData:
            if d.Datetime is None:
                roomKeyData[d.RoomKey] = {
                    "dxIN": 0,
                    "dxOUT": 0,
                    "opened": d.OpenTime,
                    "closed": d.CloseTime,
                }
            else:
                roomKeyData[d.RoomKey] = {
                    "dxIN": d.dxIN,
                    "dxOUT": d.dxOUT,
                    "opened": d.OpenTime,
                    "closed": d.CloseTime,
                }
        else:
            if d.Datetime is None:
                roomKeyData[d.RoomKey] = {
                    "dxIN": roomKeyData[d.RoomKey]["dxIN"] + 0,
                    "dxOUT": roomKeyData[d.RoomKey]["dxOUT"] + 0,
                }
            else:
                roomKeyData[d.RoomKey] = {
                    "dxIN": roomKeyData[d.RoomKey]["dxIN"] + d.dxIN,
                    "dxOUT": roomKeyData[d.RoomKey]["dxOUT"] + d.dxOUT,
                }

    # print(f"roomKeyData: {roomKeyData}")
    # print()

    # ------- Send History API ----------
    for room in roomKeyData:
        opened = roomKeyData[room]['opened'].split(":")
        openedHour = int(opened[0])
        openedMinute = int(opened[2].split(".")[0])
        # print(openedHour, openedMinute)

        closed = roomKeyData[room]['closed'].split(":")
        closedHout = int(closed[0])
        closedMinute = int(closed[1].split(".")[0])
        # print(closedHout, closedMinute)

        start = time(openedHour, openedMinute, 0)
        # print(f"start: {start}")

        end = time(closedHout, closedMinute, 0)
        # print(f"end: {end}")

        current = datetime.now().time()
        # print(f"current: {current}")

        if time_in_range(start, end, current):
            # call api
            url = config.occupation_history_api

            body = {
                "time": str(current).split(".")[0],
                "day": day,
                "in_count": roomKeyData[room]["dxIN"],
                "out_count": roomKeyData[room]["dxOUT"],
                "occupation": room
            }

            response = requests.post(url, json=body)
            print(f"post history: {response.status_code}")


def print_date_time():
    now = datetime.now()
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    print(f"minute: {minute}")

    # ทุก ๆ เที่ยงคืน
    if hour == config.hour_interval and int(minute) == 0:
        # ---------- Summary Data of Date ----------------
        summaryManage(now)
        print("summaryManage")

        # ---------- Clear Sqlite ----------------
        # query data in table device
        clearSqlite(now)
        print("clearSqlite")

        # --------- Clear API --------------
        # Find Device All in Position
        clearAPI()
        print("clearAPI")

        # ------- clear data in database.sqlite3 ---------------
        clearTableInDatabase()
        print("clearTableInDatabase")

        # ------- sync openTime, CloseTime and RoomName --------------
        syncDataTableRoom()
        print("syncDataTableRoom")

    # -------- ส่งข้อมูล history to strapi ทุก ๆ 1 ชั่วโมง ------------------
    if int(minute) == 1:
        historyToStrapiEveryOneHour(now, hour)


def init():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_date_time,
                        trigger="interval", minutes=1)     # minutes
                    #   trigger="interval", seconds=10)        # seconds
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
