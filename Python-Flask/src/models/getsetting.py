from models.db import db
from datetime import datetime


class GetSetting(db.Model):
    __tablename__ = 'getsetting'
    Getsetting_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    Week = db.Column(db.Integer)
    OpenTime = db.Column(db.Time)
    CloseTime = db.Column(db.Time)
    Create_DateTime = db.Column(db.DateTime, default=datetime.now())
    Update_DateTime = db.Column(db.DateTime)

    def __init__(self, Flag, SN, Command_Type, Speed, Recording_Cycle, Upload_Cycle, Fixed_Time_Upload, Upload_Hour_1,
                 Upload_Minute_1, Upload_Hour_2, Upload_Minute_2, Upload_Hour_3, Upload_Minute_3, Upload_Hour_4, Upload_Minute_4,
                 Model, Disable_Type, Mac_Address_1, Mac_Address_2, Mac_Address_3, DateTime, Week, OpenTime, CloseTime):

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
        self.Week = Week
        self.OpenTime = OpenTime
        self.CloseTime = CloseTime
        self.Update_DateTime = datetime.now()


    def update(self, db, st):
        st.Flag = self.Flag
        st.Command_Type = self.Command_Type
        st.Speed = self.Speed
        st.Recording_Cycle = self.Recording_Cycle
        st.Upload_Cycle = self.Upload_Cycle
        st.Fixed_Time_Upload = self.Fixed_Time_Upload
        st.Upload_Hour_1 = self.Upload_Hour_1
        st.Upload_Minute_1 = self.Upload_Minute_1
        st.Upload_Hour_2 = self.Upload_Hour_2
        st.Upload_Minute_2 = self.Upload_Minute_2
        st.Upload_Hour_3 = self.Upload_Hour_3
        st.Upload_Minute_3 = self.Upload_Minute_3
        st.Upload_Hour_4 = self.Upload_Hour_4
        st.Upload_Minute_4 = self.Upload_Minute_4
        st.Model = self.Model
        st.Disable_Type = self.Disable_Type
        st.Mac_Address_1 = self.Mac_Address_1
        st.Mac_Address_2 = self.Mac_Address_2
        st.Mac_Address_3 = self.Mac_Address_3
        st.DateTime = self.DateTime
        st.Week = self.Week
        st.OpenTime = self.OpenTime
        st.CloseTime = self.CloseTime
        st.Update_DateTime = self.Update_DateTime

        db.session.commit()

        