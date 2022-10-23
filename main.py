import flask
from flask import request, send_file
from os import getcwd
import multiprocessing
import pyexecutor as PE
from time import sleep
#import json

UPLOAD_FOLDER = getcwd() + '/userscripts/'

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

process: multiprocessing.Process = multiprocessing.Process()
lastTB = []

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/uploadPython', methods=['POST'])
def upload():
    PE.upload_file(app, request)
    return "200 OK"

@app.route("/runPython")
def runScript():
    global lastTB
    global process
    manager = multiprocessing.Manager()
    lastTB = manager.list()
    process = multiprocessing.Process(target=PE.runUserScript, args=(lastTB,))
    process.start()
    return "Code running."

@app.route("/traceback")
def getTraceback():
    global lastTB
    if len(lastTB) > 0:
        return lastTB.pop(0)
    return ""

@app.route("/prints")
def getPrints():
    with open("userscripts/printlog.txt") as f:
        lines = f.readlines()
    return ''.join(lines)

@app.route("/stopPython")
def stopScript():
    global process
    if process is not None and process.is_alive():
        process.terminate()
        with open("userscripts/printlog.txt", "a") as file:
            file.write("---SCRIPT STOPPED---\n")
    sleep(0.1)
    return "Code stopped."
#endregion

def startFlask():
    app.run(host="localhost", port=80)  # for testing
    #app.run(host="0.0.0.0", port=80, ssl_context='adhoc') #try to auto gen?

if __name__ == '__main__':
    startFlask()