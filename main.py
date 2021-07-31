from flask import Flask, request, abort
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

def get_position_name():
    position_name = request.args.get('position_name')

    if (position_name == None):
        abort(400, "Missing argument position_name")

    return position_name       


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
    @name_space.doc(
        params={'sit_position': "The sitting position for toggling", "stand_position": "The standing position for toggling"},
        responses={200: "Toggles the desk position. If it's currently above 1m it will move to sitting position. Otherwise it will move to standing position"})
    def post(self):
        sit_position = request.args.get('sit_position', default="sit")
        stand_position = request.args.get('stand_position', default="stand")

        print("Toggling Desk Position between {0} and {1}".format(sit_position, stand_position))
        current_height = get_desk_height()

        if current_height > 1.0:
            Position().put(sit_position)
        else:
            Position().put(stand_position)

        return Height().get()


@name_space.route("/height", methods=['GET'])
class Height(Resource):
    @name_space.doc(responses={200: "The current height of the desk"})
    def get(self):
        return str(get_desk_height())


@name_space.route("/position", methods=['POST', 'PUT', 'DELETE'])
class Position(Resource):
    @name_space.doc(
        params={'position_name': "The position to save"},
        responses={200: "Save current desk height for specified position"})
    def post(self):
        position_name = get_position_name()

        print("Saving current position as position for {0}".format(position_name))
        output = run_idasen_command(["save", position_name])
        print(output)

        return output

    @name_space.doc(
        params={'position_name': "The position to delete"},
        responses={200: "Delete saved position for specified position"})
    def delete(self):
        position_name = get_position_name()
        print("Delete saved position for {0}".format(position_name))
        output = run_idasen_command(["delete", position_name])
        print(output)

        return output

    @name_space.doc(
        params={'position_name': "The position to move to"},
        responses={200: "Moves desk to height specified for the given position"})
    def put(self):
        position_name = get_position_name()
        print("Moving to heigh for {0} position".format(position_name))
        output = run_idasen_command([position_name])
        print(output)

        return output


if __name__ == '__main__':
    flask_app.run(debug=True, host='0.0.0.0')