"""Crea un arxiu xml amb les dades dels contactes."""
import sqlite3 as lite
from conf import DB_FOLDER, DB_FILE


def main():
    """Crea un xml amb les dades de la taula amb telèfons."""
    res = ""
    conn_db = lite.connect('%s/%s' % (DB_FOLDER, DB_FILE))
    cursor = conn_db.cursor()

    cursor.execute("SELECT * FROM list")
    select = cursor.fetchall()
    cursor.execute("SELECT * FROM list")
    if len(select) > 0:
        for dades in cursor.fetchall():
            res += "  <Contact>\n"
            if dades[1] == '' and dades[2] == '':
                res += "    <LastName></LastName>\n"
                res += "    <FirstName>%s</FirstName>\n" % dades[3]
            else:
                res += "    <LastName>%s</LastName>\n" % dades[2]
                res += "    <FirstName>%s</FirstName>\n" % dades[1]
            if dades[7] > 0:
                if dades[3] == '':
                    res += "    <Phone type=\"Home\">\n"
                    res += "      <phonenumber>%s</phonenumber>\n" % dades[7]
                    res += "      <accountindex>1</accountindex>\n"
                    res += "    </Phone>\n"
                else:
                    res += "    <Phone type=\"Work\">\n"
                    res += "      <phonenumber>%s</phonenumber>\n" % dades[7]
                    res += "      <accountindex>1</accountindex>\n"
                    res += "    </Phone>\n"
            if dades[8] > 0:
                res += "    <Phone type=\"Mobile\">\n"
                res += "      <phonenumber>%s</phonenumber>\n" % dades[8]
                res += "      <accountindex>1</accountindex>\n"
                res += "    </Phone>\n"
            res += "    <Groups>\n"
            res += "      <groupid>0</groupid>\n"
            res += "    </Groups>\n"
            res += "  </Contact>\n"

    res = ("<AddressBook>\n" + res + "</AddressBook>\n")
    return res


if __name__ == '__main__':
    main()
