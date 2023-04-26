# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Applicació de gestió de telefons amb webpy."""
import web
import json
from contacts import Contacts
from users import Users
from session import Sessio
from tokens import Tokens
from logs import Logs
from sessionldap import SessionLdap
from conf import COOKIE_EXP, LDAP_OPTION, DB_FOLDER, IMPORT_FILE
import import_contacts

render = web.template.render('templates/')

COOKIE_SID = 'sid'
COOKIE_ULVL = 'ulvl'

urls = (
    '/', 'index',
    '/sessio/(.*)', 'ses',
    '/sendMail/(.*)', 'sendMail',
    '/regenPass/([0-9a-zA-Z]{32})', 'regenPass',
    '/createPassword/([0-9a-zA-Z]{32})', 'createPassword',
    '/regenPass', 'changePassword',
    '/getUid', 'getUid',
    '/registerUsr', 'registerUsr',
    '/log/(.*)', 'logControl',
    '/user/(.*)', 'usersControl',
    '/contact/(.*)', 'contactsControl',
    '/importContacts', 'importContacts',
    '/importContacts/(.*)', 'importContacts'
)


class index:
    """Retorna al login o al índex depenent de si el login és correcte.

    Comprova si te SID.
    """

    def GET(self):
        """Retorna al índex o login.

        Returns:
            (str): Torna render a login o índex.
        """
        if web.cookies().get(COOKIE_SID) is not None:
            if LDAP_OPTION is False:
                print('ldap False')
                if update_ulvl_cookie(Sessio()) is True:
                    return render.index()
            print('ldap True')
            return render.index()
        return render.login()


class registerUsr:
    """Classe que renderitza tablesUsrAndLog."""

    def GET(self):
        """Carrega la pàgina del registre d'usuaris i comprova permisos.

        Raises:
            sid - web.SeeOther: Torna l'usuari a índex.
            sessio.select_uid(sid) - web.SeeOther: Render a tablesUsrAndLog.

        Returns:
            (str): Torna render o SeeOther.
        """
        if LDAP_OPTION is True:
            return
        sessio = Sessio()
        update_ulvl_cookie(sessio)
        sid = web.cookies().get(COOKIE_SID)

        if sid is not None:

            if sessio.select_uid(sid) is None:
                raise web.SeeOther('/')
            if sessio.user_level == 3:
                return render.tablesUsrAndLog()
        raise web.SeeOther('/')


class regenPass:
    """Render a changePassword, comprova token vàlid."""

    def GET(self, token_uid):
        """Canvia de pàgina a changePassword, comprova token.

        Raises:
            web.SeeOther: Torna l'usuari a l'índex si no es valida la sessió.

        Returns:
            (str): Render a changePassword.
        """
        if LDAP_OPTION is True:
            return
        if Tokens().select_uid_by_token(token_uid)[0] is True:
            return render.changePassword()
        raise web.SeeOther('/')


class ses:
    """Crear la sessió, comprova les galetes, elimina les galetes."""

    def read_cookie(self):
        """Llegeix la galeta de la pàgina web.

        Returns:
            (str): Nom galeta.
        """
        return web.cookies().get(COOKIE_SID)

    def write_cookie_session(self, sid):
        """Escriu la galeta d'id de sessió.

        Args:
            sid [str]: Session Id en MD5.
        """
        web.setcookie(COOKIE_SID, sid, expires=COOKIE_EXP)

    def write_cookie_ulvl(self, ulvl):
        """Escriu la galeta de nivell d'usuari.

        Args:
            ulvl [str]: ulvl en MD5.
        """
        web.setcookie(COOKIE_ULVL, ulvl,
                      expires=COOKIE_EXP)

    def POST(self, action):
        """Crea, comprova, elimina les galetes.

        Args:

            action (str): Tipus d'acció (login/remove).

        Returns:
            (str): Retorna el dict.
        """
        val = web.input()
        web.header('Content-type', 'text/json; charset=UTF-8')
        ip = web.ctx['ip']

        if action == "login":

            if val.keys() != {'mail', 'pass'}:
                return json.dumps({'result': 'param-error'})

            if LDAP_OPTION is False:
                (result, uid, usrlvl) = Sessio().start_session(val, ip)
                self.write_cookie_ulvl(usrlvl)
                self.write_cookie_session(uid)
                if result is False:
                    return json.dumps({'result': 'login_error'})
                return json.dumps((result, uid, usrlvl))
            else:
                (result, uid) = SessionLdap().start_session_ldap(val, ip)
                self.write_cookie_session(uid)
                if result is False:
                    return json.dumps({'result': 'login_error'})
                return json.dumps((result, uid))

        elif action == "remove":

            sid = ses.read_cookie(self)
            Sessio().expire_session(sid)
            web.setcookie(COOKIE_SID, sid, expires=-1)
            web.setcookie(COOKIE_ULVL, sid, expires=-1)
            raise web.SeeOther('/')


