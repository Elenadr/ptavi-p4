#!/usr/bin/python3
# -*- coding: utf-8 -*-


import socketserver
import sys
import time
import json


class SIPRegisterHandler(socketserver.DatagramRequestHandler):

    dic = {}

    def json2register(self):
        try:

            with open('registered.json', 'r') as jsonfile:
                self.dic = json.load(jsonfile)
        except (FileNotFoundError):
            self.dic = {}

    def time_out(self):

        lista = list(self.dic)
        for client in lista:
            time_expires = self.dic[client][1]
            time_actual = time.strftime("%Y-%m-%d %H:%M:%S",
                                        time.gmtime(time.time()))
            if time_expires < time_actual:
                del self.dic[client]

    def register2json(self):
        with open('registered.json', 'w') as archivo_json:
            json.dump(self.dic, archivo_json, sort_keys=True,
                      indent=4, separators=(',', ':'))

    def handle(self):
        self.json2register()
        print("El diccionario guardado se mostrara aqui: ", self.dic, '\r\n')
        print("")
        self.wfile.write(b"Hemos recibido tu peticion")
        for line in self.rfile:
            regis = line.decode('utf-8')
            lista_regis = regis.split(" ")
            IPclient = self.client_address[0]
            PORTclient = self.client_address[1]
            if lista_regis[0] == "REGISTER":
                user = lista_regis[1][lista_regis[1].rfind(" : ") + 1:]
                print("\n" + "--> " + "Cliente con IP " + str(IPclient) +
                      " y puerto " + str(PORTclient))
                print("\n" + "Envia: " + regis)
            elif lista_regis[0] == "Expires: ":
                expires = lista_regis[1]
                gmt_expires = time.strftime("%Y-%m-%d %H:%M:%S",
                                            time.gmtime(time.time() +
                                                        int(expires)))
                self.dic[user] = [IPclient, gmt_expires]

                print("Expire: " + expires)
                if int(expires) == 0:
                    del self.dic[user]
            self.register2json()
            self.time_out()
        print(self.dic)

if __name__ == "__main__":

    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
