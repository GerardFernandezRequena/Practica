# -*- coding: utf-8 -*-

"""Script que importa dades de la BBDD.

L'arxiu CSV ha d'estar delimitat per ';' i ha de tenir les mateixes columnes
que la BBDD aquestes són:
    name, surnames, company, street, population, postal_code, landline,
    mobile_phone, fax, email, nif.
"""

import sqlite3 as lite
import csv
from conf import DB_FILE, DB_FOLDER, IMPORT_FILE
from sys import stderr


def drop_table(cursor, conn_db):
    """Esborra la taula si existeix i crea una nova.

    Args:
        cursor (method): Cursor de la DB
        conn_db (function): Connexió a la DB

    Returns:
        (bool): Retorna True si tot és correcte, si no False.
    """
    try:
        cursor.execute("DROP TABLE IF EXISTS list;")
        conn_db.commit()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS list (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT(45) DEFAULT NULL,
                surnames TEXT(45) DEFAULT NULL,
                company TEXT(45) DEFAULT NULL,
                street TEXT(45) DEFAULT NULL,
                population TEXT(45) DEFAULT NULL,
                postal_code INTEGER(11) DEFAULT 0,
                landline INTEGER(11) DEFAULT 0,
                mobile_phone INTEGER(11) DEFAULT 0,
                fax INTEGER(11) DEFAULT 0,
                email TEXT(45) DEFAULT NULL,
                nif TEXT(45) DEFAULT NULL);
        """)
        conn_db.commit()
        return True
    except lite.Error as e:
        stderr.write("Error en crear la taula. ERROR: %s\n" % e)
        return False


def import_data(cursor, conn_db):
    """Importa les dades del fitxer CSV.

    Args:
        cusrsor (method): Cursor de la DB
        conn_db (function): Connexió a la DB

    Returns:
        (bool):  Retorna True si s'ha afegit la informació a la DB,
        si no False
    """
    try:
        file = open(DB_FOLDER + "/" + IMPORT_FILE)
        contents = csv.reader(file, delimiter=";")
        next(contents)
    except csv.Error as e:
        stderr.write("""Error en llegir la informació del fitxer.
                        ERROR: %s\n""" % e)
        return False
    try:
        for line in contents:
            cursor.execute("""
            INSERT INTO list (name, surnames, company,
                    street, population, postal_code, landline,
                    mobile_phone, fax, email, nif) VALUES ('%s',
                    '%s', '%s', '%s',
                    '%s', %d, %d,
                    %d, %d, '%s', '%s')"""
                           % (line[1], line[2], line[3], line[4], line[5],
                              int(line[6].replace(',', '')),
                              int(line[7].replace(',', '')),
                              int(line[8].replace(',', '')),
                              int(line[9].replace(',', '')), line[10],
                              line[11]))
            conn_db.commit()
        return True
    except lite.Error as e:
        stderr.write("""Error en inserir les dades a la taula.
                        ERROR: %s\n""" % e)
        return False


def import_contacts():
    """Executa l'app.

    Returns:
        (bool): Retorna True si s'ha importat correctament,
        si no False
    """
    conn_db = lite.connect('%s/%s' % (DB_FOLDER, DB_FILE))
    cursor = conn_db.cursor()
    if drop_table(cursor, conn_db):
        if import_data(cursor, conn_db):
            print("Imported successfully!")
            return True
        else:
            print("Failed to import")
            return False
