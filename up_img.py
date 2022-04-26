#6D/19090146/GarinIrsyadChoriri
#6B/19090085/NurulArifiahGunarsih
import os,datetime
from tokenize import Name
import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(
    os.path.join(project_dir, "uploads.db"))
app.config['UPLOAD_FOLDER'] = 'img'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80))
    file = db.Column(db.String(120), unique=False, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)

if not os.path.exists(os.path.join(project_dir, app.config['UPLOAD_FOLDER'])):
    os.makedirs(os.path.join(project_dir, app.config['UPLOAD_FOLDER']))
if not os.path.exists(os.path.join(project_dir, 'uploads.db')):
    db.create_all()

@app.route('/file-upload', methods=['POST'])
def upload_file():
    Name = request.form.get('filename')
    file = request.files['file']

    if 'file' not in request.files:
        return jsonify({'msg': 'Upload Failed :('})

    if file.filename != '':
        try:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = User(filename=Name, file=filename)
            db.session.add(data)
            db.session.commit()
            return jsonify({'msg': 'Upload Success :)'})
        except Exception as error:
            return jsonify({'msg': 'Upload Failed, nama ini '+filename+' sudah dipakai!'})
    else:
        return jsonify({'msg': 'Upload Failed :('})

if __name__ == '__main__':
    app.run(debug=True, port=4000)
