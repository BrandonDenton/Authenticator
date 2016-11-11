#!/usr/bin/env python3
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def printJSON():
    print(request.json)
    return "success"

if __name__ == "__main__":
    app.run()
