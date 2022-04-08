import os,datetime
import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "uploads.db"))
app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80))
    image = db.Column(db.LargeBinary)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
db.create_all()

@app.route('/file-upload', methods=['POST'])
def upload_file():
    dataname = request.form.get('filename')
    dataimage = request.files['image']
    
    if 'image' not in request.files:
        return jsonify({'msg': 'Tidak Boleh Kosong'})

    elif dataname and dataimage:
        data = User(filename=dataname, image=dataimage.read())
        db.session.add(data)
        db.session.commit()
        return jsonify({'msg': 'Upload Successfully'})
    else:
        return jsonify({'msg': 'Upload Failed'})

if __name__ == '__main__':
    app.run(debug=True, port=4000)