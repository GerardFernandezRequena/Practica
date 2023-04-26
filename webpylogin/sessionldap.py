#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Modul que conte les funcions de ldap."""

from conf import USER_BASE, USER_GROUP, READ_USER, READ_PASS, SERVER_URI
from conf import DB_FOLDER, DB_FILE
from logs import Logs
from sys import stderr
import sqlite3 as lite
import libs
import ldap


class SessionLdap:
    """Classe per controlar les sessions amb LDAP."""

    def __init__(self):
        """Inicia la connexió amb la db."""
        self.conn_db = lite.connect('%s/%s' % (DB_FOLDER, DB_FILE))
        self.cursor = self.conn_db.cursor()
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        self.conn_ldap = ldap.initialize(SERVER_URI)

    def start_session_ldap(self, val, ip_address):
        """Autoritzar l'usuari amb el servidor ldap.

        Args:
            val (dict): Conte les credencials de l'usuari
            ip_address (str): L'adreça ip de l'usuari

        Returns:
            list: Resultat i uid
        """
        try:
            self.conn_ldap.simple_bind_s(
                "uid=%s,%s" % (val['mail'], USER_BASE), val['pass'])
        except ldap.INVALID_CREDENTIALS:
            return (False, None)

        self.conn_ldap.simple_bind_s(READ_USER, READ_PASS)

        userdata = self.conn_ldap.search_s(
            USER_BASE, ldap.SCOPE_SUBTREE,
            """(&(|(objectclass=inetOrgPerson))
            (|(memberof=cn=%s,ou=groups,dc=enginy,dc=eu))
            (|(uid=%s)))""" % (USER_GROUP, val['mail']))

        uid = int(userdata[0][1]['uidNumber'][0].decode())

        try:
            self.cursor.execute(
                "UPDATE sessions SET state = '%d' "
                "WHERE userid = %d AND state = '%d'" % (libs.INACTIVE, uid,
                                                        libs.ACTIVE))
            self.conn_db.commit()

            ip_numeric = libs.ip_aton(ip_address)

            sid = libs.create_sid(ip_address, self.cursor)

            now = libs.milliseconds_current_time()

            self.cursor.execute("INSERT INTO sessions VALUES("
                                "'%s', %i, %i, %i, '%d')"
                                % (sid, now, uid, ip_numeric, libs.ACTIVE)
                                )
            self.conn_db.commit()

            log = Logs()
            log.action_log(uid, log.LOG_IN, ip_numeric)
        except lite.Error as e:
            stderr.write(
                "APP: Error de BBDD al la funció start_session_ldap()(%s).\n"
                % e.args[0])
            return (False, None)

        if (len(userdata) > 0):
            return (True, uid)

        return (False, None)
