#!/usr/bin/env python3
# coding: utf-8
# Copyright 2022 Zhijian Mei, https://github.com/Zhijian-Mei/CMPUT404-assignment-web-client
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it
import os.path
import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse
import urllib


def help():
    print("httpclient.py [GET/POST] [URL]\n")


class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body


class HTTPClient(object):
    def get_host_port(self, url):
        host = None
        port = None
        o = urllib.parse.urlparse(url)
        for i in range(len(o.netloc)):
            if o.netloc[i] == ':':
                host = o.netloc[:i]
                port = o.netloc[i + 1:]
                break
        if not host or not port:
            host = o.netloc
            port = 80
        return host, int(port)

    def get_path(self, url):
        o = urllib.parse.urlparse(url)
        return o.path

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = int(data.split(' ')[1])
        return code

    def get_headers(self, data):
        ret = (re.search('\r\n\r\n', data)).span()
        headers = data[:ret[0]]
        return headers

    def get_body(self, data):
        ret = (re.search('\r\n\r\n',data)).span()
        body = data[ret[1]:]
        return body


    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))

    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:

            part = sock.recv(1024)

            if part:
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        host, port = self.get_host_port(url)
        path = self.get_path(url)
        if path == '':
            path += '/'
        req = 'GET' + ' ' + path + ' ' + 'HTTP/1.1\r\n'
        req += 'Host: '+ host +'\r\n'
        req += 'Accept: */*\r\n'
        req += '\r\n'
        self.connect(host, port)
        self.socket.send(req.encode('utf-8'))
        data = self.recvall(self.socket)
        code = self.get_code(data)
        body = self.get_body(data)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        host, port = self.get_host_port(url)
        path = self.get_path(url)
        length = 0
        if args:
            payload = urllib.parse.urlencode(args)
            length = len(payload)
        req = 'POST' + ' ' + path + ' ' + 'HTTP/1.1\r\n'
        req += 'Host: ' + host + '\r\n'
        req += 'Content-Type: application/x-www-form-urlencoded' + '\r\n'
        req += 'Content-Length: ' + str(length) + '\r\n'
        req += 'Accept: */*\r\n'
        req += 'Connection: keep-alive' + '\r\n'
        req += '\r\n'
        if args:
            req += payload + '\r\n\r\n'
        self.connect(host, port)
        self.socket.send(req.encode('utf-8'))
        data = self.recvall(self.socket)
        code = self.get_code(data)
        body = self.get_body(data)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST(url, command)
        else:
            return self.GET(url, command)


if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    print(sys.argv)
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command(sys.argv[2], sys.argv[1]))
    else:
        print(client.command(sys.argv[1]))
