"""Fitxer de configuració."""
from os import environ

# Temps vàlid de les cookies
COOKIE_EXP = environ.get('COOKIE_EXP', 3600)

# # Rutes dels arxius
# Ruta de la localització de la db. Predeterminat: BBDD.sql
DB_FILE = environ.get('DB_FILE', 'BBDD.sql')

# Carpeta on es crearà l'arxiu de db. Predeterminat: $HOME/dirfondb
DB_FOLDER = environ.get('DB_FOLDER', environ.get('HOME') + '/dirfondb')

# Ruta de la localització de les importacions. Predeteminat
IMPORT_FILE = environ.get('IMPORT_FILE', 'import_list.csv')

# # Ldap
LDAP_OPTION = False
# Unitat d'organització
USER_BASE = environ.get('USER_BASE', "ou=people,dc=enginy,dc=eu")
# Grup
USER_GROUP = environ.get('USER_GROUP', "git-repo")
# Usuari de lectura
READ_USER = environ.get('READ_USER', "cn=readonly,dc=enginy,dc=eu")
# Contrasenya de l'usuari de lectura
READ_PASS = environ.get('READ_PASS', "Eingoo5p")
# Conexió al servidor
SERVER_URI = environ.get('SERVER_URI', "ldaps://172.26.0.9:636")

# # Credencials pel primer Admin
# Escriu el nom en el camp de baix. Predeterminat: admin
ADMIN_NAME = environ.get('ADMIN_NAME', 'admin')

# Escriu la contrasenya en el camp de baix. Predeterminat: admin
ADMIN_PASSWORD = environ.get('ADMIN_PASSWORD', 'admin')

# Escriu el correu en el camp de baix. Predeterminat: admin@admin.com
ADMIN_EMAIL = environ.get('ADMIN_EMAIL', 'admin@gmail.com')
