# app/public/routes.py

from app import login_required
from flask import render_template, session
from . import public_bp
from .models import Categoria, Pregunta, Respuesta, Ranking, Resultado
import random
import datetime
import time

@public_bp.route('/trivia')
@public_bp.route('/trivia/')
def index_trivia():
    return render_template('trivia.html')

@public_bp.route('/ranking')
@public_bp.route('/ranking/')
def mostrar_ranking():
    ranking = Ranking.query.order_by('t_jugado')
    for r in ranking:
        print (r.usuario)
    return render_template('ranking.html', ranking=ranking)



@public_bp.route('/trivia/categorias', methods=['GET'])
@public_bp.route('/trivia/categorias/', methods=['GET'])
@login_required
def mostrar_categorias():
    categorias = Categoria.query.all()
    if "t_inicio" not in session.keys():
        session['t_inicio'] = datetime.datetime.now()
        for c in categorias:
            session[c.descripcion] = False

    c_faltantes = []
    for c in categorias:
        if not session[c.descripcion]:
            c_faltantes.append(c)

    if len(c_faltantes) != 0:
        return render_template('categorias.html', categorias=c_faltantes)
    else:
        return render_template('ganador.html', tiempo_total=(datetime.datetime.now()-session['t_inicio']))


@public_bp.route('/trivia/<id_categoria>/pregunta', methods=['GET'])
@login_required
def mostrar_pregunta(id_categoria):
    preguntas = Pregunta.query.filter_by(categoria_id=id_categoria).all()
    # elegir pregunta aleatoria pero de la categoria adecuada
    pregunta = random.choice(preguntas)
    categ = Categoria.query.get(id_categoria)
    
    respuestas_posibles = pregunta.respuestas
    return render_template('preguntas.html', categoria=categ, pregunta=pregunta, respuestas_posibles=respuestas_posibles)


@public_bp.route('/trivia/<int:pregunta_id>/respuesta/<int:id_respuesta>', methods=['GET'])
@login_required
def evaluar_respuesta(pregunta_id, id_respuesta):
    respuesta = Respuesta.query.get(id_respuesta)
    pregunta = Pregunta.query.get(pregunta_id)
    msg = "equivocada"
    if respuesta.pregunta_id == pregunta_id and respuesta.verdadera:
        msg = "correcta"
        categoria = Categoria.query.get(pregunta.categoria_id)
        session[categoria.descripcion] = True


    categorias = Categoria.query.all()
    c_faltantes = []
    for c in categorias:
        if not session[c.descripcion]:
            c_faltantes.append(c)
            break


    if "respuestas" not in session.keys():
        session["respuestas"] = [(pregunta_id, id_respuesta)]
    else:
        respuestas = session["respuestas"]
        respuestas.append((pregunta_id, id_respuesta))
        session["respuestas"] = respuestas

    if len(c_faltantes) != 0:
        return render_template('respuestas.html', message=msg)
    else:
        tiempo_total=datetime.datetime.now()-session['t_inicio']
        registro = Ranking(usuario_id= session["_user_id"], t_inicio=session['t_inicio'], t_jugado=float(tiempo_total.total_seconds()))
        registro.save()

        for resp in session["respuestas"]:
            resultado = Resultado(ranking_id=registro.id, pregunta_id=resp[0], respuesta_id=resp[1])
            resultado.save()
            print(str(resp[0])+" - "+str(resp[1]))

        session.clear()
        return render_template('ganador.html', tiempo_total=tiempo_total)


