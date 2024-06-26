import requests

class AirQualityClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.airvisual.com/v2"

    def get_station_air_quality(self, city: str, state: str, country: str) -> dict:
        endpoint = f"{self.base_url}/city?city={city}&state={state}&country={country}&key={self.api_key}"
        response = requests.get(endpoint)
        if response.ok:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}")

if __name__ == "__main__":
    client = AirQualityClient("001d87e0-1f3e-4a2b-9473-53bcc60ac4d0")
    try:
        air_quality_data = client.get_station_air_quality("Warsaw", "Mazovia", "Poland")
        print(air_quality_data)
    except Exception as e:
        print(f"Error: {e}")