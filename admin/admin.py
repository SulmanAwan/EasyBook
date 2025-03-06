from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_db_connection

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin.route('/homepage', methods=['GET', 'POST'])
def admin_homepage():
    name = session.get('name')

    return render_template('admin_homepage.html', name=name)

@admin.route('/analytics_dashboard', methods=['GET'])
def analytics_dashboard():
    # TODO: implement dashboard
    return render_template('admin/analytics_dashboard.html')

@admin.route('/manage_accounts', methods=['GET', 'POST'])
def manage_accounts():
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get all users in the database so that the manage_accounts.html page can render them.
        cursor.execute("SELECT user_id, name, email, password, permission FROM users")
        users = cursor.fetchall()

    except Exception as e:
        # In the case of an exception we flash the exception to the user
        flash(f'Error fetching user accounts: {str(e)}', 'error')

    finally:
        cursor.close()
        conn.close()
    
    return render_template('manage_accounts.html', users=users)

@admin.route('/booking_notifications', methods=['GET', 'POST'])
def booking_notifications():
    # TODO: implement booking notifications
    return render_template('admin/booking_notifications.html')

@admin.route('/appointment_history', methods=['GET', 'POST'])
def appointment_history():
    # TODO: implement appointment history
    return render_template('admin/appointment_history.html')

@admin.route('/inbox', methods=['GET', 'POST'])
def inbox():
    # TODO: implment inbox
    return render_template('admin_homepage.html')

@admin.route('/block_day', methods=['GET', 'POST'])
def block_day():
    # TODO: implement block day
    return render_template('admin_homepage.html')

@admin.route('/manage_shift', methods=['GET', 'POST'])
def manage_shift():
    # TODO: implement manage shift
    return render_template('admin_homepage.html')

@admin.route('/add_accounts', methods=['GET', 'POST'])
def add_accounts():
    # Handle form submission (POST REQ)
    if request.method == 'POST':
        # Retrieve form info
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        permission = request.form.get('permission')
        
        # Make sure all the data was entered and no missing values
        if not name or not email or not password or not permission:
            flash('All fields are required.', 'error')
            return render_template('add_accounts.html')

        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Check if email already exists (Cant create accounts with same email since email uniqu)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                # Flash error msg that the email is taken and re-render the form.
                flash('Email already registered', 'error')
                return render_template('add_accounts.html')
            
            # If all info in the form is entered and the email is unique, we add it to database
            cursor.execute(
                "INSERT INTO users (name, email, password, permission) VALUES (%s, %s, %s, %s)",
                (name, email, password, permission)
            )
            conn.commit()
            
            # Flash msg that it was added
            flash('User account created successfully!', 'success')
            return redirect(url_for('admin.add_accounts'))
            
        except Exception as e:
            # Flash error msg containing the exception
            flash(f'Error creating account: {str(e)}', 'error')
            # Render the page again for the user
            return render_template('add_accounts.html')
        finally:
            # Close database connection and cursor when finished with query logic.
            cursor.close()
            conn.close()
    
    # Display the form for every GET req
    return render_template('add_accounts.html')

@admin.route('/edit_account/<int:user_id>', methods=['GET','POST'])
def edit_account(user_id):
    
    # Connect to database to retrieve the record of current user for GET requests and
    # execute queries for the POST requests.
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Use the passed in user_id to retrieve the user record
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user_record = cursor.fetchone() # Store user_record (pass it in each time you render the page again)

        if request.method == 'POST':
            # Get form data
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            permission = request.form['permission']
            
            # If the user attempts to make a change but hasn't modified any form data notify them
            # that no modifications where made and render the page again.
            if name == user_record['name'] and email == user_record['email'] and password == user_record['password'] and permission == user_record['permission']:
                flash('No modifications where made', 'warning')
                return render_template('edit_accounts.html', user_id=user_id, user_record=user_record)

            # Otherwise, execute a query to count the number of users with a matching email as the one inputted by the user in the form
            cursor.execute(
                "SELECT COUNT(*) as count FROM users WHERE email = %s AND user_id != %s", 
                (email, user_id)
            )
            result = cursor.fetchone()

            # Make sure no other accounts exists with the entered email (emails must be unique)
            if result['count'] > 0:
                # Indicate to user that the email they want to update this record with is already in use
                flash('Email already in use by another user', 'warning')
                return render_template('edit_accounts.html', user_id=user_id, user_record=user_record)
            
            # If all test cases are passed (ie: data was modificated, no duplicate email exists) then run the update query on the 
            cursor.execute(
                "UPDATE users SET name = %s, email = %s, permission = %s, password = %s WHERE user_id = %s",
                (name, email, permission, password, user_id)
            )

            # Commit the changes made into the database
            conn.commit()
            # Alert user of successful update
            flash('User updated successfully', 'success')
            # Return user back to manage_accounts page
            return redirect(url_for('admin.manage_accounts'))
    
    except Exception as e:
        # Flash any exceptions that may arise during the process (ex: database crashes)
        flash(f'Error processing account: {str(e)}', 'error')
    finally:
        # Always got to close cursor and database connection
        cursor.close()
        conn.close()
    
    # render template with user_id and user_record in the case of GET requests or exceptions
    return render_template('edit_accounts.html', user_id=user_id, user_record=user_record)
