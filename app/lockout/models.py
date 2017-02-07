from app import db
from datetime import datetime

class Lockout(db.Model):

    __tablename__="lockout"
    id=db.Column(db.Integer, primary_key=True)
    lockout_number=db.Column(db.String(10), nullable=False)
    lockout_description=db.Column(db.String(200), nullable=False)
    lockout_author = db.relationship('User', backref=db.backref('lockout_author', lazy='dynamic'))
    user_id=db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
    lockout_file=db.Column(db.String(20), nullable=True)
    pid_file=db.Column(db.String(20), nullable=True)
    open_status=db.Column(db.Boolean(), default=True)
    close_status=db.Column(db.Boolean(), default=False)
    implemented_by= db.relationship('User', backref=db.backref('implemented_by', lazy='dynamic'))
    implemented_status=db.Column(db.Boolean(), default=False)
    accepted_by = db.relationship('User', backref=db.backref('accepted_by', lazy='dynamic'))
    accepted_status=db.Column(db.Boolean(), default=False)
    work_status=db.Column(db.Boolean(), default=False)
    closed_by=db.relationship('User', backref=db.backref('pulled_by', lazy='dynamic'))
    goggles=db.Column(db.Boolean(), default=False)
    faceshield=db.Column(db.Boolean(),default=False)
    fullface=db.Column(db.Boolean(), default=False)
    dustmask=db.Column(db.Boolean(), default=False)
    leathergloves=db.Column(db.Boolean(), default=False)
    saranax=db.Column(db.Boolean(), default=False)
    nitrilegloves=db.Column(db.Boolean(), default=False)
    chemicalgloves=db.Column(db.Boolean(), default=False)
    chemicalsuit=db.Column(db.Boolean(),default=False)
    tyrex=db.Column(db.Boolean(),default=False)
    rubberboots=db.Column(db.Boolean(),default=False)
    sar=db.Column(db.Boolean(),default=False)
    date=db.Column(db.DateTime)
    ppe=db.Column(db.String(50))


    def __init__(self, lockout_number, lockout_description, lockout_author, goggles, faceshield,
        fullface, dustmask, leathergloves, saranax, nitrilegloves, chemicalsuit, chemicalgloves,
        tyrex, rubberboots, sar, ppe, date=None):
        self.lockout_number=lockout_number
        self.lockout_description=lockout_description
        if date is None:
            date = datetime.utcnow()
        self.date = date
        self.lockout_author=lockout_author
        self.goggles=goggles
        self.faceshield=faceshield
        self.fullface=fullface
        self.dustmask=dustmask
        self.leathergloves=leathergloves
        self.saranax=saranax
        self.nitrilegloves=nitrilegloves
        self.chemicalsuit=chemicalsuit
        self.chemicalgloves=chemicalgloves
        self.tyrex=tyrex
        self.rubberboots=rubberboots
        self.sar=sar
        self.ppe=ppe

    def __repr__(self):
        return 'Lockout: {}'.format(self.lockout_number)

class Lockout_Line(db.Model):

    __tablename__="lockout_line"
    id=db.Column(db.Integer, primary_key=True)
    valve_number=db.Column(db.String(10), nullable=False)
    line_description=db.Column(db.String(50), nullable=True)
    lock_position=db.Column(db.String(10), nullable=False)
    removal_position=db.Column(db.String(10), nullable=False)
    lockout=db.relationship('Lockout', backref=db.backref('lockout', lazy='dynamic'))
    lockout_id=db.Column('lockout_id', db.Integer, db.ForeignKey('lockout.id'))

    def __init__(self, valve_number, line_description,lock_position, removal_position, lockout):
        self.valve_number=valve_number
        self.line_description=line_description
        self.lock_position=lock_position
        self.removal_position=removal_position
        self.lockout=lockout

    def __repr__(self):
        return 'Valve #: {} | Lockout ID: {}'.format(self.valve_number, self.lockout.id)
