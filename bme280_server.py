from flask import Flask
from flask_cors import CORS, cross_origin
import flask
import smbus2
import bme280
import json

bme280_port = 1
bme280_address = 0x76
bus = smbus2.SMBus(bme280_port)

calibration = bme280.load_calibration_params(bus, bme280_address)

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-type'

live_html = '''
<!DOCTYPE html>
	<html>
	<header>
		<meta charsett='utf-8'>
		<title>BME280</title>
		<script>
			setInterval(function(){
				let ajax = new XMLHttpRequest();
				ajax.open('GET', '/json', true);
				ajax.addEventListener('load', function(){
					json = JSON.parse(this.responseText);
					if(json.temperature){
						document.getElementById('temperature').innerText = json.temperature.toFixed(2) + ' C';
					}
					if(json.pressure){
						document.getElementById('pressure').innerText = json.pressure.toFixed(2) + ' hPa';
					}
					if(json.humidity){
						document.getElementById('humidity').innerText = json.humidity.toFixed(2) + ' %';
					}
				});
				ajax.send();
			}, 1000);
		</script>
	</header>
	<body>
		<center>
			<h1>BME280</h1>
			<h3 id='temperature'></h3>
			<h3 id='pressure'></h3>
			<h3 id='humidity'></h3>
		</center>
	</body>
	</html>
'''

def bme280_sample(bus,addr,calibration):
	data = bme280.sample(bus,addr,calibration)
	return {
		"id":str(data.id),
		"timestamp":str(data.timestamp),
		"temperature":data.temperature,
		"pressure":data.pressure,
		"humidity":data.humidity
	}

@app.route('/')
def index():
	return live_html

@app.route('/json') #, methods=['GET','OPTIONS'])
@cross_origin()
def raw_json():
	#print(request.method)
	#print(request.headers)
	resp = flask.Response( json.dumps( bme280_sample(bus,bme280_address,calibration) ) )
	resp.headers['Content-type'] = 'application/json'
	#resp.headers['Access-Control-Allow-Origin'] = '*'
	#print(resp)
	return resp

if __name__ == '__main__':
	app.run(host='0.0.0.0')
