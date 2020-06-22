# app/auth/routes.py

from . import auth_bp
from app import login_manager
from flask import render_template, redirect, url_for, flash, request, session, current_app
from flask_principal import Principal, Permission, Identity, AnonymousIdentity, RoleNeed, UserNeed, identity_loaded, identity_changed

from .models import Usuario
from .forms.login import LoginForm
from .forms.register import RegisterForm

from flask_login import LoginManager, current_user, login_user, login_required, logout_user

#le decimos a Flask-Login como obtener un usuario
@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(int(user_id))

@auth_bp.route('/trivia/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index_trivia'))
    form = LoginForm()
    if form.validate_on_submit():
        #get by email valida
        user = Usuario.get_by_user(form.username.data)
        if user is None:
            user = Usuario.get_by_email(form.username.data)

        if user is not None and user.check_password(form.password.data):
            # funcion provista por Flask-Login, el segundo parametro gestion el "recordar"
            login_user(user, remember=form.remember_me.data)

            next_page = request.args.get('next', None)
            if not next_page:
                next_page = url_for('public.index_trivia')

            app_actual = current_app._get_current_object()
            identity_changed.send(app_actual, identity=Identity(user.id))
            return redirect(url_for('public.index_trivia'))
        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('auth.login'))
    # no loggeado, dibujamos el login con el form vacio
    return render_template('login.html', form=form)

@auth_bp.route("/trivia/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('public.index_trivia'))
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        nombre = form.nombre.data
        apellido = form.apellido.data
        usuario = form.usuario.data
        email = form.email.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese email
        user = Usuario.get_by_email(email)
        if user is None:
            user = Usuario.get_by_user(usuario)

        if user is not None:
            flash('El email {} ya está siendo utilizado por otro usuario'.format(email))
        else:
            # Creamos el usuario y lo guardamos
            user = Usuario(nombre=nombre, apellido=apellido, usuario=usuario, email=email)
            user.set_password(password)
            user.save()
            # Dejamos al usuario logueado
            login_user(user, remember=True)
            app_actual = current_app._get_current_object()
            identity_changed.send(app_actual, identity=Identity(user.id))
            return redirect(url_for('public.index_trivia'))
    return render_template("register.html", form=form)


@auth_bp.route('/trivia/logout')
def logout():
    session.clear()
    logout_user()
    # Flask-Principal: Remove session keys
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Flask-Principal: the user is now anonymous
    app_actual = current_app._get_current_object()
    identity_changed.send(app_actual, identity=AnonymousIdentity())

    return redirect(url_for('public.index_trivia'))






