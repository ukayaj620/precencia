from api.models import Attendance
from app import db


class AttendanceController:

    def __init__(self):
        self.attendance_model = Attendance()

    def fetch_all(self):
        return self.attendance_model.query.all()

    def fetch_user_today_attendance(self, user_id, time):
        return self.attendance_model.query.filter_by(
            user_id=user_id, attendance_date=time.date()).first()

    def check_in(self, user_id, time):
        db.session.add(Attendance(
            user_id=user_id,
            attendance_date=time.date(),
            check_in_time=time
        ))
        db.session.commit()

    def check_out(self, user_id, time):
        user_attendance = self.fetch_user_today_attendance(
            user_id=user_id, time=time)
        user_attendance.check_out_time = time
        db.session.commit()
