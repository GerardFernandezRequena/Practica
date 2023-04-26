# **App creada amb webpy**
Aplicació creada amb webpy.

Aplicació destinada a ser una agenda de telèfons. Aquesta aplicació te serveis d'administració d'usuaris, recuperació de contrasenyes per correu electrònic, creació d'usuaris amb validació per correu electrònic i es compatible amb ldap.

## **Ldap:**
Ldap s'activa desde el codi a l'arxiu de configuració de l'app.
```py
# # Ldap
LDAP_OPTION = False
```
Si està en False funcionara amb el correu electrònic i tindra el control d'usuaris i registres.
```py
# # Ldap
LDAP_OPTION = True
```
Si està en True funcionara amb les credencials de ldap, però perdras el control d'ususaris, nomès hi haura un unic nivell d'usuaris i perdras la taula de registres.
## **Permisos d'usuaris:**
Els permisos d'usuaris et permeten tenir mes seguretat a l'app. Hi han els seguents nivells:
- **Usuari:**
    - ***Taula de contactes:*** Mostra els contactes.

- **Operador:**
    - ***Taula de contactes:*** Mostra els contactes. Creació i edició de contactes desde la taula.

- **Adminisitrador:**
    - ***Taula d'usuaris:*** Mostra tots els usuaris. Creació i edició d'usuaris desde la taula.
    - ***Taula de registres:*** Mostra totes les accions fetes per els usuaris.
    - ***Taula de contactes:*** Mostra els contactes. Creació i edició de contactes desde la taula.



## **Importar Contactes:**
La aplciació te una opcio amagada per importar contactes. Aquesta opcio s'accedeix escribin a la barra de navegació */importContacts*. En aquesta pàgina hi haura un  formulari on s'ha de seleccionat un arxiu *csv*. L'arxiu csv ha de contenir les mateixes columnes que la BBDD.

## **Configuració:**
- **Cookies:** Es pot configurar el temps d'expiració de les cookies. Predeterminat a *COOKIE_EXP (3600)* el numero de la cookie es en segons.

- **Base de dades:** 
    - **Localització:** Es pot configurar el nom de l'arxiu amb DB_FILE i pots cambiar la ruta de la BBDD amb DB_FOLDER. Predeterminat *DB_FILE (BBDD.sql)* i *DB_FOLDER (home/dirfondb)*.
    - **Credencials :** Es pot configurar el nom, la contrasenya i el mail del admin. Predeterminat a nom: *ADMIN_NAME (admin)*, correu electrònic: *ADMIN_EMAIL (admin@<area>gmail<area>.com)* i contrasenya: *ADMIN_PASSWORD (admin)*.
- **Ldap:** Es pot activar el ldap. Predeterminat *LDAP_OPTION (False)*
    - **Credencials:** Si ldap està actiu s'ha de configrar la base, el grup, l'usuari de lectura, la contrasenya de l'usuari de lectura i la URI del servidor de ldap. Dades a modificar base: *USER_BASE*, grup: *USER_GROUP*, usuari de lectura: *READ_USER*, contrasenya de l'usuari de lectura: *READ_PASS*, URI del servidor de ldap: *SERVER_URI*.

## **Base de dades**
Si ldap està activat les taules de *users*, *log* i *tokens* quedaran inutilitzades.
### **Com actualitzar la BBDD**
Si vols actualitzar la BBDD s'ha de fer desde el arxiu init_db.py (abans d'actualitzar comprobar que el codi funcioni correctament):
- Per saber la versió que té la base de dades s'ha de consultar a la BBDD i es guarda en una variable:
```py
cursor.execute("SELECT version FROM info WHERE id = 1")
    res = cursor.fetchone()

vers = res[0]
```
- Es comprova si la versió es correcte (per això s'ha de tenir la constant VERSION actualitzada):
```py
if vers == VERSION:
    print("Database is valid")
    return True
```
- Si es igual sortira de la aplicació i dira que es vàlid, sino es cambiara la versió de la BBDD:
```py
else:
    print("Database version not valid.")
    try:
        print("Proceeding to update")
        # --> Ficar Actualitzacions aqui <--
    except:
        copy_db_file(db_file)
        return False
```
- Exemple actualitzar una versió:
```py
import sqlite3 as lite
VERSIO = '1.1'
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
        try:
            print("Proceeding to update")
            # --> Actualitzacions <--
            if vers == '1.0':
                # Crear o modificar les taules desitjades
                cursor.execute("""
                    ALTER TABLE TABLE_EXAMPLE ADD
                    COLUMN_EXAMPLE varchar(255) DEFAULT NULL
                """)
                # Posar dades a les noves taules
                cursor.execute("""
                    UPDATE info SET validation = '%s'
                    WHERE id=1
                """ % conf.VALIDATION)
                # Actualitzar la versió de la BBDD
                cursor.execute("""
                    UPDATE info SET
                    version = '1.1' WHERE id=1
                """)
                # Fer commit
                conn_db.commit()
                vers == '1.1'
                print("Succsesfully updated to %s" % vers)
        except:
            copy_db_file(db_file)
            return False
```
- Si vols fer actualitzacions consecutives s'han de deixar les anteriors actualitzacions. Exemple: 
```py
            print("Proceeding to update")
            # --> Actualitzacions <--
            if vers == '1.0':
                """
                ---------------------
                    Actualització
                ---------------------
                """
                # Actualitzar la versió de la BBDD
                cursor.execute("""
                    UPDATE info SET
                    version = '1.1' WHERE id=1
                """)
                # Fer commit
                conn_db.commit()
                vers == '1.1'
                print("Succsesfully updated to %s" % vers)
            if vers == '1.1':
                                """
                ---------------------
                    Actualització
                ---------------------
                """
                # Actualitzar la versió de la BBDD
                cursor.execute("""
                    UPDATE info SET
                    version = '1.2' WHERE id=1
                """)
                # Fer commit
                conn_db.commit()
                vers == '1.2'
                print("Succsesfully updated to %s" % vers)
```