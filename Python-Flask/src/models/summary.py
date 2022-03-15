from models.db import db

class Summary(db.Model):
    __tablename__ = 'summary'
    Sum_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Position = db.Column(db.String, db.ForeignKey('device.SN'))
    DateTime = db.Column(db.DateTime)
    In = db.Column(db.Integer, default=0)
    Out = db.Column(db.Integer, default=0)
    Current = db.Column(db.Integer, default=0)

    def __init__(self, Position, DateTime, In, Out, Current):
        self.Position = Position
        self.DateTime = DateTime
        self.In = In
        self.Out = Out
        self.Current = Current

    @property
    def serialize(self):
        return {
            'id': self.Sum_ID,
            'Position': self.Position,
            'DateTime': self.DateTime,
            'In': self.In,
            'Out': self.Out,
            'Current': self.Current,
        }


