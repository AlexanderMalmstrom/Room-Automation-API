#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request, url_for
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
chan_list = [2, 3, 4, 9, 10, 17, 22, 27]
GPIO.setup(chan_list, GPIO.OUT)
GPIO.output(chan_list, GPIO.HIGH)


# En array med alla GPIO portar som anvands
relays = [
	{
		'id': 1,
		'GPIO': 2,
		'type': u'Relay',
		'status': 0
	},
	{
		'id': 2,
		'GPIO': 3,
		'type': u'Relay',
		'status': 0
	},
	{
		'id': 3,
		'GPIO': 4,
		'type': u'Relay',
		'status': 0
	},
	{
		'id': 4,
		'GPIO': 9,
		'type': u'Relay',
		'status': 0
	},
	{
		'id': 5,
		'GPIO': 10,	
		'type': u'Relay',
		'status': 0
	},
	{
		'id': 6,
		'GPIO': 17,
		'type': u'Relay',
		'status': 0
	},
	{
		'id': 7,
		'GPIO': 22,
		'type': u'Relay',
		'status': 0
	},
	{
		'id': 8,
		'GPIO': 27,
		'type': u'Relay',
		'status': 0
	}
]

# Retunerar hella relays arrayen
@app.route('/auto/api/v1.0/relays', methods=['GET'])
def get_relays():
	return jsonify({'relays': relays})

# retunerar bara de med ratt id
@app.route('/auto/api/v1.0/relays/<int:relay_id>', methods=['GET'])
def get_relay(relay_id):
    relay = [relay for relay in relays if relay['id'] == relay_id]
    if len(relay) == 0:
        abort(404)
    return jsonify({'relay': relay[0]})

# Gor om http 404 till json
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not Found'}), 404)

# Updaterar status till 1 = HIGH eller 0 = LOW
@app.route('/auto/api/v1.0/relays/<int:relay_id>', methods=['PUT'])
def update_relay(relay_id):
    relay = [relay for relay in relays if relay['id'] == relay_id]
    if len(relay) == 0:
        abort(404)
    if not request.json:
        abort(400)

    status = request.json['status']
    
    if status == 1:
    	GPIO.output(relay[0]['GPIO'], GPIO.LOW)
    	relay[0]['status'] = 1
    elif status == 0:
    	GPIO.output(relay[0]['GPIO'], GPIO.HIGH)
    	relay[0]['status'] = 0
    else:
    	abort(400)
    return jsonify({'relay': relay[0]})
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=1337)
