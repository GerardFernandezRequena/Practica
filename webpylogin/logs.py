# -*- coding: utf-8 -*-
"""Modul que conte les funcions dels logs."""
import sqlite3 as lite
from sys import stderr
from conf import DB_FILE, DB_FOLDER


class Logs(object):
    """Classe de registres (log)."""

    def __init__(self):
        """Inicia la conexió amb la db."""
        self.conn_db = lite.connect('%s/%s' % (DB_FOLDER, DB_FILE))
        self.cursor = self.conn_db.cursor()
        self.LOG_IN = 1
        self.LOG_OUT = 2
        self.NEW_USER = 3
        self.PW_CHANGE = 4
        self.USER_EDIT = 5
        self.USER_AUTOEDIT = 6
        self.USER_ADD = 7
        self.CONTACT_EDIT = 8
        self.CONTACT_ADD = 9
        self.CONTACT_DEL = 10

    def action_log(self, user_id, action, ip):
        """Insereix a la taula registres cada acció que es fa a l'aplicació.

        Args:
            user_id: Id del usuari.
            action (int): Accio feta per l'usuari. Les accions sòn:
                - 1: Entrada a l'app. LOG_IN
                - 2: Sortida de l'app. LOG_OUT
                - 4: Canvia de contrasenya d'un usuari. PW_CHANGE
                - 5: Usuari editat. USER_EDIT
                - 6: Usuari autoeditat. USER_AUTOEDIT
                - 7: Usuari afegit manualment. USER_ADD
                - 8: Telèfon editat. CONTACT_EDIT
                - 9: Telèfon afegit. CONTACT_ADD
                - 10: Telèfon eliminat. CONTACT_DEL
                - (+10): Invalid.
            ip (str): IP de l'usuari registrat.

        Returns:
            (bool): True si s'executa correctament, False si dóna error.
        """
        try:

            self.cursor.execute("INSERT INTO log "
                                "(user_id, date, action, ipaddress)"
                                " VALUES( %i, datetime('now','localtime')"
                                ", %i, %i);"
                                % (user_id, action, ip))
            self.conn_db.commit()
            return True

        except lite.Error as e:
            stderr.write("APP: Error de BBDD en user_registration(), (%s).\n"
                         % e.args[0])
            return False

    def log_table(self):
        """Retorna la taula de log.

        Returns:
            (list): Retorna la consulta. Si esta buida o dóna error None.
        """
        try:

            self.cursor.execute("""SELECT log.action, log.date, log.ipaddress,
                                users.user, users.email, users.userlevel
                                FROM log INNER JOIN users ON
                                log.user_id = users.id""")
            return self.cursor.fetchall()

        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la funció"
                         " log_table() (%s).\n" % e.args[0])
            return None