class sendMail:
    """Classe per enviar correus electrònics."""

    def POST(self, action):
        """Envia un mail diferent segons el action.

        Args:
            action:
                - sendmail1: Anar a la pàgina de recuperar contrasenya.
        Returns:
            (int): Retorna un 0 si les dades rebudes no són vàlides.
        """
        if LDAP_OPTION is True:
            return
        web.header('Content-type', 'text/json; charset=UTF-8')
        ret_param_error = json.dumps({'result': 'param-error'})

        if action == "sendmail1":

            val = web.input()

            if 'mail' not in val and Sessio().select_email(val) is False:
                return ret_param_error

            Tokens().send_mail(web.ctx.get('homedomain'), val)
            return json.dumps({'result': 'enviat'})


class logControl:
    """Dades de la pàgina principal."""

    def POST(self, action):
        """Recollir dades de la taula, editar usuaris, afegir usuaris.

        Args:
            action:
                - list: Retorna la consulta de tot el log.

        Returns:
            (str): Un string con el resultado formateado en json.
        """
        if LDAP_OPTION is True:
            return

        web.header('Content-type', 'text/json; charset=UTF-8')

        if not update_ulvl_cookie(Sessio()):
            return json.dumps({'result': 'session-error'})

        if web.cookies().get(COOKIE_ULVL) != '3':
            return json.dumps({'result': 'user-level-error'})

        if action == "list":
            return json.dumps(Logs().log_table())


class usersControl:
    """Classe de control d'usuaris."""

    def POST(self, action):
        """Controlador dels usuaris.

        Args:
            action:
                - show_one: Retorna la consulta d'un usuari concret.
                - auto_edit: Retorna la consulta de l'usuari connectat.
                - list: Retorna la consulta de tots els usuaris.
                - edit: Edita les dades d'un usuari.
                - add: Afegeix un usuari a la db.

        Returns:
            (str): Un string con el resultado formateado en json.
        """
        if LDAP_OPTION is True:
            return
        web.header('Content-type', 'text/json; charset=UTF-8')
        sessio = Sessio()
        val = web.input()

        ret_param_error = json.dumps({'result': 'param-error'})

        if not update_ulvl_cookie(sessio):
            return json.dumps({'result': 'session-error'})

        if action == "show_one":

            if 'uid' in val:
                return json.dumps(Users().users_table(val['uid']))

            return ret_param_error

        if action == "auto_edit":

            if val.keys() != {'nom', 'mail', 'uid', 'option'}:
                return ret_param_error

            if val['option'] == "0" and sessio.select_email(val):
                return json.dumps({'result': 'mail-exists'})

            return json.dumps(Users().self_edit(sessio, val))

        if web.cookies().get(COOKIE_ULVL) != '3':
            return json.dumps({'result': 'user-level-error'})

        if action == "list":
            return json.dumps(Users().users_table())

        if action == "edit":

            if val.keys() != {'nom', 'mail', 'lvl', 'uid', 'option'}:
                return ret_param_error

            if val['option'] == "0" and sessio.select_email(val):
                return json.dumps({'result': 'mail-exists'})

            return json.dumps(Users().edit_user(sessio, val))

        if action == "add":

            if val.keys() != {'nom', 'pass', 'mail', 'lvl'}:
                return ret_param_error

            if sessio.select_email(val):
                return json.dumps({'result': 'mail-exists'})

            return json.dumps(Users().add_user(val, sessio))


