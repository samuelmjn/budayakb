import os
import json

from cas import CASClient
from flask import current_app as app


def get_cas_client(service_url=None, request=None):
    server_url = f"{app.config['SSO_UI_URL']}"
    if server_url and request and server_url.startswith("/"):
        scheme = request.headers.get("X-Forwarded-Proto", request.scheme)
        server_url = scheme + "://" + request.headers["HTTP_HOST"] + server_url

    return CASClient(service_url=service_url, server_url=server_url, version=2)


def authenticate(ticket, client):
    username, attributes, a = client.verify_ticket(ticket)
    print(username, attributes, a)

    if not username:
        return None

    sso_profile = {"username": username, "attributes": attributes}
    return sso_profile