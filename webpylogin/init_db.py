#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Compravació bbdd.

Si t'equivocàs en les teves credencials borra l'arxiu creat, posa correctament
les teves credencials i torna a executar l'arxiu.
"""

import sqlite3 as lite
from os import path, makedirs, rename
from conf import DB_FILE, DB_FOLDER, ADMIN_NAME, ADMIN_EMAIL, ADMIN_PASSWORD

VERSION = '1.0'


def check_db():
    """Comprova que la db existeixi i sigui correcte."""
    db_file = "%s/%s" % (DB_FOLDER, DB_FILE)

    if path.isdir(DB_FOLDER):
        print("Directory '%s' already exists" % DB_FOLDER)
    else:
        makedirs(DB_FOLDER)
        print("Directory %s created " % DB_FOLDER)

    if not path.isfile(db_file):
        return False

    else:
        print("File %s already exists" % DB_FILE)
        print("Cheking if %s is valid" % DB_FILE)
        conn_db = lite.connect(db_file)
        cursor = conn_db.cursor()
        try:
            cursor.execute("SELECT version FROM info WHERE id = 1")
            res = cursor.fetchone()

            if res is None:
                copy_db_file(db_file)
                return False

            vers = res[0]

            if vers == VERSION:
                print("Database is valid")
                return True

            else:
                print("Database version not valid.")
                copy_db_file(db_file)
                return False

        except lite.Error:
            copy_db_file(db_file)
            return False


def copy_db_file(db_file):
    """Canvia de nom l'antic arxiu."""
    copy_file = "%s.old" % db_file
    print("Database version not valid")
    print("%s is gonna be renamed to %s" % (db_file, copy_file))
    rename(db_file, copy_file)


def create_db_file():
    """Crea la db."""
    import hashlib
    md5pass = hashlib.md5(ADMIN_PASSWORD.encode('utf-8')).hexdigest()
    conn_db = lite.connect('%s/%s' % (DB_FOLDER, DB_FILE))
    cursor = conn_db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS log (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date datetime DEFAULT current_timestamp NOT NULL,
            action INTEGER DEFAULT 0 NOT NULL,
            ipaddress INTEGER DEFAULT 0 NOT NULL);
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT NOT NULL PRIMARY KEY,
            toupdate INTEGER NOT NULL,
            userid INTEGER NOT NULL,
            ipaddr INTEGER NOT NULL,
            state INTEGER NOT NULL);
    """)
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            token TEXT(256) NOT NULL,
            date datetime NOT NULL,
            isvalid TEXT(256) NOT NULL,
            uid TEXT NOT NULL);
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            user TEXT(256) NOT NULL,
            password TEXT(256) NOT NULL,
            date datetime default current_timestamp,
            userlevel INTEGER DEFAULT 1 NOT NULL,
            email TEXT NOT NULL);
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS info (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            version TEXT(256) NOT NULL);
    """)
    cursor.execute("""
        INSERT INTO users
        (user,password,userlevel,email)
        VALUES ( '%s', '%s', '3', '%s');
    """ % (ADMIN_NAME, md5pass, ADMIN_EMAIL))
    cursor.execute("""
        INSERT INTO info (version) VALUES ('%s');
    """ % VERSION)
    conn_db.commit()
    print("Database created correctly")


if __name__ == "__main__":
    if not check_db():
        create_db_file()
