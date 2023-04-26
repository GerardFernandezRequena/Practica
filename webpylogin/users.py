# -*- coding: utf-8 -*-
"""Modul que conte les funcions de usuaris."""
import sqlite3 as lite
from sys import stderr
from conf import DB_FILE, DB_FOLDER
from logs import Logs


class Users(object):
    """Classe de control d'usuaris (users)."""

    def __init__(self):
        """Inicia la conexió amb la db."""
        self.conn_db = lite.connect('%s/%s' % (DB_FOLDER, DB_FILE))
        self.cursor = self.conn_db.cursor()

    def users_table(self, uid=-1):
        """Retorna les dades per la taula usuari.

        Args:
            uid (int, optional): Mostra les dades de l'usuari donat,
            sinó donarà totes les dades de tots els usuaris.

        Returns:
            (list): Dades usuaris, si dóna error o la taula està buida: None.
        """
        try:

            if uid == -1:
                self.cursor.execute("SELECT * FROM users")
                return self.cursor.fetchall()

            self.cursor.execute("SELECT * FROM users WHERE id=%s" % uid)
            return self.cursor.fetchall()

        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la funció"
                         " users_table() (%s).\n" % e.args[0])
            return None

    def add_user(self, val, sessio):
        """Afegeix un nou usuari a la taula users.

        Args:

            val:
                - 'nom'    (str): Nom.
                - 'passwd' (str): Contrasenya.
                - 'mail'   (str): Correu eletrònic.
                - 'lvl'    (int): Nivell d'usuari.

            sessió: (Object)


        Returns:
            (bool): True si s'executa correctament, False si dóna error.
        """
        try:

            self.cursor.execute("INSERT INTO users"
                                "(user,password,userlevel,email)"
                                "VALUES ( '%s', '%s', '%s', '%s');"
                                % (val['nom'], val['pass'], val['lvl'],
                                   val['mail'])
                                )
            self.conn_db.commit()

            logs = Logs()
            logs.action_log(sessio.user_id, logs.USER_ADD, sessio.user_ip)

            return True

        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la"
                         " funció add_user() (%s).\n" % e.args[0])
            return False

    def edit_user(self, sessio, val):
        """Edita el nom/email/nivell d'usuari d'un usuari (només admin).

        Args:

            sessió: (Object)

            val:
                - 'nom'  (str): Nom.
                - 'mail' (str): Correu eletrònic.
                - 'lvl'  (int): Nivell d'usuari.
                - 'uid'  (int): Id d'usuari.


        Returns:
            (bool): True si s'executa correctament, False si dóna error.
        """
        try:

            self.cursor.execute(
                "UPDATE users SET "
                "user='%s', userlevel=%s, email='%s' WHERE id='%s';"
                % (val['nom'], val['lvl'], val['mail'], val['uid']))
            self.conn_db.commit()

            logs = Logs()
            logs.action_log(sessio.user_id, logs.USER_EDIT, sessio.user_ip)

            return True

        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la"
                         " funció edit_user() (%s).\n" % e.args[0])
            return False

    def self_edit(self, sessio, val):
        """Actualitza el correu i la contrasenya de l'usuari.

        Args:

            sessió: (Object)

            val:
                - 'nom' (str): Nom.
                - 'mail'(str): Correu eletrònic.
                - 'uid' (int): Id d'usuari (db).

        Returns:
            (bool): True si s'executa correctament, False si dóna error.
        """
        from sys import stderr

        try:

            self.cursor.execute(
                "UPDATE users SET user='%s', email='%s' WHERE id='%s';"
                % (val['nom'], val['mail'], val['uid']))
            self.conn_db.commit()

            logs = Logs()
            logs.action_log(sessio.user_id, logs.USER_AUTOEDIT, sessio.user_ip)

            return True

        except lite.Error as e:
            stderr.write("APP: Error de BBDD self_edit() (%s).\n" % e.args[0])
            return False
