from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=False, nullable=False)
    encoding = db.Column(db.LargeBinary, unique=False, nullable=False)
    attendance = db.relationship('Attendance', back_populates='user', lazy=True)

    def __repr__(self):
        return str({
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "encoding": self.encoding
        })


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), unique=False, nullable=False)
    attendance_date = db.Column(db.Date, nullable=False)
    check_in_time = db.Column(db.DateTime, nullable=False)
    check_out_time = db.Column(db.DateTime, nullable=True)
    user = db.relationship('User', back_populates='attendance', lazy=True)

    def __repr__(self) -> str:
        return str({
            "id": self.id,
            "user": self.user_id,
            "attendance_date": self.attendance_date,
            "check_in_time": self.check_in_time,
            "check_out_time": self.check_out_time,
        })
