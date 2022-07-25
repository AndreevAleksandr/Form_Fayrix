from io import BytesIO
import datetime
from sqlalchemy import DateTime
from flask import Flask, render_template, request, redirect, send_file, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_form.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hashwjj2123hhshsajyzx66SzSda?/./a;asu&&9auqw!!2weoqs'
db = SQLAlchemy(app)


class user_form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(DateTime, default=datetime.datetime.utcnow)
    position = db.Column(db.String(20), nullable=False)
    grade = db.Column(db.String(20), nullable=False)
    lvl_english = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text)
    test_task = db.Column(db.Boolean, default=True)
    filename = db.Column(db.String(50))
    filedata = db.Column(db.LargeBinary)

    def __repr__(self):
        return self.title


@app.route('/', methods=['POST', 'GET'])
def index():
    position = ['Developer', 'Data Science', 'Design & UX', 'DevOps',
            'QA / Manual', 'QA / Auto', 'Product Management',]
    grade = ['Junior', 'Middle', 'Senior', 'Teamlead / Techlead']
    lvl_english = ['A-1 / A-2', 'B-1 / B-2', 'C-1 / C-2']

    if request.method == 'POST':
        position = request.form['position']
        grade = request.form['grade']
        lvl_english = request.form['lvl_english']
        email = request.form['email']
        link = request.form['link']
        comment = request.form['comment']

        test_task = request.form.get('test_task') != None
        if  request.form.get('test_task'):
            test_task = True

        if len(request.form['email']) > 5:
            flash('Thank you for your feedback')
            flash('We will contact you within three business days')
        else:
            flash('Sending error')

        file = request.files['file']

        item = user_form(position=position, grade=grade, lvl_english=lvl_english,
                         email=email, link=link, comment=comment, test_task=test_task,
                         filename=file.filename, filedata=file.read())

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error:('
    else:
        return render_template('index.html', position=position, grade=grade, lvl_english=lvl_english)


@app.route('/down/<pdf_id>')
def down(pdf_id):
    item = user_form.query.filter_by(id=pdf_id).first()
    return send_file(BytesIO(item.filedata), attachment_filename=item.filename,
                     as_attachment=True)


if __name__ == '__main__':
    app.run(debug=False)


