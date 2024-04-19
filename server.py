from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

data_store = []


class AirQualityReading:
    def __init__(self, timestamp, temperature, pressure, humidity, pollution):
        self.timestamp = timestamp
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.pollution = pollution


def validate_data(data):
    temperature = data.get('temperature')
    pressure = data.get('pressure')
    humidity = data.get('humidity')

    if not (-50 <= temperature <= 50):
        return False, "Temperatura poza dopuszczalnym zakresem"
    if not (900 <= pressure <= 1100):
        return False, "Ciśnienie poza dopuszczalnym zakresem"

    if not (0 <= humidity <= 100):
        return False, "Wilgotność poza dopuszczalnym zakresem"

    return True, None


@app.route('/add', methods=['POST'])
def add_data():
    data = request.get_json()
    is_valid, error_message = validate_data(data)

    if not is_valid:
        return jsonify({"error": error_message}), 400

    timestamp = data['timestamp']
    temperature = data['temperature']
    pressure = data['pressure']
    humidity = data['humidity']
    pollution = data['pollution']

    data_store.append(AirQualityReading(timestamp, temperature, pressure, humidity, pollution))

    return jsonify({"message": "Dane dodane pomyślnie"}), 201


@app.route('/get_nearest', methods=['GET'])
def get_nearest():
    query_date = request.args.get('timestamp')
    query_date = datetime.strptime(query_date, '%Y-%m-%dT%H:%M:%S')

    nearest_reading = None
    smallest_diff = timedelta.max

    for reading in data_store:
        diff = abs(reading.timestamp - query_date)
        if diff < smallest_diff:
            smallest_diff = diff
            nearest_reading = reading

    if nearest_reading:
        response_data = {
            "timestamp": nearest_reading.timestamp.strftime('%Y-%m-%dT%H:%M:%S'),
            "temperature": nearest_reading.temperature,
            "pressure": nearest_reading.pressure,
            "humidity": nearest_reading.humidity,
            "pollution": nearest_reading.pollution
        }
        return jsonify(response_data)
    else:
        return jsonify({"error": "Brak danych w pobliżu podanej daty"}), 404


if __name__ == '__main__':
    app.run(port=5000)
