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
  

            
        new_forum_data = {
            "title": request.form['title'],
            "description": request.form['description'],
            "user_id": session['user_id']  # Retrieved from the logged-in user's session
        }
        Forum.save(new_forum_data)
        return redirect('/dashboard')

    return render_template('make_forum.html')

@app.route('/forum/<key>')
def show_forum(key):
    forum = Forum.get_by_key(key)
    if forum is not None:
        return render_template('forums.html', forum=forum)
    else:
        flash('Forum not found.')
        return redirect(url_for('dashboard'))
    

@app.route('/forums/<int:id>/update', methods=['POST',"GET"])
@login_required
def update_forum(id):
    forum = Forum.get_by_id(id)
    if forum.user_id != session['user_id']:
        flash("You are not authorized to update this forum.")
        return redirect(url_for('dashboard'))
    
    update_data = {
        'forum_id': id,
        'title': request.form['title'],
        'description': request.form['description']
    }
    Forum.update(id, update_data)
    return redirect(url_for('dashboard'))
    

@app.route('/forums/<int:id>/delete', methods=['POST',"GET"])
@login_required
def delete_forum(id):
    forum = Forum.get_by_id(id)
    if forum.user_id != session['user_id']:
        flash("You are not authorized to delete this forum.")
        return redirect(url_for('dashboard'))
    
    Forum.delete(id)
    return redirect(url_for('dashboard'))

@app.route('/forums/<int:id>/edit')
@login_required
def edit_forum(id):
    forum = Forum.get_by_id(id)
    if not forum or forum.user_id != session['user_id']:
        flash("You are not authorized to edit this forum.")
        return redirect(url_for('dashboard'))
    return render_template('edit_forum.html', forum=forum)