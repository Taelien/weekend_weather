from fastapi import FastAPI
import requests, json, datetime, configparser

app = FastAPI()

@app.get("/{zipcode}")
async def getweekendweather(zipcode: int):
    try:
        config = configparser.ConfigParser()
        config.read_file(open(r'./config.txt'))
        api_key = config.get('CREDENTIALS', 'apikey')
        zip_code = zipcode
        country_code = 'US'
        url = f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code},{country_code}&appid={api_key}"
        res = requests.request("GET", url)
        location = json.loads(res.text)
        lat = location['lat']
        lon = location['lon']
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
        res = requests.request("GET", url)
        weather_info = json.loads(res.text)
        weekend = []
        weekend_days = ['Sat', 'Sun']
        next_week = (datetime.date.today()+datetime.timedelta(weeks=1)).strftime("%V")
        for item in weather_info['list']:
            day = datetime.datetime.fromtimestamp(item['dt']).strftime('%a')
            week = datetime.datetime.fromtimestamp(item['dt']).strftime('%V')
            if (day in weekend_days and next_week == week):
                weekend.append(item)

        message = 'Weekend info'
        if len(weekend) == 0:
            message = 'Too far away from weekend, please run this again when closer'
        elif len(weekend)/8 == 1:
            message = 'Too far away from weekend for full report, please run this again when closer'

        response_object = {'message': message, 'weekend_info': weekend}
        return response_object
    
    except Exception as e:
        return {'exception:': str(e)}
