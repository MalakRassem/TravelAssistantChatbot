import requests


def geocode(place):
    payload = {'q': place,
               'format': "jsonv2",
               }
    headers = {"User-Agent": "TravelAssistantChatbot"}
    nominatim_url = "https://nominatim.openstreetmap.org/search"
    response = requests.get(nominatim_url, params=payload, headers=headers)
    if response.status_code == 200:
        try:
            return response.json()[0]["lat"], response.json()[0]["lon"]
        except:
            if response.json() == []:
                print("Location not found.")  # TODO: Exception Handling
            else:
                print("Response received from API call has unexpected structure.",
                      response.json())  # TODO: Exception Handling
    else:
        # TODO: Exception Handling
        print(f"API Request Failed. Status Code: {response.status_code}")


def weatherforecast(lat: float, lon: float, hours: int = 48):
    payload = {'latitude': lat,
               'longitude': lon,
               'hourly': "temperature_2m",
               'forecast_hours': hours,
               }
    openmeteo_url = "https://api.open-meteo.com/v1/forecast"
    response = requests.get(openmeteo_url, params=payload)
    if response.status_code == 200:
        try:
            return response.json()["hourly"]
        except:
            print("Response received from API call has unexpected structure.",
                  response.json())  # TODO: Exception Handling
    else:
        # TODO: Exception Handling
        print(f"API Request Failed. Status Code: {response.status_code}")


print(weatherforecast(*geocode("Eis-Greissler, Graz"), 4))
