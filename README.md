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

# Acknowledgements
Thanks to [newAM](https://github.com/newAM) for creating the [idasen](https://github.com/newAM/idasen) package which this REST API is fully based on.
