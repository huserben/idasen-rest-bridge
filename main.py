from flask import Flask
import subprocess
from subprocess import Popen, PIPE

app = Flask(__name__)


@app.route("/init", methods=['POST'])
def init():
    print("Starting idasen init...")
    output = run_idasen_command(["init"])
    print(output)

    return output


@app.route("/toggle", methods=['POST'])
def toggle():
    print("Toggling Desk Position")
    current_height = get_desk_height()

    if current_height > 1.0:
        move_sit()
    else:
        move_stand()

    return get_height()


@app.route("/height", methods=['GET'])
def get_height():
    return str(get_desk_height())


@app.route("/move/sit", methods=['POST'])
def move_sit():
    print("Moving to sitting position")
    output = run_idasen_command(["sit"])
    print(output)

    return output


@app.route("/sit", methods=['POST'])
def save_sit():
    print("Saving current position as sit position")
    output = run_idasen_command(["save", "sit"])
    print(output)

    return output


@app.route("/sit", methods=['DELETE'])
def delete_sit():
    print("Delete saved sitting position")
    output = run_idasen_command(["delete", "sit"])
    print(output)

    return output


@app.route("/stand", methods=['POST'])
def save_stand():
    print("Saving current position as standing position")
    output = run_idasen_command(["save", "stand"])
    print(output)

    return output


@app.route("/stand", methods=['DELETE'])
def delete_stand():
    print("Delete saved standing position")
    output = run_idasen_command(["delete", "stand"])
    print(output)

    return output


@app.route("/move/stand", methods=['POST'])
def move_stand():
    print("Moving to stand position")
    output = run_idasen_command(["stand"])
    print(output)

    return output


def get_desk_height():
    print("Getting current desk height...")
    output = run_idasen_command(["height"])
    desk_height = output.split(' ')[0]

    print(desk_height)
    return float(desk_height)


def run_idasen_command(command_arguments):
    command = ["idasen"]
    command.extend(command_arguments)

    process = Popen(command, stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    return output.decode("utf-8")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
