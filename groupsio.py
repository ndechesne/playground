#!/usr/bin/python3

import os
import sys
import requests
import json
from urllib.parse import urljoin
import getpass

BACKEND_URL = "https://groups.io"

def get_password():
    """
    Get the password either from the environment variable or from the
    terminal.
    """
    try:
        password = os.environ['GROUPSIO_PASSWORD']
        return password
    except KeyError:
        print("GROUPSIO_PASSWORD not set")

    password = getpass.getpass()
    if len(password) == 0:
        sys.exit(os.EX_NOPERM)

    return password

def login(email, password):
    params = {
        "email": email,
        "password": password,
        "api_key": "nonce",
    }

    url = urljoin(BACKEND_URL, "/api/v1/login")
    s = requests.Session()
    req = s.get(url, params=params)
    if req.status_code != 200:
        raise Exception("Unable to authenticate %s: %s" % (url, req.content))

    return s

def getsubs(session):
    params = {
        "limit": "50",
    }

    url = urljoin(BACKEND_URL, "/api/v1/getsubs")
    req = session.get(url, params=params)
    if req.status_code != 200:
        raise Exception("Unable to getsubs %s: %s" % (url, req.content))

    for group in req.json()['data']:
        print("Id: %d, Name: %s" % (group['group_id'], group['group_name']))

def main(email, password=None):

    if password is None:
        password = get_password()

    s = login(email, password)
    getsubs(s)

if __name__ == "__main__":
    main(*sys.argv[1:])
