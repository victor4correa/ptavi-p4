#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import sys
import socketserver


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    registro = {}
    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        str_line = self.rfile.read().decode("utf-8")
        contenido = str_line.split()
        self.wfile.write("SIP/2.0 200 OK\r\n\r\n".encode('utf-8'))
        usuario = contenido[1].split(":")[-1]
        if contenido[0] == "REGISTER":
            self.registro[usuario] = self.client_address[0]   
        if contenido[-1] == "0":
            del(self.registro[usuario])
        print(self.registro)
        
        

if __name__ == "__main__": 
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)

    print("Lanzando servidor UDP de registro...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
