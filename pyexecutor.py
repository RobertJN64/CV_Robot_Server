import traceback
from flask import flash
from os import getcwd, path
from time import sleep
import requests

try:
    from CONFIG_CV_ROBOT import robot_URL

    is_Robot = True
except ImportError:
    robot_URL = "0.0.0.0"
    is_Robot = False

def stop_robot():
    if is_Robot:
        try:
            requests.get('http://' + robot_URL + '/stop')
        except (Exception,):
            with open("userscripts/printlog.txt", "a") as f:
                f.write("---COULD NOT STOP ROBOT---\n")

ALLOWED_EXTENSIONS = {'py'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def formatTraceback(tb):
    traces = tb.split('\n')
    traces.pop(1)
    traces.pop(1)
    trace = '\n'.join(traces)
    directory = getcwd() + '/userscripts/UserScript.py'
    trace = trace.replace(path.abspath(directory), "User_Submitted_Code")
    return trace

def swapTabSpace(file):
    with open(file) as f:
        lines = f.readlines()
    for i in range(0, len(lines)):
        lines[i] = lines[i].replace("	", "    ")
    with open(file, "w+") as f:
        f.write("from CV_Robot import robot\n")
        f.write("from CV_Robot import vision\n")
        f.write("from time import sleep\n")
        f.write("from printlog import printlog as print\n")
        f.writelines(lines)
        f.write("\nrobot.stop()")

def runUserScript(tb):
    try:
        with open("userscripts/printlog.txt", "w+") as file:
            file.write("---SCRIPT STARTING---\n")
        swapTabSpace("userscripts/UserScript.py")
        import userscripts.UserScript
        with open("userscripts/printlog.txt", "a") as f:
            f.write("---SCRIPT FINISHED---\n")

    except ImportError:
        trace = traceback.format_exc()
        traces = trace.split('\n')
        if traces[-2] != "ModuleNotFoundError: No module named 'userscripts.UserScript'":
            with open("userscripts/printlog.txt", "a") as f:
                f.write("---ERROR---\n")
            tb.append(formatTraceback(trace))
            print("Error in user script:")
            print(tb[0])
        else:
            print("Error. Demo script not found.")
            tb.append("Error. No script found. Try redownloading, or this might be an internal server issue.")
    except (Exception,):
        stop_robot()
        with open("userscripts/printlog.txt", "a") as f:
            f.write("---ERROR---\n")
        print("Error in user script:")
        trace = traceback.format_exc()
        tb.append(formatTraceback(trace))
        print(tb[0])
    sleep(0.1)

def upload_file(app, request):
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return "No file"
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return "No file"
    if file and allowed_file(file.filename):
        file.save(path.join(app.config['UPLOAD_FOLDER'], "UserScript.py"))
        return "200 OK"
    print(file.filename)
    print(file.stream.readlines())
    return "Invalid filename"