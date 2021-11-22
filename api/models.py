from app import db
import json


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=False, nullable=False)
    encoding = db.Column(db.LargeBinary, unique=False, nullable=False)

    def __repr__(self):
        return str({
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "encoding": self.encoding
        })
