from datetime import datetime
from models.db import db


class CacheData(db.Model):
    __tablename__ = 'cache_data'
    Data_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Flag = db.Column(db.String)
    DateTime = db.Column(db.DateTime)
    Focus = db.Column(db.Integer)
    DxIN = db.Column(db.Integer)
    DxOUT = db.Column(db.Integer)
    Count = db.Column(db.Integer)
    Tend = db.Column(db.String)
    Create_DateTime = db.Column(db.DateTime)

    def __init__(self, Flag, DateTime, Focus, DxIN, DxOUT, Count, Tend):
        self.Flag = Flag
        self.DateTime = DateTime
        self.Focus = Focus
        self.DxIN = DxIN
        self.DxOUT = DxOUT
        self.Count = Count
        self.Tend = Tend
        self.Create_DateTime = datetime.now()

    # @property
    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'city': self.city,
    #         'state': self.state,
    #         'address': self.address
    #     }
