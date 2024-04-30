from flask_app.models.utilities import login_required
from flask_app.models.user import User
from flask_app.models.forum import Forum
from flask_app.models.guide import Guide
from flask_app import app
from flask import render_template, request, session, redirect, flash, url_for
from flask_bcrypt import Bcrypt
import logging
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    # Log the current session state
    logging.debug(f"Current session state: {session}")

    if 'user_id' not in session:
        # If no user is logged in, render the 'index.html' template
        logging.debug("No user logged in, displaying index page.")
        return render_template('index.html')
    else:
        # If a user is logged in, redirect to the dashboard
        logging.debug(f"User logged in with ID {session['user_id']}, redirecting to dashboard.")
        return redirect('/dashboard')
    



@app.route('/dashboard')
@login_required
def dashboard():
    logging.debug("Loading the dashboard")
    try:
        guides = Guide.get_all_guides()
        forums = Forum.get_all_forums()
        return render_template('dashboard.html', guides=guides, forums=forums)
    except Exception as e:
        logging.error(f"Failed to load dashboard data: {e}")
        flash('There was a problem loading the dashboard.')
        return render_template('dashboard.html', guides=[], forums=[])

@app.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        flash("You are not authorized to view this page.")
        return redirect('/login')
    
    user = User.get_by_id({'id': user_id})
    if not user:
        flash("User not found.")
        return redirect('/dashboard')
    
    return render_template('profile.html', user=user)



@app.route("/register", methods=["POST"])
def register():
   
    if not User.validate_user(request.form):
        # If validation fails, redirect back to the home page to display flash messages
        return redirect('/')
    
    # Check if the user already exists
    existing_user = User.get_by_email({'email': request.form['email']})
    if existing_user:
        flash("Email already taken.")
        return redirect('/')
    
    # Hash the password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    # Create new user data dictionary
    new_user_data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash  # Store the hashed password
    }

    # Save the user to the database
    user_id = User.save(new_user_data)

    # Store user id in session
    session['user_id'] = user_id
    
    return redirect('/dashboard')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Validate login information
        if not User.validate_user_login(request.form):
            flash("Invalid input. Please try again.")
            return redirect(url_for('login'))  # Redirect to the login route which renders index.html

        # Attempt to retrieve the user by email
        user_in_db = User.get_by_email({'email': request.form['email']})
        if not user_in_db:
            flash("Invalid Email/Password")
            return redirect(url_for('login'))

        # Check password hash against entered password
        if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            flash("Invalid Email/Password")
            return redirect(url_for('login'))

        # If the passwords matched, we set the user_id into session
        session['user_id'] = user_in_db.id
        flash("You are now logged in!")
        return redirect(url_for('dashboard'))
    else:
        # If it's a GET request, just render the login page which is index.html
        return render_template('index.html')
@app.route('/logout')
def logout():
    session.clear()  # This clears the session, logging the user out
    flash("You have been logged out successfully.")
    return redirect('/')  #

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if 'user_id' not in session:
        flash("Please log in to view this page.")
        return redirect('/login')

    if request.method == 'POST':
        user_data = {
            "id": session['user_id'],
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email']
        }
        User.update(user_data)
        flash("Your profile has been updated.")
        return redirect('/dashboard')

    user = User.get_by_id({'id': session['user_id']})  # Assuming there's a method to fetch user by ID
    return render_template('edit_profile.html', user=user)