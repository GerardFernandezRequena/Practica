# -*- coding: utf-8 -*-
"""Modul que conte les funcions de sessions."""
import sqlite3 as lite
import libs
from conf import DB_FILE, DB_FOLDER, COOKIE_EXP
from logs import Logs
from sys import stderr


class Sessio(object):
    """Funcions relacionades amb el funcionament de la sessió."""

    def __init__(self):
        """Inicia la connexió amb la db."""
        self.conn_db = lite.connect('%s/%s' % (DB_FOLDER, DB_FILE))
        self.cursor = self.conn_db.cursor()

    def start_session(self, val, ip_address):
        """
        Crea una sessió si el correu electrònic i contrasenya són correctes.

        Args:
            val:
             - 'email'      (str): Correu electrònic.
             - 'passwd'     (str): Contrasenya.
             - 'ip_address' (int): La IP de l'usuari.

        Returns:
            (list): True si l'usuari es correcte, id de sessió, nivell d'usuari
        """
        try:

            self.cursor.execute(
                """SELECT id, userlevel FROM users
                WHERE email = '%s' AND password = '%s'""" % (
                 val['mail'], val['pass']
                )
            )

            res = self.cursor.fetchone()

            if res is None:
                return (False, None, None)

            (uid, usrlvl) = res

            ip_numeric = libs.ip_aton(ip_address)

            self.cursor.execute(
                "UPDATE sessions SET state = '%d' "
                "WHERE userid = %d AND state = '%d'" % (libs.INACTIVE, uid,
                                                        libs.ACTIVE))
            self.conn_db.commit()

            sid = libs.create_sid(ip_address, self.cursor)

            now = libs.milliseconds_current_time()

            self.cursor.execute("INSERT INTO sessions VALUES("
                                "'%s', %i, %i, %i, '%d')"
                                % (sid, now, uid, ip_numeric, libs.ACTIVE)
                                )
            self.conn_db.commit()

            log = Logs()
            log.action_log(uid, log.LOG_IN, ip_numeric)

            return (True, sid, usrlvl)

        except lite.Error as e:
            stderr.write(
                "APP: Error de BBDD al la funció start_session()(%s).\n"
                % e.args[0])
            return (False, None, None)

    def check_session(self, sid):
        """Actualitza la darrera data de sessió i revisa si està activa.

        Args:
            sid (str): Id de sessió.

        Returns:
            (list): True si la sessió es vàlida i el nivell d'usuari.
        """
        try:

            now = libs.milliseconds_current_time()
            exp = now - (COOKIE_EXP * 1000)

            self.cursor.execute(
                "UPDATE sessions SET state = '%d' "
                "WHERE state = '%d' AND toupdate < %d" % (libs.EXPIRED,
                                                          libs.ACTIVE, exp)
            )
            self.conn_db.commit()

            self.cursor.execute(
                "SELECT toupdate FROM sessions "
                "WHERE id='%s' AND state='%d'" % (sid, libs.ACTIVE))

            if self.cursor.fetchone() is None:
                return (False, None)

            self.cursor.execute(
                "UPDATE sessions SET toupdate = %i WHERE id='%s'"
                % (now, sid))
            self.conn_db.commit()

            user_data = self.get_user_by_sid(sid)

            self.user_email = user_data[5]
            self.user_level = user_data[4]
            self.user_id = user_data[0]
            self.user_ip = libs.ip_aton(libs.get_ip())
            self.user_name = user_data[1]

            return (True, self.user_level)

        except lite.Error as e:
            stderr.write(
                "APP: Error de BBDD al la funció check_session() (%s).\n"
                % e.args[0])
            return (False, None)

    def is_valid_session(self, sid):
        """Comprova si la sessió és vàlida.

        Args:
            sid (str): Id de sessió.

        Returns:
            (bool): True si és vàlid, False si no és vàlid.
        """
        try:

            self.cursor.execute(
                "SELECT * FROM sessions WHERE id='%s' AND state='%d' " % (
                    sid, libs.ACTIVE)
            )
            return self.cursor.fetchone() is not None

        except lite.Error as e:
            stderr.write(
                "APP: Error de BBDD al la funció is_valid_session() (%s).\n"
                % e.args[0])
            return False

    def expire_session(self, sid):
        """Marca com a expirada la sessió de l'usuari.

        Args:
            sid (str): Id de sessió.

        Returns:
           (bool): True si s'executa correctament, False si dóna error.
        """
        from sys import stderr
        try:

            if not self.is_valid_session(sid):
                return False

            res = self.get_user_by_sid(sid)

            self.adapt_state_Y(sid)

            log = Logs()
            log.action_log(res[0], log.LOG_OUT, libs.ip_aton(libs.get_ip()))

            return True

        except lite.Error as e:
            stderr.write("APP: Error de BBDD al la funció "
                         "expire_session() (%s).\n"
                         % e.args[0])
            return False

    def get_user_by_sid(self, sid):
        """Retorna les dades de l'usuari per la sessió donada.

        Args:
            sid (str): ID de sessió.

        Returns:
            (list): Dades de l'usuari al qual pertany la sessió.
        """
        try:

            self.cursor.execute("SELECT userid FROM sessions WHERE id='%s'"
                                % sid)
            res = self.cursor.fetchone()
            self.cursor.execute("SELECT * FROM users WHERE id='%s'" % res[0])
            return self.cursor.fetchone()

        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la funció"
                         " get_user_by_sid() (%s).\n" % e.args[0])
            return None

    def select_email(self, val):
        """Comprova si el correu està a la db i l'usuari està actiu.

        Args:
             val:
             - 'email' (str): Correu electrònic.

        Returns:
            (bool): True si l'usuari existeix i no està desactivat.
        """
        try:

            self.cursor.execute("SELECT * FROM users WHERE email='%s' "
                                "AND userlevel<>'0'" % val['mail'])
            return self.cursor.fetchone() is not None

        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la funció"
                         " select_email() (%s).\n" % e.args[0])
            return False

    def adapt_state_Y(self, sid):
        """Canvia el camp state a Inactiu a la taula sessions.

        Args:
            sid (str): Id de sessió.
        """
        from sys import stderr

        try:

            self.cursor.execute(
                "UPDATE sessions SET state = '%d' WHERE id='%s'"
                % (libs.INACTIVE, sid))
            self.conn_db.commit()

        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la funció"
                         " adapt_state_Y() (%s).\n" % e.args[0])

    def select_uid(self, sid):
        """Selecciona la id del usuari de la taula de sessions si esta actiu.

        Args:
            sid (str): Id de sessió.

        Returns:
            (list): Consulta de la BBDD o None si la consulta dona error.
        """
        self.cursor.execute(
            "SELECT userid FROM sessions WHERE id='%s' AND state='%d'" % (
                sid, libs.ACTIVE)
        )
        return self.cursor.fetchone()
