from flask import Flask
from flask_restplus import Api, Resource
from subprocess import Popen, PIPE

flask_app = Flask(__name__)
app = Api(app = flask_app)
name_space = app.namespace('', description='idasen API')

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


@name_space.route("/init", methods=['POST'])
class Init(Resource):
    @name_space.doc(responses={200: "Initializes idasen config file"})
    def post(self):
        print("Starting idasen init...")
        output = run_idasen_command(["init"])
        print(output)

        return output


@name_space.route("/toggle", methods=['POST'])
class Toggle(Resource):
    @name_space.doc(responses={200: "Toggles the desk position. If it's currently above 1m it will move to sitting position. Otherwise it will move to standing position"})
    def post(self):
        print("Toggling Desk Position")
        current_height = get_desk_height()

        if current_height > 1.0:
            MoveSit().post()
        else:
            MoveStand().post()

        return Height().get()


@name_space.route("/height", methods=['GET'])
class Height(Resource):
    @name_space.doc(responses={200: "The current height of the desk"})
    def get(self):
        return str(get_desk_height())


@name_space.route("/sit", methods=['POST', 'DELETE'])
class Sit(Resource):
    @name_space.doc(responses={200: "Saves current desk height as new sitting position"})
    def post(self):
        print("Saving current position as sit position")
        output = run_idasen_command(["save", "sit"])
        print(output)

        return output

    @name_space.doc(responses={200: "Deletes saved sitting position"})
    def delete(self):
        print("Delete saved sitting position")
        output = run_idasen_command(["delete", "sit"])
        print(output)

        return output


@name_space.route("/stand", methods=['POST', 'DELETE'])
class Stand(Resource):
    @name_space.doc(responses={200: "Saves current desk height as new standing position"})
    def post(self):
        print("Saving current position as standing position")
        output = run_idasen_command(["save", "stand"])
        print(output)

        return output

    @name_space.doc(responses={200: "Deletes saved standing position"})
    def delete(self):
        print("Delete saved standing position")
        output = run_idasen_command(["delete", "stand"])
        print(output)

        return output


@name_space.route("/move/sit", methods=['POST'])
class MoveSit(Resource):
    @name_space.doc(responses={200: "Moves desk to sitting position"})
    def post(self):
        print("Moving to sitting position")
        output = run_idasen_command(["sit"])
        print(output)

        return output

@name_space.route("/move/stand", methods=['POST'])
class MoveStand(Resource):
    @name_space.doc(responses={200: "Moves desk to standing position"})
    def post(self):
        print("Moving to stand position")
        output = run_idasen_command(["stand"])
        print(output)

        return output


if __name__ == '__main__':
    flask_app.run(debug=True, host='0.0.0.0')