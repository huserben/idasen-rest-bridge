from flask import Flask, request, abort
from flask_restplus import Api, Resource
from idasen import cli
from subprocess import Popen, PIPE
import os

flask_app = Flask(__name__)
app = Api(app = flask_app)

name_space = app.namespace('', description='idasen API')

HOME = os.path.expanduser("~")
IDASEN_CONFIG_DIRECTORY = os.path.join(HOME, ".config", "idasen")
IDASEN_CONFIG_PATH = os.path.join(IDASEN_CONFIG_DIRECTORY, "idasen.yaml")

def get_desk_height():
    print("Getting current desk height...")
    output, _, _ = run_idasen_command(["height"])
    desk_height = output.split(' ')[0]

    print(desk_height)
    return float(desk_height)


def run_idasen_command(command_arguments):
    command = ["idasen"]
    command.extend(command_arguments)

    process = Popen(command, stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    return output.decode("utf-8"), exit_code, err

def position_exists(position_name):
    config = cli.load_config()
    return position_name in config["positions"]

def get_position_height(position_name):
    config = cli.load_config()
    return config["positions"][position_name]

def move_desk_to_position(position_name):
    print("Moving to height for {0} position".format(position_name))
    cli.move_to(position=position_name)

def get_position_name():
    position_name = request.args.get('position_name')

    if (position_name == None):
        abort(400, "Missing argument position_name")

    return position_name       

@name_space.errorhandler(Exception)
def handle_exception(error):
    return {'message': "Something went wrong: {0}".format(error)}, 400

@name_space.route("/init", methods=['POST'])
class Init(Resource):
    @name_space.doc(responses={
        201: "Creates new idasen config file",
        204: "Config file already exists"})
    def post(self):
        print("Starting idasen init...")
        _, exit_code, _ = run_idasen_command(["init"])

        if (exit_code == 0):
            return IDASEN_CONFIG_PATH, 201
        else:
            return IDASEN_CONFIG_PATH, 204

@name_space.route("/toggle", methods=['POST'])
class Toggle(Resource):
    @name_space.doc(
        params={'sit_position': "The sitting position for toggling", "stand_position": "The standing position for toggling"},
        responses={
            202: "Starts moving desk to new position. If it's currently above 1m it will move to sitting position. Otherwise it will move to standing position",
            404: "Specified position for toggling does not exist"
        })
    def post(self):
        sit_position = request.args.get('sit_position', default="sit")
        stand_position = request.args.get('stand_position', default="stand")

        print("Toggling Desk Position between {0} and {1}".format(sit_position, stand_position))

        if (not position_exists(sit_position)):
            return "Position {0} does not exist".format(sit_position), 404
        elif (not position_exists(stand_position)):
            return "Position {0} does not exist".format(stand_position), 404

        current_height = get_desk_height()

        if current_height > 1.0:
            move_desk_to_position(sit_position)
            return "Moving Desk t {0}m".format(get_position_height(sit_position)), 202
        else:
            move_desk_to_position(stand_position)
            return "Moving Desk t {0}m".format(get_position_height(stand_position)), 202


@name_space.route("/height", methods=['GET', 'POST'])
class Height(Resource):
    @name_space.doc(responses={200: "The current height of the desk"})
    def get(self):
        return str(get_desk_height()), 200

    @name_space.doc(
        params={'position_name': "The position to move to"},
        responses={
            200: "Moves desk to height specified for the given position",
            400: "Position Name argument is missing",
            404: "Position does not exist"
        })
    def post(self):
        position_name = get_position_name()

        if (not position_exists(position_name)):
            return "Position {0} does not exist".format(position_name), 404
        else:
            move_desk_to_position(position_name)
            return get_position_height(position_name), 200

@name_space.route("/position", methods=['POST', 'DELETE'])
class Position(Resource):
    @name_space.doc(
        params={'position_name': "The position to save"},
        responses={
            200: "Existing Position adjusted to current desk height",
            201: "New Position created with current desk height",
            400: "Position Name argument is missing",
            500: "Save failed" })
    def post(self):
        position_name = get_position_name()

        return_code = 200
        if (not position_exists(position_name)):
            return_code = 201
        
        print("Saving current position as position for {0}".format(position_name))        
        output, exit_code, error = run_idasen_command(["save", position_name])
        if (exit_code == 0):
            return output, return_code
        else:
            return "Save failed: {0}".format(error), 500

    @name_space.doc(
        params={'position_name': "The position to delete"},
        responses={
            204: "Delete saved position for specified position",            
            400: "Position Name argument is missing",
            404: "Position does not exist",
            500: "Delete failed"})
    def delete(self):
        position_name = get_position_name()
        
        if (position_exists(position_name)):
            print("Delete saved position for {0}".format(position_name))
            output, exit_code, error = run_idasen_command(["delete", position_name])

            if (exit_code == 0):
                return output, 204
            else:
                return "Delete Failed: {0}".format(error), 500
        else:
            return "Position {0} does not exist".format(position_name), 404

if __name__ == '__main__':
    flask_app.run(debug=True, host='0.0.0.0')