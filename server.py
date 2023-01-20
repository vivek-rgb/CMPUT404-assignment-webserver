#  coding: utf-8 
import socketserver
import os
import mimetypes


# You will need to create a class that inherits from BaseHTTPRequestHandler
# and override the do_GET method. You will also need to create a server
# that inherits from TCPServer and pass in your request handler class.


# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip().decode('utf-8')
        print ("Got a request of: %s\n" % self.data)

        # get the request type
        request_type = self.get_request_type()

        # only handle GET requests
        if request_type != "GET":
            self.send_405()
            return
        
            
        





        self.request.sendall(bytearray("OK",'utf-8'))

    def get_request_type(self):
        return self.data.split()[0]
    
    def get_request_path(self):
        return self.data.split()[1]
    
    def send_405(self):
        self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
