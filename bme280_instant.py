import smbus2
import bme280
import json

port=1
address=0x76
bus=smbus2.SMBus(port)

calibration = bme280.load_calibration_params(bus,address)

data = bme280.sample(bus,address,calibration)
out = {
	"id":str(data.id),
	"timestamp":str(data.timestamp),
	"temperature":data.temperature,
	"pressure":data.pressure,
	"humidity":data.humidity
}

print(json.dumps(out))

