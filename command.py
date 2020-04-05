import paramiko
from flask import Flask, request, redirect
from flask import render_template
from flask import jsonify

hostname = "192.168.2.55"
username = "oracle"
password = "oracle"


commands = [
    "pwd",
    "id",
    "uname -a",
    "df -h"
]


def execute(commands):
    # initialize the SSH client
    client = paramiko.SSHClient()
    # add to known hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname,
                       username=username, password=password)
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()
    # execute the commands
    stdouts = {}
    for command in commands:
        print("="*50, command, "="*50)
        stdin, stdout, stderr = client.exec_command(command)
        # the byte steam is consumed by print()
        # print(stdout.read().decode())
        lines = stdout.readlines()
        # client.close()
        stdouts[command] = lines
        err = stderr.read().decode()
        if err:
            return err
    return stdouts


def single_command(command):
    client = paramiko.SSHClient()
    # add to known hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname,
                       username=username, password=password)
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()
    stdin, stdout, stderr = client.exec_command(command)
    lines = stdout.readlines()
    client.close()
    # close the connection before handling stdout
    output = ""
    for line in lines:
        output = output+line
    if output != "":
        print(output)
    else:
        print("There was no output for this command")
    stdouts = {}
    stdouts[command] = lines
    return stdouts


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/commands', methods=['POST'])
def running():
    message = request.get_json(force=True)
    pwd = [
        message['name']
    ]
    print(pwd)
    stdouts = execute(pwd)
    print(jsonify(stdouts))
    # return 'Flask is running'
    # return render_template('index.html', response=jsonify(stdouts))
    return jsonify(stdouts)
