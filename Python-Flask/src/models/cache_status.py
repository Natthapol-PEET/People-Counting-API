from models.db import db
from datetime import datetime


class CacheStatus(db.Model):
    __tablename__ = 'cache_status'
    Status_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Data_ID = db.Column(db.Integer, db.ForeignKey('cache_status.Data_ID'))
    Version = db.Column(db.String)
    Device_SN = db.Column(db.String)
    Focus = db.Column(db.Integer)
    Batterry_Voltage = db.Column(db.Integer)
    Voltage_Percentage = db.Column(db.Integer)
    Charge = db.Column(db.Integer)
    Res = db.Column(db.String)
    Create_DateTime = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, Data_ID, Version, Device_SN, Focus, Batterry_Voltage, Voltage_Percentage, Charge, Res):
        self.Data_ID = Data_ID
        self.Version = Version
        self.Device_SN = Device_SN
        self.Focus = Focus
        self.Batterry_Voltage = Batterry_Voltage
        self.Voltage_Percentage = Voltage_Percentage
        self.Charge = Charge
        self.Res = Res
        Create_DateTime = datetime.now()

