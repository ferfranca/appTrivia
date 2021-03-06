# app/restricted/routes.py

from . import restricted_bp

from app import db, admin, app
from flask_login import current_user, login_required
from flask_principal import Principal, Permission, Identity, AnonymousIdentity, RoleNeed, UserNeed, identity_loaded, identity_changed
from flask import render_template, current_app, g, abort
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, request



from app.auth.models import Usuario, Role
from app.public.models import Categoria, Pregunta, Respuesta, Ranking, Resultado
from flask_admin import AdminIndexView


# Agregamos las necesidades a una identidad, una vez que se loguee el usuario.
admin_permission = Permission(RoleNeed('Admin'))

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # Seteamos la identidad al usuario
    identity.user = current_user
    # Agregamos una UserNeed a la identidad, con el usuario actual.
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    # Agregamos a la identidad la lista de roles que posee el usuario actual.
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.rolename))


class MyModelView(ModelView):
    def is_accessible(self):
        has_auth = current_user.is_authenticated
        has_perm = admin_permission.allows(g.identity)
        return has_auth and has_perm

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        has_auth = current_user.is_authenticated
        has_perm = admin_permission.allows(g.identity)
        return has_auth and has_perm

    def inaccessible_callback(self, name, **kwargs):
        has_auth = current_user.is_authenticated
        has_perm = admin_permission.allows(g.identity)
        # esta loggeado pero no es admin
        if has_auth and not has_perm:
            abort(401)
        # no loggeado
        else:
            return redirect(url_for('auth.login', next=request.url))


admin.init_app(app, index_view=MyAdminIndexView())
# agregadmos al admin de todos los modelos
admin.add_view(MyModelView(Categoria, db.session))
admin.add_view(MyModelView(Pregunta, db.session))
admin.add_view(MyModelView(Respuesta, db.session))
admin.add_view(MyModelView(Ranking, db.session))
admin.add_view(MyModelView(Resultado, db.session))
admin.add_view(MyModelView(Usuario, db.session))
admin.add_view(MyModelView(Role, db.session))

#admin.add_view(ModelView(Categoria, db.session))
#admin.add_view(ModelView(Pregunta, db.session))
#admin.add_view(ModelView(Respuesta, db.session))
#admin.add_view(ModelView(Ranking, db.session))
#admin.add_view(ModelView(Resultado, db.session))
#admin.add_view(ModelView(Usuario, db.session))
#admin.add_view(ModelView(Role, db.session))


@restricted_bp.route('/test')
@login_required
@admin_permission.require(http_exception=403)
def test_principal():
    return render_template('test.html')
