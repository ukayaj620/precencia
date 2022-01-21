from flask import Blueprint, flash, url_for, render_template, request, redirect
from werkzeug.security import check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from datetime import timedelta

from api.controllers.user import UserController
from api.controllers.role import RoleController
from api.controllers.attendance import AttendanceController


admin = Blueprint('admin', __name__, template_folder='templates')

user_controller = UserController()
role_controller = RoleController()
attendance_controller = AttendanceController()

@admin.route('/', methods=['GET'])
@login_required
def index():
    attendance_list = attendance_controller.fetch_all()
    return render_template('admin/index.html', attendance_list=attendance_list)


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    if request.method == 'POST':
        payload = request.form
        user = user_controller.fetch_by_email(payload['email'])
        remember = True if payload.get('remember') is not None else False
        
        if not user:
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('admin.login'))
        
        if not check_password_hash(user.password, payload['password']):
            flash('Please check your login details and try again.', 'danger')
            return redirect(url_for('admin.login'))
        
        login_user(user, remember=remember, duration=timedelta(days=30))
        return redirect(url_for('admin.index')) 

    return render_template('admin/login.html')

