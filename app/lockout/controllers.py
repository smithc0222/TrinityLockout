from flask import Flask, Blueprint, render_template, redirect, url_for, request, session, flash, send_from_directory
from app.lockout.forms import LockoutForm, LockoutLineForm
from app.lockout.models import Lockout, Lockout_Line
from app.auth.models import User
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

#Blueprint Module Creation
mod = Blueprint('lockout', __name__, template_folder='templates')

#login manager flask-login
from app import app
from app import db

from app.auth.controllers import load_user

@mod.route('/')
@login_required
def index():
    today=datetime.today()
    user=db.session.query(User).filter_by(username=current_user.username).first()
    print(current_user.username)
    open_lockouts=db.session.query(Lockout).filter_by(status=True).all()
    closed_lockouts=db.session.query(Lockout).filter_by(status=False).all()
    return render_template('index.html', closed_lockouts=closed_lockouts, open_lockouts=open_lockouts, user=user, today=today)

@mod.route('/upload', methods = ['GET','POST'])
@login_required
def upload():
    return render_template('upload.html')


@mod.route('/save_lockout', methods=['POST', 'GET'])
@login_required
def save_lockout():
    all_lockout=db.session.query(Lockout).all()
    this_lockout=all_lockout[-1]
    lockout_line_form=LockoutLineForm(request.form)
    lockout_lines=this_lockout.lockout
    if request.method == 'POST':
        new_lockout_line=Lockout_Line(valve_number=lockout_line_form.valve_number.data,
                        line_description=lockout_line_form.line_description.data,
                        lock_position=lockout_line_form.lock_position.data,
                        removal_position=lockout_line_form.removal_position.data,
                        lockout=this_lockout)
        db.session.add(new_lockout_line)
        db.session.commit()
        return redirect(url_for('lockout.save_lockout'))
    else:
        return render_template('save_lockout.html', this_lockout=this_lockout, lockout_line_form=lockout_line_form, lockout_lines=lockout_lines)


@mod.route('/lockout', methods=['POST', 'GET'])
@login_required
def lockout():
    user=db.session.query(User).filter_by(username=current_user.username).first()
    lockout_form=LockoutForm(request.form)
    lockout_line_form=LockoutLineForm(request.form)
    today=datetime.today()
    lockout=db.session.query(Lockout).all()
    last_lockout=lockout[-1].id
    next_lockout=last_lockout+1


    if request.method == 'POST':

        new_lockout=Lockout(lockout_number=lockout_form.lockout_number.data,
                            lockout_description=lockout_form.lockout_description.data,
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

        new_lockout_line=Lockout_Line(valve_number=lockout_line_form.valve_number.data,
                        line_description=lockout_line_form.line_description.data,
                        lock_position=lockout_line_form.lock_position.data,
                        removal_position=lockout_line_form.removal_position.data,
                        lockout=new_lockout)
        db.session.add(new_lockout_line)

        db.session.commit()
        return redirect(url_for('lockout.save_lockout'))

    else:
        return render_template('lockout.html', lockout=lockout, user=user, today=today, next_lockout=next_lockout, lockout_form=lockout_form, lockout_line_form=lockout_line_form)

@mod.route('/lockout/<int:this_lockout_id>', methods=['POST', 'GET'])
@login_required
def this_lockout(this_lockout_id):
    this_lockout=db.session.query(Lockout).filter_by(id=this_lockout_id).first()
    lockout_lines=this_lockout.lockout
    if request.method=='POST':
        files = request.files['file']
        filename=files.filename
        files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        this_file=db.session.query(Lockout).filter_by(id=this_lockout.id).first()
        this_file.filename=files.filename
        this_file.data=files.read()
        this_lockout.status=False
        db.session.commit()

        return redirect(url_for('lockokut.index'))

    else:
        return render_template('upload.html', this_lockout=this_lockout, lockout_lines=lockout_lines)


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@mod.route('/static/lockout/<filename>')
@login_required
def uploaded_file(filename):

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)