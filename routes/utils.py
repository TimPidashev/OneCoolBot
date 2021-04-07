import quart
import os
import requests

app=quart.Quart("")
app.secret_key=bytes(os.environ.get("session"),"utf-8")

app.secret_key=bytes(os.urandom(24), "utf-8)

