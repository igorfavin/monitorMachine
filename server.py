#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging, json


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def realizaLog(self,hostname):
        #global hostname
        hostname = hostname + ".log"
        logging.basicConfig(filename=hostname,level=logging.DEBUG)

    def organizaDados(self,dados):
        print(dados['hostname'])

    def do_POST(self):
        #logging.basicConfig(filename=hostname,level=logging.DEBUG)
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        #Converte os dados recebidos para dict
        dados = json.loads(post_data)
        logging.info(dados)
        self.organizaDados(dados)
        #hostname = dados['hostname']#Pega o hostname para passar para o arquivo de log
        #self.realizaLog(hostname)
        #logging.info(dados['hostname'])
        #print(dados['hostname'])
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                #str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._set_response()
        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('127.0.1.2', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()