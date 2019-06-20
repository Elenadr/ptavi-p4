#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


PORT = int(sys.argv[1])
class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dic = {}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"Hemos recibido tu peticion")
        IPclient = self.client_address[0]
        PORTclient = self.client_address[1]
        for line in self.rfile:
            print("El cliente nos manda ", line.decode('utf-8'),IPclient, PORTclient)

if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)

    print("Lanzando servidor UDP de Sip...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
