'''
This modules declares routes that handle uploading and retrieving sneakers
'''
from flask import Blueprint, render_template
from form import UploadForm
from flask_login import login_required
from utils.role import role_required, current_user
from model import db, Sneakers, Images


post = Blueprint('post', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    # checks if it is a valid file
    if '.' in filename:

        # split the file once from the right using the . as a benchmark
        parts = filename.rsplit('.', 1)
        file_extension = parts[1].lower() # convert the extension to lowercase
        if file_extension in ALLOWED_EXTENSIONS:
            return True
        else:
            return False
    else:
        return False # if no . it cannot contain a valid extension

@post.route('/upload', methods=['GET', 'POST'])
@loginrequired
@role_required('admin')
def upload():
    form = UploadForm()

    if request.method == 'POST':
        form = UploadForm(request.form)

        if form.validate_on_submit():
            name = form.name.data.lower()
            price = float(form.price.data)
            description = form.description.data

            if 'files' not in request.files:
                return jsonify({'error': 'No file part in the request. Please make sure to select files for upload.'})

            files = request.files.getlist('files')

            if not files:
                return jsonify({'error': 'No files were selected. Please choose at least one file to upload.'})

            try:
                sneaker = Sneakers(name=name, price=price, description=description, user_id=current_user.id)
                db.session.add(sneaker)
                db.session.commit()

                uploads = []
                for file in files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        
                        # save the images to a folder
                        upload_folder = current_app.config['UPLOAD_FOLDER']
                        file.save(os.path.join(upload_folder, filename))
                        
                        # save the filename to the database
                        image = Images(filename=filename, sneaker_id=sneaker.id)
                        db.session.add(image)
                        db.session.commit()
                        uploads.append(filename)
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': 'An unexpected error occured. Try Again!'})

            if uploads:
                return jsonify({'success': 'Uploaded successfully!'})
            else:
                return jsonify({'error': "Failed to upload!"})
        else:
            return jsonify({'errors': form.errors})

    return render_template('upload.html', form=form)
