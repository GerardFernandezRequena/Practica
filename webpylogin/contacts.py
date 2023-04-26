# -*- coding: utf-8 -*-
"""Modul que conte les funcions de contactes."""

import sqlite3 as lite
from logs import Logs
from sys import stderr
from conf import DB_FILE, DB_FOLDER, LDAP_OPTION


class Contacts(object):
    """Classe de contactes de la taula de telèfons (list)."""

    def __init__(self):
        """Inicia la conexió amb la db."""
        self.conn_db = lite.connect('%s/%s' % (DB_FOLDER, DB_FILE))
        self.cursor = self.conn_db.cursor()

    def contacts_table(self, uid=-1):
        """Retorna la llista de telèfons o la informació d'un contacte concret.

        Returns:
            (list): Llista de telèfons. Si esta buida o falla: None
        """
        from sys import stderr
        try:
            if uid == -1:
                self.cursor.execute("SELECT * FROM list")
                return self.cursor.fetchall()

            self.cursor.execute("SELECT * FROM list WHERE id=%s"
                                % uid['uid'])
            return self.cursor.fetchall()

        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la"
                         " funció phone_table() (%s).\n" % e.args[0])
            return None

    def add_contact(self, sessio, val):
        """Afegir contacte a la taula telèfons (list).

        Args:
            sessió: (Object)
            val:
                - 'sid'     (str): Id de sessió.
                - 'nom'     (str): Nom.
                - 'cognoms' (str): Cognoms.
                - 'empresa' (str): Empresa.
                - 'carrer'  (str): Carrer.
                - 'poblacio'(str): Població.
                - 'cp'      (int): Codi postal.
                - 'telfix'  (int): Telèfon Fix.
                - 'telmovil'(int): Telèfon Mòbil.
                - 'fax'     (int): Número de Fax.
                - 'correu'  (str): Correu electrònic.
                - 'nif'     (str): Número d'identificació fiscal.
                - 'id'      (str): id del Contacte.

        Returns:
            (bool): True si s'executa correctament, False si l'insert falla.
        """
        try:
            self.cursor.execute("INSERT INTO list (name, surnames, company,"
                                " street, population, postal_code, landline,"
                                " mobile_phone, fax, email, nif) VALUES ('%s',"
                                "'%s', '%s', '%s',"
                                "'%s', '%s', '%s',"
                                "'%s', '%s', '%s', '%s')"
                                % (val['nom'], val['cognoms'], val['empresa'],
                                    val['carrer'], val['poblacio'], val['cp'],
                                    val['telfix'], val['telmovil'], val['fax'],
                                    val['correu'], val['nif']))
            self.conn_db.commit()

            if LDAP_OPTION is False:
                logs = Logs()
                logs.action_log(sessio.user_id, logs.CONTACT_ADD,
                                sessio.user_ip)

            return True

        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la"
                         " funció addPhone() (%s).\n" % e.args[0])
            return False

    def edit_contact(self, sessio, val):
        """Edita un usuari a la taula telèfons (list).

        Args:
            sessió: (Object)
            val:
                - 'sid'     (str): Id de sessió.
                - 'nom'     (str): Nom.
                - 'cognoms' (str): Cognoms.
                - 'empresa' (str): Empresa.
                - 'carrer'  (str): Carrer.
                - 'poblacio'(str): Població.
                - 'cp'      (int): Codi postal.
                - 'telfix'  (int): Telèfon Fix.
                - 'telmovil'(int): Telèfon Mòbil.
                - 'fax'     (int): Número de Fax.
                - 'correu'  (str): Correu electrònic.
                - 'nif'     (str): Número d'identificació fiscal.
                - 'id'      (str): id del Contacte.

        Returns:
            (bool): True si s'executa correctament, False si dóna error.
        """
        from sys import stderr

        try:

            self.cursor.execute("UPDATE list SET name='%s', "
                                "surnames='%s', company='%s', street='%s', "
                                "population='%s', postal_code='%s', "
                                "landline= '%s', mobile_phone='%s', "
                                "fax= '%s', email='%s', nif='%s'"
                                " WHERE id='%s';"
                                % (val['nom'], val['cognoms'], val['empresa'],
                                   val['carrer'], val['poblacio'], val['cp'],
                                   val['telfix'], val['telmovil'], val['fax'],
                                   val['correu'], val['nif'], val['id']))
            self.conn_db.commit()

            if LDAP_OPTION is False:
                logs = Logs()
                logs.action_log(sessio.user_id, logs.CONTACT_EDIT,
                                sessio.user_ip)

            return True

        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la"
                         " funció selfeditPhone() (%s).\n" % e.args[0])
            return False

    def delete_contact(self, sessio, val):
        """Elimina un registre de la taula de telèfons (list).

        Args:
            val:
                id (int): id del telèfon que s'eliminarà.

        Returns:
            (bool): True si s'executa correctament, False si dóna error.
        """
        try:

            self.cursor.execute("DELETE FROM list WHERE id=%s" % val['id'])
            self.conn_db.commit()

            if LDAP_OPTION is False:
                logs = Logs()
                logs.action_log(sessio.user_id, logs.CONTACT_DEL,
                                sessio.user_ip)

            return True

        except lite.Error as e:
            stderr.write("APP: Error de BBDD a la"
                         " funció deletePhone() (%s).\n" % e.args[0])
            return False
