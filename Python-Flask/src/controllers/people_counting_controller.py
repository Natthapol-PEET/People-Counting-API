import requests
import threading
from flask import request, jsonify, abort

# auth
from auth.auth_token import auth_token

# model
from models.db import db
from models.device import Device
from models.summary import Summary

# config
from configs import config


@auth_token.login_required
def index():
    return jsonify({
        "message": "people counting"
    })


@auth_token.login_required
def counting():
    return jsonify([i.serialize for i in Device.query.all()])


@auth_token.login_required
def counting_by_id(id):
    device_query = Device.query.filter_by(ID=id).first()

    if device_query is None:
        return jsonify({})

    return jsonify(device_query.serialize)


@auth_token.login_required
def counting_by_area(area):
    SN = []
    In = 0
    Out = 0

    # query where area
    device_query = Device.query.filter_by(Position=area).all()

    # area not found
    if device_query is None:
        abort(404, "Area Not Found")

    # calculate In, Out, Current in Area
    for device in device_query:
        SN.append({
            "Id": device.ID,
            "SN": device.SN,
            "Create_By": device.Create_DateTime,
            "Update_By": device.Update_DateTime,
        })
        In = In + device.In
        Out = Out + device.Out

    return jsonify({
        "Area": area,
        "SN_List": SN,
        "In": In,
        "Out": Out,
        "Current": In - Out,
    })


@auth_token.login_required
def summary():
    return jsonify([i.serialize for i in Summary.query.all()])


def test():
    from sqlalchemy import func

    # -------------------- Sum Data ---------------------------------------------------------
    # data = db.session.query(Device.Position,
    #                         func.sum(Device.In),
    #                         func.sum(Device.Out),
    #                         func.sum(Device.Current)) \
    #                     .group_by(Device.Position).all()

    # for i in data:
    #     print(f"Position >> {i[0]}")
    #     print(f"In >> {i[1]}")
    #     print(f"Out >> {i[2]}")
    #     print(f"Current >> {i[3]}")
    #     print()

    # ------------------------ Clear data in Sqlite ---------------------------------------------
    # try:
    #     del_cache_data = db.session.execute("DELETE FROM cache_data WHERE Create_DateTime <= date('now','-1 day')")
    #     del_cache_response = db.session.execute("DELETE FROM cache_response WHERE Create_DateTime <= date('now','-1 day')")
    #     del_cache_status = db.session.execute("DELETE FROM cache_status WHERE Create_DateTime <= date('now','-1 day')")
    #     del_summary = db.session.execute("DELETE FROM summary WHERE DateTime <= date('now','-10 day')")
    # except:
    #     pass

    return jsonify({})


items = []
forever = False


def callback():
    global items, forever

    roomId = request.json['roomId']
    count = request.json['count']

    items.append({
        'roomId': roomId,
        'count': count,
    })

    # print(f"items: {items}")
    consumer = threading.Thread(target=consume)

    if not forever:
        forever = True
        consumer.start()

    return jsonify({'message': 'successful'})


def consume():
    global items, forever

    # print(f"items[0] >> {items[0]}")
    # print(f"roomId >> {items[0]['roomId']}")
    # print(f"count >> {items[0]['count']}")

    while forever:
        if items:
            url = f"{config.current_counting_api}/{items[0]['roomId']}"

            try:
                response = requests.put(url, json={
                                    "current_people": items[0]['count']})
                # print(f'response >> {response.json()}')

                if response.status_code == 200 and items:
                    items.pop(0)
            except:
                pass
        else:
            forever = False
            # print("items: No Items")

        # print("items: " + str(len(items)))
