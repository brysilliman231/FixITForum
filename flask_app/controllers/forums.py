from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.forum import Forum

@app.route('/forums')
def forums():
    if 'user_id' not in session:
        flash('Please log in to view the forums.')
        return redirect('/')

    forums = Forum.get_all_forums_with_creators()
    return render_template('forums.html', forums=forums)

@app.route('/make_forum', methods=['GET', 'POST'])
def make_forum():
    if 'user_id' not in session:
        flash('Please log in to access this feature.')
        return redirect('/')

    if request.method == 'POST':
        # Assume there's validation before saving
        # ... Your form validation logic ...
            
        new_forum_data = {
            "title": request.form['title'],
            "description": request.form['description'],
            "user_id": session['user_id']  # Retrieved from the logged-in user's session
        }
        Forum.save(new_forum_data)
        return redirect('/forums')

    return render_template('make_forum.html')