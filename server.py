import unittest
import httpclient
import http.server
import threading
import socketserver
import random
import time
import urllib.parse
import json


BASEHOST = '127.0.0.1'
#BASEPORT = 27600 + random.randint(1,100)
BASEPORT = 27600

class MyHTTPHandler(http.server.BaseHTTPRequestHandler):
    post = None
    get = None
    def do_POST(self):
        try:
            if (self.post == None):
                return None
            else:
                return self.post()
        except Exception as e:
            print("Exception %s\n" % e)
            raise e

    def do_GET(self):
        try:
            print("GET %s\n" % self.path)
            if (self.get == None):
                return None
            else:
                return self.get()
        except Exception as e:
            print("Exception %s\n" % e)
            raise e

def make_http_server(host = BASEHOST, port = BASEPORT):
    return http.server.HTTPServer( (host, port) , MyHTTPHandler)

def run_server():
    '''run the httpd server in a thread'''
    try:
        socketserver.TCPServer.allow_reuse_address = True
        http.server.HTTPServer.allow_reuse_address = True
        httpd = make_http_server()
        print("HTTP UP!\n")
        httpd.serve_forever()
        print("HTTP has been shutdown!\n")
    except Exception as e:
        print(e)
        print("run_server: Thread died")

run_server()