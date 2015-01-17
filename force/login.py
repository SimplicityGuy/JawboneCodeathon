from force import app

from flask import redirect, request, make_response
from redis import Redis

import requests
from jawbone.jawbone import Jawbone

site_root = "http://192.168.59.103"

jawbone_client_id = "KOls4_kxR_Q"
jawbone_client_secret = "d84b648530a3aa9029322c37fa77c75ce64664a4"
jawbone_redirect_uri = "{0}/authorized/jawbone".format(site_root)
scope = "basic_read,extended_read,location_read"


@app.route("/")
def index():
    return make_response("You've hit 4ce!", 200)


@app.route("/jawbone")
def root_jb():
    jb = Jawbone(jawbone_client_id,
                 jawbone_client_secret,
                 jawbone_redirect_uri,
                 scope)
    auth = jb.auth()
    return redirect(auth)


@app.route("/authorized/jawbone")
def login_jawbone():
    code = request.args.get("code")
    if not code:
        return redirect(site_root)

    jb = Jawbone(jawbone_client_id,
                 jawbone_client_secret,
                 jawbone_redirect_uri,
                 scope)

    token = jb.access_token(code)
    access_token = token["access_token"]

    headers = {"Accept": "application/json",
               "Authorization": "Bearer {0}".format(access_token)}

    response = requests.get("https://jawbone.com/nudge/api/v.1.1/users/@me",
                            headers=headers)

    redis = Redis(host="redis_1", port=6379)
    redis.incr("jawbone_hits")

    return make_response("Success! ({0})\n{1}".format(
        redis.get("jawbone_hits"), response.json()), 200)
