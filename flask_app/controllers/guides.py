from flask_app import app
from flask_app.models.utilities import login_required
from flask import render_template, request, redirect, session, flash,url_for
from flask_app.models.guide import Guide
import os

@app.route('/guide/<int:id>')
def show_guide(id):
    guide = Guide.get_by_id(id)
    print(guide)  # or use logging.debug(guide)
    if guide:
        return render_template('guides.html', guide=guide)
    else:
        flash('Guide not found.')
        return redirect(url_for('dashboard'))

@app.route('/make_guide', methods=['GET', 'POST'])
@login_required
def make_guide():
    if request.method == 'POST':
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
            return redirect(url_for('guides')) 
        except Exception as e:
            flash(f"An error occurred while saving the guide: {str(e)}")
            return render_template('make_guide.html')

    return render_template('make_guide.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload_guide_image', methods=['POST'])
def upload_guide_image():
    if 'image' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Here, you might also want to update the database with the new image path
        return redirect(url_for('dashboard')) 

@app.route('/create_guide', methods=['POST'])
def create_guide():
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(file.filename)  #Remnant function for inputting images
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            image_path = None
    else:
        image_path = None

    guide_data = {
        'title': request.form['title'],
        'content': request.form['content'],
        'user_id': session['user_id'],
        'image_path': image_path
    }
    Guide.save(guide_data)
    return redirect(url_for('dashboard'))



@app.route('/guides/<int:id>/delete', methods=['POST',"GET"])
@login_required
def delete_guide(id):
    guide = Guide.get_by_id(id)
    if guide.user_id != session['user_id']:
        flash("You are not authorized to delete this guide.")
        return redirect(url_for('dashboard'))
    
    Guide.delete(id)
    return redirect(url_for('dashboard'))

@app.route('/guides/<int:id>/edit')
@login_required
def edit_guide(id):
    guide = Guide.get_by_id(id)
    if not guide or guide.user_id != session['user_id']:
        flash("You are not authorized to edit this guide.")
        return redirect(url_for('dashboard'))
    return render_template('edit_guide.html', guide=guide)

@app.route('/guides/<int:id>/update', methods=['POST',"GET"])
@login_required
def update_guide(id):
    guide = Guide.get_by_id(id)
    if guide.user_id != session['user_id']:
        flash("You are not authorized to update this guide.")
        return redirect(url_for('dashboard'))
    
    update_data = {
        'guide_id': id,
        'title': request.form['title'],
        'content': request.form['content']
    }
    Guide.update(update_data)
    flash('Guide updated successfully!')
    return redirect(url_for('guides', id=id))