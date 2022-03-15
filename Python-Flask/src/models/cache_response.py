from datetime import datetime
from models.db import db

class CacheResponse(db.Model):
    __tablename__ = 'cache_response'
    Response_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Data_ID = db.Column(db.Integer, db.ForeignKey('cache_data.Data_ID'))
    Answer_Type = db.Column(db.Integer)
    Flag = db.Column(db.Integer)
    Command_Type = db.Column(db.Integer)
    DateTime = db.Column(db.Integer)
    Week = db.Column(db.Integer)
    Open_Time = db.Column(db.Time)
    Close_Time = db.Column(db.Time)
    Create_DateTime = db.Column(db.DateTime)

    def __init__(self, Data_ID, Answer_Type, Flag, Command_Type, DateTime, Week, Open_Time, Close_Time):
        self.Data_ID = Data_ID
        self.Answer_Type = Answer_Type
        self.Flag = Flag
        self.Command_Type = Command_Type
        self.DateTime = DateTime
        self.Week = Week
        self.Open_Time = Open_Time
        self.Close_Time = Close_Time
        self.Create_DateTime = datetime.now()

        