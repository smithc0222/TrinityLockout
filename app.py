from flask import Flask, render_template, redirect, url_for, request, session, flash, send_file
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from io import BytesIO


#create app object
app = Flask(__name__)

#config
import os
app.config.from_object('config.DevelopmentConfig')

#create sqlalchemy object
db = SQLAlchemy(app)

#instantiate bootstrap
Bootstrap(app)
from forms import *
from models import *

#------------------------------------------------------
# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/login', methods = ['POST', 'GET'])
def login():
    login_form=LoginForm()
    if login_form.validate_on_submit():
        session['logged_in'] = True
        return redirect(url_for('index'))
    return render_template('login.html', login_form=login_form)


@app.route('/upload', methods = ['GET','POST'])
def upload():
    return render_template('upload.html')

@app.route('/lockout', methods=['POST', 'GET'])
def lockout():
    user=db.session.query(User).first()
    lockout_form=LockoutForm(request.form)
    lockout_line_form=LockoutLineForm(request.form)
    today=date.today()
    user=db.session.query(User).first()
    lockout=db.session.query(Lockout).all()
    last_lockout=lockout[-1].id
    next_lockout=last_lockout+1


    if request.method == 'POST':

        new_lockout=Lockout(lockout_description=lockout_form.lockout_description.data,
                            lockout_author=user,
                            goggles=lockout_form.goggles.data,
                            faceshield=lockout_form.faceshield.data,
                            fullface=lockout_form.fullface.data,
                            dustmask=lockout_form.dustmask.data,
                            leathergloves=lockout_form.leathergloves.data,
                            saranax=lockout_form.saranax.data,
                            nitrilegloves=lockout_form.nitrilegloves.data,
                            chemicalgloves=lockout_form.chemicalgloves.data,
                            chemicalsuit=lockout_form.chemicalsuit.data,
                            tyrex=lockout_form.tyrex.data,
                            rubberboots=lockout_form.rubberboots.data,
                            sar=lockout_form.sar.data,
                            ppe=lockout_form.ppe.data)
        db.session.add(new_lockout)
        print(new_lockout.lockout_description)
        new_lockout_lines=Lockout_Line(valve_number=lockout_line_form.valve_number.data,
                        line_description=lockout_line_form.line_description.data,
                        lock_position=lockout_line_form.lock_position.data,
                        removal_position=lockout_line_form.removal_position.data,
                        lockout=new_lockout)
        db.session.add(new_lockout_lines)
        print(new_lockout_lines.line_description)
        db.session.commit()
        return redirect(url_for('index'))

    else:
        return render_template('lockout.html', lockout=lockout, user=user, today=today, next_lockout=next_lockout, lockout_form=lockout_form, lockout_line_form=lockout_line_form)

@app.route('/lockout/<int:this_lockout_id>', methods=['POST', 'GET'])
def this_lockout(this_lockout_id):
    this_lockout=db.session.query(Lockout).filter_by(id=this_lockout_id).first()
    lockout_lines=this_lockout.lockout
    if request.method=='POST':
        files = request.files['inputFile']
        this_file=db.session.query(Lockout).first()
        this_file.filename=filename=files.filename
        this_file.data=files.read()
        this_lockout.status=False
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('upload.html', this_lockout=this_lockout, lockout_lines=lockout_lines)


@app.route('/')
def index():
    today=date.today()
    user=db.session.query(User).first()
    lockout=db.session.query(Lockout).all()
    open_lockouts=db.session.query(Lockout).filter_by(status=True).all()
    closed_lockouts=db.session.query(Lockout).filter_by(status=False).all()
    return render_template('index.html', closed_lockouts=closed_lockouts, open_lockouts=open_lockouts, user=user, today=today)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
