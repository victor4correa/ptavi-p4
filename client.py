#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente UDP que abre un socket a un servidor."""
import sys
import socket


try:
    # Constantes. Dirección IP del servidor y contenido a enviar
    IPSERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    PETICION = sys.argv[3]
    USER = sys.argv[4]
    EXPIRES = sys.argv[5]
    LINE = ("REGISTER sip:" + USER + " SIP/2.0\r\nExpires: " + EXPIRES +
            "\r\n\r\n")
except IndexError:

    sys.exit("Usage: client.py ip puerto register sip_address expires_value")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.connect((IPSERVER, PORT))
        print(LINE)
        my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024)
        print(data.decode('utf-8'))
        print("Socket terminado.")
