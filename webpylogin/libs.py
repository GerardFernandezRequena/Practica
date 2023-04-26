# -*- coding: utf-8 -*-
"""Modul que conte classes generals."""

MAX_TOKEN = (1 * 900)
EXPIRED = 0
ACTIVE = 1
INACTIVE = 2


def create_message(usr, tid, ADDR_MAIL, email, host):
    """Transforma l'html a type mime per poder enviar-lo per correu.

    Args:
        usr (str): Nom.
        htmlcorreo (str): Nom de l'html.
        tid (int): Id del token.
        ADDR_MAIL (str): Correu electrònic del proveïdor.
        email (str): Correu electrònic del receptor.
        host (str): El protocol utilitzat + el nom d'amfitrió (domini).

    Returns:
        (MIMEMultipart): Correu electrònic.
    """
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.header import Header
    from email.utils import make_msgid, formatdate

    msg = MIMEMultipart('related')
    msg['Subject'] = Header("(Re)Activació de l'accés.", "utf-8")
    msg['From'] = "%s <%s>" % (Header("Telecontrol", "utf-8"), ADDR_MAIL)
    msg['To'] = "%s <%s>" % (Header("%s" % usr[1], "utf-8"), "%s" % usr[5])
    msg['Message-ID'] = make_msgid('enginy.eu')
    msg['Date'] = formatdate()
    msg_alt = MIMEMultipart('alternative')
    with open("templates/changePasswordEmail.html", 'r') as fhd:
        html = fhd.read()
    msg_alt.attach(
        MIMEText(html % {'host': host, 'token': tid, 'email': email},
                 'html', _charset="UTF-8"))

    msg.attach(msg_alt)
    with open("static/img/logo.png", 'rb') as img_file:
        image = MIMEImage(img_file.read())
    image.add_header('Content-ID', '<logotip>')
    msg.attach(image)
    return msg


def milliseconds_current_time():
    """Retorna el temps actual en mil·lisegons.

    Returns:
        (int): El temps actual en mil·lisegons.
    """
    from time import time
    return round(time())


def make_sid(ip_address):
    """Genera l'identificador de sessió amb IP.

    Args:
        ip_address (str): IP rebuda.

    Returns:
        (str): IP en MD5.
    """
    from hashlib import md5
    from time import strftime
    seed = ip_address + strftime('%Y%M%D%h%m%s')
    return md5(seed.encode('utf-8')).hexdigest()


def ip_aton(addr):
    """Transforma la IP en Nombre enter.

    Args:
        ip_address (str): IP rebuda.

    Returns:
        (int): IP transformada en Nombre enter.
    """
    import socket
    import struct
    return struct.unpack("!I", socket.inet_aton(addr))[0]


def get_ip():
    """Retorna la IP del hostname.

    Returns:
        (str): IP de la host.
    """
    import socket
    return socket.gethostbyname(socket.gethostname())


def create_sid(ip_address, cursor):
    """Crea una id de sessió.

    Args:
        ip_address (str): Una adreça IP
        cursor (object): Cursor a la bbdd

    Returns:
        str: Retorna la sid de
    """
    while True:

        sid = make_sid(ip_address)

        cursor.execute(
            "SELECT * FROM sessions WHERE id = '%s'" % sid)
        if len(cursor.fetchall()) == 0:
            break

    return sid
