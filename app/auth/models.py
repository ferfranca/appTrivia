from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.public.models import TriviaUser

class Usuario(TriviaUser, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=False)
    apellido = db.Column(db.String(50), nullable=False, unique=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128))
    roles = db.relationship('Role', backref='user', lazy='dynamic')

    def __repr__(self):
        return '{} {}'.format(self.nombre, self.apellido)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)

    @staticmethod
    def get_by_user(usuario):
        return Usuario.query.filter_by(usuario=usuario).first()

    @staticmethod
    def get_by_email(email):
        return Usuario.query.filter_by(email=email).first()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(60), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

