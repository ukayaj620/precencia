from api.models import Role
from app import db


class RoleController:

    def __init__(self):
        self.role_model = Role()

    def fetch_by_name(self, name):
        return self.role_model.query.filter_by(name=name).first()

    def create(self, name):
        db.session.add(Role(
            name=name
        ))
        db.session.commit()