class contactsControl:
    """Envia les dades de la db al JS."""

    def POST(self, action):
        """Crea les taules.

        Args:
            action:
                - add: Afegeix un contacte a la db.
                - edit: Edita les dades d'un contacte.
                - delete: Esborra les dades d'un contacte.
                - list: Retorna la consulta de tots els contactes.
                - show_one: Retorna la consulta d'un contacte concret.
        Returns:
            (str): Retorna la consulta.
        """
        web.header('Content-type', 'text/json; charset=UTF-8')
        sessio = Sessio()
        contacts = Contacts()
        val = web.input()
        ret_param_error = json.dumps({'result': 'param-error'})

        if LDAP_OPTION is False:
            if not update_ulvl_cookie(sessio):
                return json.dumps({"result": "sessio-error"})

        if action == "list":
            llista = contacts.contacts_table()

            if llista is None:
                return json.dumps({'result': 'phone-table-error'})

            return json.dumps(llista)

        if action == "show_one":
            contact = contacts.contacts_table(web.input())

            if contact is None:
                return json.dumps({'result': 'phone-table-error'})

            return json.dumps(contact)

        if action == "add":

            if val.keys() != {'nom', 'cognoms', 'empresa', 'carrer',
                              'poblacio', 'cp', 'telfix', 'telmovil',
                              'fax', 'correu', 'nif'}:
                return ret_param_error

            return json.dumps(contacts.add_contact(sessio, val))

        if action == "edit":

            if val.keys() != {'nom', 'cognoms', 'empresa', 'carrer',
                              'poblacio', 'cp', 'telfix', 'telmovil', 'fax',
                              'correu', 'nif', 'id'}:
                return ret_param_error

            return json.dumps(contacts.edit_contact(sessio, val))

        if action == "delete":

            if 'id' not in val:
                return ret_param_error

            return json.dumps(contacts.delete_contact(sessio, val))


class importContacts:
    """Classe per importar contactes."""

    def GET(self):
        """Mostra la pàgina per importar contactes.

        Returns:
            str: Torna el resultat en json
        """
        return render.importContacts()

    def POST(self, action):
        """Importar un fitxer csv a la db."""
        web.header('Content-type', 'text/json; charset=UTF-8')
        if action == 'enviar':
            x = web.input(myfile={})
            filedir = DB_FOLDER
            if 'myfile' in x:
                x.myfile.filename = IMPORT_FILE
                filename = IMPORT_FILE.split('/')[-1]
                fout = open(filedir + '/' + filename, 'wb')
                fout.write(x.myfile.file.read())
                fout.close()
                if import_contacts.import_contacts():
                    return json.dumps({'succes': 'True'})
                return json.dumps({'result': 'error-import'})
        return json.dumps({'result': 'post-error'})


class changePassword:
    """Classe per canviar contrasenya."""

    def POST(self):
        """Actualitza la contrasenya a la taula.

        Returns:
            (str): Retorna la consulta.
        """
        if LDAP_OPTION is True:
            return
        web.header('Content-type', 'text/json; charset=UTF-8')
        val = web.input()

        if val.keys() != {'newpass', 'token'}:
            return json.dumps({'result': 'param-error'})

        return json.dumps(Tokens().update_password(val))


class getUid:
    """Classe per agafar la id de l'usuari."""

    def POST(self):
        """Recull la ID d'usuari.

        Returns:
            (str): Retorna la id del usuari.
        """
        web.header('Content-type', 'text/json; charset=UTF-8')
        if LDAP_OPTION is False:
            return json.dumps(Sessio().select_uid(web.cookies()
                              .get(COOKIE_SID)))
        return json.dumps({'result': "ldap-user"})


def update_ulvl_cookie(sessio):
    """Re-escriu la COOKIE_ULVL a partir de la COOKIE_SID.

    Returns:
        (bool): Retorna l'estat de la sessió.
    """
    sid = web.cookies().get(COOKIE_SID)

    if sid is None:
        return False

    (session_status, user_level) = sessio.check_session(sid)

    if session_status:
        web.setcookie(COOKIE_ULVL, user_level, expires=COOKIE_EXP)

    return session_status


if __name__ == "__main__":
    """Inicia l'app."""

    app = web.application(urls, globals())
    app.run()
