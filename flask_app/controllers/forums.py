from flask_app import app
from flask_app.models.utilities import login_required
from flask import render_template, request, redirect, session, flash,url_for
from flask_app.models.forum import Forum

@app.route('/forum/<int:id>')
def forum(id):
    forum = Forum.get_by_id(id)  # Fetch the forum by its ID
    if not forum:
        flash('Forum not found.')
        return redirect(url_for('dashboard'))
    return render_template('forums.html', forum=forum)

@app.route('/make_forum', methods=['GET', 'POST'])
@login_required
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

@app.route('/forum/<key>')
def show_forum(key):
    forum = Forum.get_by_key(key)
    if forum is not None:
        return render_template('forums.html', forum=forum)
    else:
        flash('Forum not found.')
        return redirect(url_for('dashboard'))
    