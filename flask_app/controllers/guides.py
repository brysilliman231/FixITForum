from flask_app import app
from flask_app.models.utilities import login_required
from flask import render_template, request, redirect, session, flash,url_for
from flask_app.models.guide import Guide

@app.route('/guide/<int:id>')
def guide(id):
    guide = Guide.get_by_id(id)  # Fetch the guide by its ID
    if guide:
        return render_template('guides.html', guide=guide)  # Consider renaming to guide_detail.html
    else:
        flash('Guide not found.')
        return redirect(url_for('dashboard'))
    
@app.route('/guide/<key>')
def show_guide(key):
    guide = Guide.get_by_key(key)
    if guide is not None:
        return render_template('guides.html', guide=guide)
    else:
        flash('Guide not found.')
        return redirect(url_for('dashboard'))

@app.route('/make_guide', methods=['GET', 'POST'])
@login_required
def make_guide():
    if request.method == 'POST':
        # Assume there's validation before saving
        # Here you should also validate the data from the form
        if not request.form['title'] or not request.form['content']:
            flash("Please fill in all fields.")
            return render_template('make_guide.html')

        new_guide_data = {
            'title': request.form['title'],
            'content': request.form['content'],
            'user_id': session['user_id']  # Securely getting user_id from session
        }
        
        try:
            Guide.save(new_guide_data)
            flash("Guide created successfully!")
            return redirect(url_for('guides'))  # Assuming you have a 'guides' endpoint to display guides
        except Exception as e:
            flash(f"An error occurred while saving the guide: {str(e)}")
            return render_template('make_guide.html')

    return render_template('make_guide.html')