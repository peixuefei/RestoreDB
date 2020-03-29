import paramiko
from flask import Flask

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
    for command in commands:
        print("="*50, command, "="*50)
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print(err)


app = Flask(__name__)
@app.route('/commands', methods=['POST'])
def running():
    pwd = [
        "pwd"
    ]
    execute(pwd)
    return 'Flask is running'
