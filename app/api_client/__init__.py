from flask import current_app
from potion_client import Client
from potion_client.auth import HTTPBearerAuth

api_clients = {}


def create_api(token):

    if not token in api_clients:
        api_clients[token] = Client(current_app.config.get('API_ROUTE'), auth=HTTPBearerAuth(token))

    return api_clients[token]

def delete_api(token):
    if token in api_clients:
        api_clients.pop(token)
