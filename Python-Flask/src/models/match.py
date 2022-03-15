# from models.db import db
# from datetime import datetime

# class Match(db.Model):
#     __tablename__ = 'match'
#     Match_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     Position = db.Column(db.String)
#     Room_ID = db.Column(db.String)
#     Open_Time = db.Column(db.String)
#     Close_Time = db.Column(db.String)
#     Create_DateTime = db.Column(db.DateTime, default=datetime.now())
#     Update_DateTime = db.Column(db.DateTime)

#     def __init__(self, Position, Room_ID):
#         self.Position = Position
#         self.Room_ID = Room_ID
#         self.Update_DateTime = datetime.now()

#     @property
#     def serialize(self):
#         return {
#             'Match_ID': self.Match_ID,
#             'Position': self.Position,
#             'Room_ID': self.Room_ID,
#             'Create_DateTime': self.Create_DateTime,
#             'Update_DateTime': self.Update_DateTime,
#         }


