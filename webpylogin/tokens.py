# -*- coding: utf-8 -*-
"""Modul que conte les funcions dels tokens."""
import sqlite3 as lite
from conf import DB_FILE, DB_FOLDER
import libs
from logs import Logs
from sys import stderr


class Tokens(object):
    """Classe per enviar correus."""

    def __init__(self):
        """Inicia la connexió amb la db."""
        self.conn_db = lite.connect('%s/%s' % (DB_FOLDER, DB_FILE))
        self.cursor = self.conn_db.cursor()

    def select_uid_by_token(self, token):
        """Selecciona la uid segons el token rebut.

        Args:
            token (str): El token de l'usuari el qual vols el uid.

        Returns:
            (list): Retorna true o false i la uid de l'usuari.
        """
        try:
            self.cursor.execute(
                "SELECT uid FROM tokens WHERE token = '%s' AND isvalid = 'N'"
                % token)
            res = self.cursor.fetchone()
            if res is not None:
                return (True, res[0])
            return (False, None)
        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la funció"
                         " select_uid_by_token() (%s).\n" % e.args[0])
            return (False, None)

    def expire_tokens(self):
        """Invalida els tokens expirats."""
        exp = libs.milliseconds_current_time() - (libs.MAX_TOKEN * 1000)

        try:
            self.cursor.execute(
                "UPDATE tokens SET isvalid = 'E' WHERE date < %d" % exp)
            self.conn_db.commit()
        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la funció"
                         " expire_tokens() (%s).\n" % e.args[0])

    def invalidate_Token(self, token):
        """Invalida un token específic.

        Args:
            token (str): El token que s'eliminarà
        """
        try:
            self.cursor.execute(
                "UPDATE tokens SET isvalid = 'U' WHERE token='%s'\n" % token)
            self.conn_db.commit()
        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la funció"
                         " invalidate_Token() (%s).\n" % e.args[0])

    def update_password(self, val):
        """Actualitza la contrasenya dels usuaris a la taula d'usuaris (users).

        Args:

            val:
                newpass (str): Contrasenya nova.
                token   (str): Validar sessió.

        Returns:
            (bool): True si s'executa correctament, False si dóna error.

        """
        try:

            self.expire_tokens()

            (select_result, user_id) = self.select_uid_by_token(val['token'])

            if select_result is False:
                return False

            self.cursor.execute(
                "UPDATE users SET password ='%s' WHERE id= %i"
                % (val['newpass'], int(user_id)))

            self.conn_db.commit()
            logs = Logs()
            logs.action_log(int(user_id), logs.PW_CHANGE,
                            libs.ip_aton(libs.get_ip()))
            self.invalidate_Token(val['token'])
            return True

        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la"
                         " funció regenerate_password() (%s).\n"
                         % e.args[0])
            return False

    def send_mail(self, host, val):
        """Crea i envia correus.

        Args:

            host (str): El protocol utilitzat + el nom d'amfitrió (domini)

            val:
             - 'email' (str): Correu electrònic.

            nom (str, optional): Nom. Predeterminat a 0.

        Returns:
           (bool): True si s'executa correctament, False si dóna error.
        """
        from smtplib import SMTP_SSL
        from time import time

        ADDR_MAIL = 'noreply@enginy.eu'
        USER_MAIL = 'daemon@enginy-automatica.com'
        PASS_MAIL = 'JM8fAUXT72te5nH'
        SERV_MAIL = 'mail.enginy.eu'
        email = val['mail']

        try:

            self.cursor.execute(
                "SELECT * FROM users WHERE email = '%s'" % email)
            usr = self.cursor.fetchone()

            if usr is None:
                return True

            uid = usr[0]

            while True:

                tid = libs.make_sid(libs.get_ip())

                self.cursor.execute(
                    "SELECT * FROM tokens WHERE token = '%s' AND isvalid = 'N'"
                    % tid)
                if len(self.cursor.fetchall()) == 0:
                    break

                if time() > libs.MAX_TOKEN:
                    self.cursor.execute(
                        "UPDATE tokens SET isvalid = 'E' WHERE uid='%s'"
                        % uid)
                    self.conn_db.commit()

            sec = libs.milliseconds_current_time()

            self.cursor.execute("INSERT INTO tokens "
                                "(token, date, isvalid, uid)"
                                "VALUES( '%s', %i, 'N', '%s' );"
                                % (tid, sec, uid))
            self.conn_db.commit()

            msg = libs.create_message(usr, tid, ADDR_MAIL,
                                      email, host)

            try:
                sender = SMTP_SSL()
                sender = SMTP_SSL(SERV_MAIL)
                sender.login(USER_MAIL, PASS_MAIL)
                sender.sendmail(ADDR_MAIL, usr[5], msg.as_string())
            except sender.SMTPException:
                return False
            return True

        except lite.Error as e:
            stderr.write(
                "APP: Error de BBDD a la funció send_mail() (%s).\n"
                % e.args[0])
            return False

    def select_valid_token(self, uid):
        """Torna el token del uid donat si es vàlid.

        Args:
            uid (int): ID d'usuari.

        Returns:
            (list): Token de la uid donada.
        """
        try:

            self.cursor.execute(
                "SELECT * FROM tokens WHERE uid = '%s' AND isvalid = 'N'"
                % uid
            )
            return self.cursor.fetchone()

        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la funció"
                         " select_valid_token() (%s).\n" % e.args[0])
            return None
