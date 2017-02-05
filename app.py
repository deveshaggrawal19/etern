from os.path import join, dirname, realpath
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import User, Subscribe, Base, Uploads
from werkzeug.utils import secure_filename


engine = create_engine('sqlite:///lantern.db')
Base.metadata.bind = engine
Data_session = sessionmaker(bind=engine)
session = Data_session()
app = Flask(__name__)


UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/database')
def database():
    tmp = []
    for i in session.query(User).all():
        tmp.append(i.name)
    print(tmp)
    return 'nothing'


@app.route('/', methods=['GET', 'POST'])
def coming_soon():
    if request.method == 'GET':
        return render_template('soon.html')
    else:
        if request.args.get('subscribe'):
            new = Subscribe()
            new.name = request.form.get('name')
            new.email = request.form.get('email')
            session.add(new)
            session.commit()
            return 'Thankyou for subscribing'
        else:
            new = User()
            upload = Uploads()
            file = request.files['file']
            new.name = request.form.get('name')
            new.title = request.form.get('title')
            new.caption = request.form.get('caption')
            new.genre = request.form.get('genre')
            try:
                session.add(new)
                session.flush()
                upload.user_id = new.id
                upload.filename = secure_filename(file.filename)
                session.add(upload)
                session.flush()
                file.save(join(app.config['UPLOAD_FOLDER']+'/'+new.genre, str(upload.id)))
                session.commit()
            except:
                session.rollback()
                return 'Something went wrong.'
            return redirect(url_for('coming_soon'))

if __name__ == "__main__":
    app.run(debug=True)
