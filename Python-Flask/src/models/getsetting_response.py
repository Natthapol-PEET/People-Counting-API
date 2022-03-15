from models.db import db
from datetime import datetime


class GetSettingResponse(db.Model):
    __tablename__ = 'getsetting_response'
    Response_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Getsetting_ID = db.Column(db.Integer, db.ForeignKey('getsetting.Getsetting_ID'))
    Responding_Type = db.Column(db.Integer)
    Flag = db.Column(db.String)
    SN = db.Column(db.String, unique=True)
    Command_Type = db.Column(db.Integer)
    Speed = db.Column(db.Integer)
    Recording_Cycle = db.Column(db.Integer)
    Upload_Cycle = db.Column(db.Integer)
    Fixed_Time_Upload = db.Column(db.Integer)
    Upload_Hour_1 = db.Column(db.Integer)
    Upload_Minute_1 = db.Column(db.Integer)
    Upload_Hour_2 = db.Column(db.Integer)
    Upload_Minute_2 = db.Column(db.Integer)
    Upload_Minute_3 = db.Column(db.Integer)
    Upload_Hour_3 = db.Column(db.Integer)
    Upload_Hour_4 = db.Column(db.Integer)
    Upload_Minute_4 = db.Column(db.Integer)
    Model = db.Column(db.Integer)
    Disable_Type = db.Column(db.Integer)
    Mac_Address_1 = db.Column(db.String)
    Mac_Address_2 = db.Column(db.String)
    Mac_Address_3 = db.Column(db.String)
    DateTime = db.Column(db.DateTime)
    OpenTime = db.Column(db.Time)
    CloseTime = db.Column(db.Time)
    Res_1 = db.Column(db.String)
    Res_2 = db.Column(db.String)
    Create_DateTime = db.Column(db.DateTime, default=datetime.now())
    Update_DateTime = db.Column(db.DateTime)

    def __init__(self, Getsetting_ID, Responding_Type, Flag, SN, Command_Type, Speed, Recording_Cycle, Upload_Cycle, Fixed_Time_Upload, Upload_Hour_1,
                 Upload_Minute_1, Upload_Hour_2, Upload_Minute_2, Upload_Hour_3, Upload_Minute_3, Upload_Hour_4, Upload_Minute_4,
                 Model, Disable_Type, Mac_Address_1, Mac_Address_2, Mac_Address_3, DateTime, OpenTime, CloseTime, Res_1, Res_2):

        self.Getsetting_ID = Getsetting_ID
        self.Responding_Type = Responding_Type
        self.Flag = Flag
        self.SN = SN
        self.Command_Type = Command_Type
        self.Speed = Speed
        self.Recording_Cycle = Recording_Cycle
        self.Upload_Cycle = Upload_Cycle
        self.Fixed_Time_Upload = Fixed_Time_Upload
        self.Upload_Hour_1 = Upload_Hour_1
        self.Upload_Minute_1 = Upload_Minute_1
        self.Upload_Hour_2 = Upload_Hour_2
        self.Upload_Minute_2 = Upload_Minute_2
        self.Upload_Hour_3 = Upload_Hour_3
        self.Upload_Minute_3 = Upload_Minute_3
        self.Upload_Hour_4 = Upload_Hour_4
        self.Upload_Minute_4 = Upload_Minute_4
        self.Model = Model
        self.Disable_Type = Disable_Type
        self.Mac_Address_1 = Mac_Address_1
        self.Mac_Address_2 = Mac_Address_2
        self.Mac_Address_3 = Mac_Address_3
        self.DateTime = DateTime
        self.OpenTime = OpenTime
        self.Res_1 = Res_1
        self.Res_2 = Res_2
        self.CloseTime = CloseTime
        self.Update_DateTime = datetime.now()


    def update(self, db, str, id):
        self.Getsetting_ID = id
        str.Responding_Type = self.Responding_Type
        str.Flag = self.Flag
        str.Command_Type = self.Command_Type
        str.Speed = self.Speed
        str.Recording_Cycle = self.Recording_Cycle
        str.Upload_Cycle = self.Upload_Cycle
        str.Fixed_Time_Upload = self.Fixed_Time_Upload
        str.Upload_Hour_1 = self.Upload_Hour_1
        str.Upload_Minute_1 = self.Upload_Minute_1
        str.Upload_Hour_2 = self.Upload_Hour_2
        str.Upload_Minute_2 = self.Upload_Minute_2
        str.Upload_Hour_3 = self.Upload_Hour_3
        str.Upload_Minute_3 = self.Upload_Minute_3
        str.Upload_Hour_4 = self.Upload_Hour_4
        str.Upload_Minute_4 = self.Upload_Minute_4
        str.Model = self.Model
        str.Disable_Type = self.Disable_Type
        str.Mac_Address_1 = self.Mac_Address_1
        str.Mac_Address_2 = self.Mac_Address_2
        str.Mac_Address_3 = self.Mac_Address_3
        str.DateTime = self.DateTime
        str.OpenTime = self.OpenTime
        str.CloseTime = self.CloseTime
        str.Res_1 = self.Res_1
        str.Res_2 = self.Res_2
        str.Update_DateTime = self.Update_DateTime

        db.session.commit()
        

        