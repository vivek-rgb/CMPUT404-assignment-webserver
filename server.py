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

        # only handle GET requests
        if self.get_request_type() != "GET":
            self.send_405()
            print("Error: only GET requests are supported")
            return
        
        # get the request path
        requested_path = self.get_request_path()
        print("path requested: %s" % requested_path)

        # get the path of the requested file
        # only allow files in the www and sub directories
        requested_file_path = os.path.abspath("www"+ requested_path)
        print("Requested file path: ",  requested_file_path)

        # check if the requested file is in the www directory
        if requested_path.startswith("/etc"):
            self.send_404()
            print("Error: file not found")
            return

        # check if the requested file exists
        if os.path.isfile(requested_file_path):
            http_response = f"HTTP/1.1 200 OK\r\n"
            file = open(requested_file_path ).read()
            http_response += "Content-Length: " + str(len(file))
            http_response+= "\r\n"
            http_response += f"Content-Type: {mimetypes.guess_type(requested_file_path)[0]}; charset=utf-8\r\n"

            # end of header
            http_response += "\r\n"
        
            self.request.sendall(bytearray(http_response + file,'utf-8'))
            
        

        
        # check if the requested file is a directory
        elif os.path.isdir(requested_file_path) and requested_path.endswith("/"):  
            http_response = f"HTTP/1.1 200 OK\r\n"
            # open index.html if it exists
            if os.path.isfile(requested_file_path + "/index.html"):
                file = open(requested_file_path + "/index.html").read()
                http_response += "Content-Length: " + str(len(file))
                http_response += "\r\n"
                http_response += f"Content-Type: text/html; charset=utf-8\r\n"

                # end of header
                http_response += "\r\n"

                self.request.sendall(bytearray(http_response + file,'utf-8'))
                return
            self.request.sendall(bytearray(http_response,'utf-8'))
            return           


        # check if redirection is required
        elif os.path.isdir(requested_file_path ) and not requested_path.endswith("/") :

            http_response = f"HTTP/1.1 301 Moved Permanently\r\n"
            http_response += f"Location: http://127.0.0.1:8080{requested_path}/ \r\n"
            # end of header
            http_response += "\r\n"
            self.request.sendall(bytearray(http_response,'utf-8'))
            return
        
        # file not found
        else:
            self.send_404()
            print("Error: file not found")
            return
        

    def get_request_type(self):
        print(self.data.split()[0])
        return self.data.split()[0]
    
    def get_request_path(self):
        return self.data.split()[1]
    
    def send_405(self):
        self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n\r\n",'utf-8'))

    def send_404(self):
        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n",'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
