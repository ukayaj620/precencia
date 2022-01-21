from flask_login import UserMixin

from app import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    user = db.relationship('User', back_populates='role', uselist=False)

    def __repr__(self):
        return str({
            "id": self.id,
            "name": self.name
        })


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=False, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'role.id', ondelete='CASCADE'), unique=False, nullable=False)
    attendance = db.relationship(
        'Attendance', back_populates='user', lazy=True)
    role = db.relationship('Role', back_populates='user', lazy=True)
    encoding = db.relationship(
        'Encoding', back_populates='user', uselist=False)

    def __repr__(self):
        return str({
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role.name
        })


class Encoding(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), unique=True, nullable=False)
    vector = db.Column(db.LargeBinary, unique=False, nullable=True)
    user = db.relationship('User', back_populates='encoding', lazy=True)

    def __repr__(self):
        return str({
            "id": self.id,
            "vector": self.vector,
            "name": self.user.name
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
