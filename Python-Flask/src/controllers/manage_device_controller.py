from datetime import datetime
from urllib import response
from flask import jsonify, request, render_template, redirect
import requests

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, update, delete, values
from models.device import Device
# from models.match import Match

# auth
from auth.basic_authy import basic_auth

# config
from configs import config

db = SQLAlchemy()


# @basic_auth.login_required
# def register_device():
#     sn = request.json["SN"]
#     position = request.json["Position"]

#     if Device.query.filter_by(SN=sn).first() is not None:
#         return jsonify({"message": "already have this information."})

#     # insert
#     device = Device(sn, position)
#     db.session.add(device)
#     db.session.commit()

#     return jsonify({"message": "register successful."})


# @basic_auth.login_required
def delete_device(id):
    # sql = delete(Device).where(Device.ID == id)
    # db.session.execute(sql)

    db.session.query(Device).filter_by(ID=id).delete()
    db.session.commit()

    return redirect("/manage_device/show_device", code=302)
    # return jsonify({"message": "delete device successful."})


def read_camera():
    return [i.serialize for i in Device.query.all()]

# def read_match():
#     return [i.serialize for i in Match.query.all()]


def read_room_api():
    url = config.current_counting_api
    response = requests.get(url)
    print(f"status code: {response.status_code}")
    # print(f"data: {response.json()}")

    # for data in response.json():
    #     print(data["room_name"])
    #     print(data["id"])
    #     print(data["opened"])
    #     print(data["closed"])
    #     print()

    if response.status_code == 200:
        return response.json()
    else:
        return []


@basic_auth.login_required
def show_device():
    rooms = read_room_api()

    if request.method == 'POST':
        SN = request.form['SN']
        RoomKey = request.form['RoomKey']
        print(f'SN: {SN}')
        print(f'RoomKey: {RoomKey}')

        for room in rooms:
            if room['id'] == RoomKey:
                device = Device(
                    SN=SN, RoomKey=RoomKey, RoomName=room['room_name'], OpenTime=room['opened'], CloseTime=room['closed'])
                try:
                    db.session.add(device)
                    db.session.commit()
                    db.session.refresh(device)
                except:
                    pass
    # return render_template('manage_device/show_device.html', devices=read_camera(), matchs=read_match())
    return render_template('manage_device/show_device.html', devices=read_camera(), rooms=rooms)


# @basic_auth.login_required
# def edit_device():
#     # sn = request.json["SN"]
#     # Position = request.json["Position"]

#     # device = Device.query.filter_by(SN=sn).first()
#     # if device is not None:
#     #     device.Position = Position
#     #     db.session.commit()

#     # return jsonify(device.serialize)

#     return render_template('manage_device/show_device.html', devices=[i.serialize for i in Device.query.all()])


# @basic_auth.login_required
# def register_match_device():
#     Room = request.json["Room"]
#     Room_ID = request.json["Room_ID"]

#     # if Match.query.filter_by(Room_ID=Room_ID).first() is not None:
#     #     return jsonify({"message": "already have this information."})

#     # insert
#     # match = Match(Room, Room_ID)
#     # db.session.add(match)
#     # db.session.commit()

#     return jsonify({"message": "register successful."})


# @basic_auth.login_required
# def show_match_device():
#     # return jsonify([i.serialize for i in Match.query.all()])
#     return []


# @basic_auth.login_required
# def edit_match_device():
#     Room = request.json["Room"]
#     Room_ID = request.json["Room_ID"]

#     # match = Match.query.filter_by(Room_ID=Room_ID).first()

#     # print(match)

#     # if match is not None:
#     #     match.Position = Room
#     #     db.session.commit()
#     #     return jsonify(match.serialize)

#     return jsonify({'message': 'no match'})


# @basic_auth.login_required
# def delete_match_device(id):
#     # sql = delete(Match).where(Match.Match_ID == id)
#     # db.session.execute(sql)
#     # db.session.commit()

#     return jsonify({"message": "delete device successful."})
