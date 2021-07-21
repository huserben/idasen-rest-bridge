from flask import Flask
import subprocess
from subprocess import Popen, PIPE

app = Flask(__name__)

@app.route("/init", methods=['POST'])
def init():
    process = Popen(["idasen", "init"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    return output.decode("utf-8")

@app.route("/toggle", methods=['POST'])
def toggle():
    current_height = get_height()

    if current_height > 1.0:
        print("Desk is up, will move to sitting position")
        subprocess.run(["idasen", "sit"])
    else:
        print("Desk is down, will move to standing position")
        subprocess.run(["idasen", "stand"])

    return get_height()

@app.route("/height", methods=['GET'])
def get_height():
    process = Popen(["idasen", "height"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    current_height = float(output.decode("utf-8").split(' ')[0])
    return current_height


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')