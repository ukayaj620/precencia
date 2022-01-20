from werkzeug.security import generate_password_hash

from api.models import User, Encoding
from app import db


class UserController:

    def __init__(self):
        self.user_model = User()

    def fetch_all(self):
        return self.user_model.query.all()

    def fetch_by_id(self, id):
        return self.user_model.query.get(int(id))
    
    def fetch_by_role(self, role):
        return self.user_model.query.filter_by(role_id=role.id).all()

    def fetch_by_email(self, email):
        return self.user_model.query.filter_by(email=email).first()

    def create(self, name, email, role_id, password=None):
        password_value = generate_password_hash(
            password) if password is not None else None
        user = User(
            name=name,
            email=email,
            role_id=role_id,
            password=password_value
        )
        db.session.add(user)
        db.session.flush()
        db.session.commit()

        encoding = Encoding(
            user_id=user.id,
            vector=None
        )
        db.session.add(encoding)
        db.session.commit()
    
    def update(self, user_id, name, email):
        user = self.fetch_by_id(id=user_id)
        user.name = name
        user.email = email
        db.session.commit()

        return user
    
    def delete(self, user_id):
        user = self.fetch_by_id(id=user_id)
        db.session.delete(user.encoding)
        db.session.delete(user)
        db.session.commit()

        return user

    def update_face_embedding(self, user_id, embedding):
        user = self.fetch_by_id(user_id)
        user.encoding.vector = embedding
        db.session.commit()
