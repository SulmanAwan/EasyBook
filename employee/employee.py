from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_db_connection

employee = Blueprint('employee', __name__, template_folder='templates', static_folder='static')

@employee.route('/homepage', methods=['GET', 'POST'])
def employee_homepage():
    return render_template('employee_homepage.html')