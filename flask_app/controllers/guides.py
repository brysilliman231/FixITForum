from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.guide import Guide

@app.route('/guides')
def guides():
    if 'user_id' not in session:
        flash('Please log in to view the guides.')
        return redirect('/')

    guides = Guide.get_all_guides_with_creators()
    return render_template('guides.html', guides=guides)

@app.route('/make_guide', methods=['GET', 'POST'])
def make_guide():
    if 'user_id' not in session:
        flash('Please log in to access this feature.')
        return redirect('/')

    if request.method == 'POST':
        # Assume there's validation before saving
        # ... Your form validation logic ...

        new_guide_data = {
            'title': request.form['title'],
            'content': request.form['content'],
            # Add other form fields as necessary
        }
        Guide.save(new_guide_data)
        return redirect('/guides')

    return render_template('make_guide.html')