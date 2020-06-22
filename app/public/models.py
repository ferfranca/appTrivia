from app import db


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(64), index=True, unique=True)
    preguntas = db.relationship('Pregunta', backref='categoria', lazy='dynamic')

    def __repr__(self):
        return '<Categoria: {}>'.format(self.descripcion)


class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False, unique=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    respuestas = db.relationship('Respuesta', backref='pregunta', lazy='dynamic')
    resultado = db.relationship('Resultado', backref='pregunta', lazy='dynamic')

    def __repr__(self):
        return '<Pregunta %s>' % self.text


class Respuesta(db.Model):
    # campo id es el Primary Key de la tabla
    id = db.Column(db.Integer, primary_key=True)
    # Texto que tiene la respuesta
    text = db.Column(db.String(255), nullable=False, unique=True)
    # ¿Es la respuesta correcta a la Pregunta? Lo defino en este campo booleano, que no sea Nulo, y que x defecto sea False
    verdadera = db.Column(db.Boolean, nullable=False, default=False)
    # Esta respuesta corresponde a una pregunta exacta, guardo el id de esa pregunta
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'))
    resultado = db.relationship('Resultado', backref='respuesta', lazy='dynamic')

    def __repr__(self):
        return '<Respuesta %s>' % self.text


from sqlalchemy.ext.declarative import declared_attr
class TriviaUser(db.Model):
    __abstract__ = True

    @declared_attr
    def rankings(cls):
        return db.relationship('Ranking', backref='usuario', lazy='dynamic')


class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    t_inicio = db.Column(db.DateTime)
    t_jugado = db.Column(db.Float)
    resultado = db.relationship('Resultado', backref='ranking', lazy='dynamic')

    def __repr__(self):
        return str(self.id)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()



class Resultado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ranking_id = db.Column(db.Integer, db.ForeignKey('ranking.id'))
    pregunta_id = db.Column(db.Integer, db.ForeignKey('pregunta.id'))
    respuesta_id = db.Column(db.Integer, db.ForeignKey('respuesta.id'))

    def __repr__(self):
        return str(self.id)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

