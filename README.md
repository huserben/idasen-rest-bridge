# idasen-rest-bridge
The *idasen-rest-bridge* exposes the commands offered by the [idasen](https://github.com/newAM/idasen) python package via a REST api. This can be used to create a bridge for a device that does not support bluetooth (e.g. a Desktop PC). You can install the bridge on a device that has bluetooth support like a Raspberry Pi and then interact with the idasen desk via REST from your desktop via the raspberry pi.

## Run Server
Install dependencies:
`python -m pip install --no-cache-dir -r requirements.txt`

Then run the application:
`python main.py`

You can reach the API on port [5000 on localhost](http://localhost:5000). There is a swagger API to test out the commands.

![Swagger Overview](https://user-images.githubusercontent.com/5486874/127734589-bcb15d8f-dbb9-46f5-8781-de03f5216978.png)
![Swagger Execution](https://user-images.githubusercontent.com/5486874/127734608-02869956-7864-4eb3-a18c-b631cb911c13.png)


## Usage
Once the server is running and listening for request, you can send rest requests via any tool of choice.

The following is a *curl* command that will toggle the desk position via a server that is running on the IP 192.168.1.225:
`curl -X post http://192.168.1.225:5000/toggle`

You can also use the .[Swagger UI](http://localhost:5000) as described above.

## Setup
Before you can use any command, you must make sure the desk is connected and paired with the server.
Then you can create the config file by issuing the _init_ command - this will create a config file at `~/.config/idasen/idasen.yaml`. In this file you have to specify the mac address of the idasen desk - this currently does not work via REST api, so you have to be connected to the server directly and adjust the file.

For more details you can check out the [configuration section](https://github.com/newAM/idasen#configuration) in the idasen project.

Once this works you can should be able to get the current desk height by issuing a `GET` to `/height`. If this returns the current height, the connection works.

## Save Positions
Next you want to manually setup your standing and sitting positions by manually adjusting the desk height. Once you've found something comfortable for you, you can save the current height with `POST` requests to `/sit` and `/stand`.  

A new `POST` request to `/sit` or `/stand` will override the existing values, while a `DELETE` to those endpoints will delete the saved positions.

## Move Desk
You can move your desk to the predefined positions in two ways. Either directly to stand or move with a `POST` to `/move/sit` or `/move/stand_`. Or via `POST` to `/toggle`. Toggle will check the current desk height, and move it to the saved standing position if the current height is below 1m. If it's above it it will move it to the sitting position.

# Acknowledgements
Thanks to [newAM](https://github.com/newAM) for creating the [idasen](https://github.com/newAM/idasen) package which this REST API is fully based on.
