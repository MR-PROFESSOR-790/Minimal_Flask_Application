from flask import Flask, render_template, request, redirect, url_for     
from flask_sqlalchemy import SQLAlchemy 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firstapp.db'
with app.app_context():
    db = SQLAlchemy(app)
    
class FirstApp(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    firstapp = FirstApp(fname=fname, lname=lname, email=email)
    db.session.add(firstapp)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/home', methods=['GET'])
def home():
    all_firstapp = FirstApp.query.all()
    return render_template('home.html', all_firstapp=all_firstapp)

@app.route('/delete/<int:sno>')
def delete(sno):
    user = FirstApp.query.filter_by(sno=sno).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update/<int:sno>', methods=['POST'])
def update(sno):
    user = FirstApp.query.filter_by(sno=sno).first()
    user.fname = request.form['fname']
    user.lname = request.form['lname']
    user.email = request.form['email']
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)