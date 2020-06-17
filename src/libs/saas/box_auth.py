# coding: utf-8

from __future__ import print_function, unicode_literals

import bottle
import os
import json
from threading import Thread, Event
import webbrowser
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server

from boxsdk import OAuth2

creds_file = os.path.abspath(os.path.join('..', "credentials/credentials_box.json"))
with open(creds_file, 'r') as f:
    json_data = json.loads(f.read())
    CLIENT_ID = json_data["ClientID"]
    CLIENT_SECRET = json_data["ClientSecret"]

def authenticate_one_time(oauth_class=OAuth2):
    class StoppableWSGIServer(bottle.ServerAdapter):
        def __init__(self, *args, **kwargs):
            super(StoppableWSGIServer, self).__init__(*args, **kwargs)
            self._server = None

        def run(self, app):
            server_cls = self.options.get('server_class', WSGIServer)
            handler_cls = self.options.get('handler_class', WSGIRequestHandler)
            self._server = make_server(self.host, self.port, app, server_cls, handler_cls)
            self._server.serve_forever()

        def stop(self):
            self._server.shutdown()

    auth_code = {}
    auth_code_is_available = Event()

    local_oauth_redirect = bottle.Bottle()

    @local_oauth_redirect.get('/')
    def get_token():
        auth_code['auth_code'] = bottle.request.query.code
        auth_code['state'] = bottle.request.query.state
        auth_code_is_available.set()

    local_server = StoppableWSGIServer(host='localhost', port=8080)
    server_thread = Thread(target=lambda: local_oauth_redirect.run(server=local_server))
    server_thread.start()

    oauth = oauth_class(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )
    auth_url, csrf_token = oauth.get_authorization_url('http://localhost:8080')
    webbrowser.open(auth_url)

    auth_code_is_available.wait()
    local_server.stop()
    assert auth_code['state'] == csrf_token
    access_token, refresh_token = oauth.authenticate(auth_code['auth_code'])

    print('access_token: ' + access_token)
    print('refresh_token: ' + refresh_token)

    return oauth, access_token, refresh_token


def authenticate_with_tokens(client_id, client_secret, access_token, refresh_token):
    """Login to box using credentials
        :arg
          creds_file: ClientID, ClientSecret & Access Token

        :returns
          client: Box API session instance
        """

    try:
        oauth = OAuth2(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            refresh_token=refresh_token
        )
        return oauth

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

