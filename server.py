#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import sys
import socketserver
import time
import json

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    
    registro = {}
    def register2json(self):

            with open("registered.json", "w") as fich_json:
                data_json = json.dumps(self.registro)
                fich_json.write(data_json)

    def json2registered(self):
        try:
            with open("registered.json", "r") as fich_json:
                self.registro = json.load(fich_json)
        except:
            pass
            
    def expired_users(self):
        exp_user=[]
        for user in self.registro:
            tiempo_actual = time.strftime('%Y-%m-%d %H:%M:%S',
                                          time.gmtime(time.time()))
            if tiempo_actual >= self.registro[user][1]["expires"]:
                exp_user.append(user)
  
        for user in exp_user:        
                del(self.registro[user])

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        str_line = self.rfile.read().decode("utf-8")
        contenido = str_line.split()
        self.json2registered()
        usuario = contenido[1].split(":")[-1]
        if contenido[0] == "REGISTER":
            ip = self.client_address[0]   
            if contenido[-2] == "Expires:":
                expires = time.strftime('%Y-%m-%d %H:%M:%S',
                                            time.gmtime(time.time() +
                                                        int(contenido[-1])))
                self.registro[usuario] =[{"address": ip}, {"expires": expires}] 
        self.expired_users()
        self.register2json()
        
        self.wfile.write("SIP/2.0 200 OK\r\n\r\n".encode('utf-8'))
        

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
