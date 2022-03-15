from models.db import db
from datetime import datetime

class Device(db.Model):
    __tablename__ = 'device'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SN = db.Column(db.String, unique=True)
    RoomKey = db.Column(db.String)
    RoomName = db.Column(db.String)
    OpenTime = db.Column(db.String)
    CloseTime = db.Column(db.String)
    In = db.Column(db.Integer, default=0)
    Out = db.Column(db.Integer, default=0)
    Current = db.Column(db.Integer, default=0)
    Create_DateTime = db.Column(db.DateTime, default=datetime.now())
    Update_DateTime = db.Column(db.DateTime)

    def __init__(self, SN, RoomKey, RoomName, OpenTime, CloseTime):
        self.SN = SN
        self.RoomKey = RoomKey
        self.RoomName = RoomName
        self.OpenTime = OpenTime
        self.CloseTime = CloseTime

    @property
    def serialize(self):
        return {
            'id': self.ID,
            'SN': self.SN,
            'RoomName': self.RoomName,
            'RoomKey': self.RoomKey,
            'OpenTime': self.OpenTime,
            'CloseTime': self.CloseTime,
            'In': self.In,
            'Out': self.Out,
            'Current': self.Current,
            'Create_DateTime': self.Create_DateTime,
            'Update_DateTime': self.Update_DateTime,
        }
