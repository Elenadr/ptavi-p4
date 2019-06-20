#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import time



class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    dic = {}

    def handle(self):
        self.wfile.write(b"Hemos recibido tu peticion")
        for line in self.rfile:
            regis = line.decode('utf-8')
            lista_regis = regis.split(" ")
            IPclient = self.client_address[0]
            PORTclient = self.client_address[1]
            if lista_regis[0] == "REGISTER":
                user= lista_regis[1][lista_regis[1].rfind(":") +1:]
                print("\n" + "Cliente con IP " + str(IPclient) + " y puerto " + str(PORTclient))
                print("\n" + "Envia: " + regis)
            elif lista_regis[0] == "Expires:":
                expires=lista_regis[1]
                self.dic[user] = [IPclient, expires]
                print("Expire: " + expires)
                if int(expires) == 0:
                    del self.dic[user]
        print(self.dic)

if __name__ == "__main__":
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)

    print("Lanzando servidor UDP de Sip...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
