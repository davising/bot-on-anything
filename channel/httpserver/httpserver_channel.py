#!/usr/local/bin/python3

from channel.channel import Channel
from config import channel_conf
from common import const
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote
import json

class HttpServerChannel(Channel):
    def startup(self):

        hostName = channel_conf(const.HTTPSERVER).get('host')
        serverPort = channel_conf(const.HTTPSERVER).get('port')
        webServer = HTTPServer((hostName, serverPort), MyServer)
        print("Server started http://%s:%s" % (hostName, serverPort))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse the request URL to extract the query string
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        # Extract parameter from the query string
        from_user_id = query_params.get('from_user_id', [''])[0]
        context = {"from_user_id": from_user_id}
        query = query_params.get('query', [''])[0]
        query = unquote(query, encoding='utf-8')

        result = ""
        for res in Channel().build_reply_content(query, context):
            result = result + "" + res

        # Send an HTTP response
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

        # Construct the response data as a Python dictionary
        data = {
            'data': result
        }

        # Encode the response data as a JSON string
        message = json.dumps(data).encode('utf-8')
        self.wfile.write(message)


