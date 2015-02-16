__author__ = 'Shane DiNozzo'

try:
    # noinspection PyUnresolvedReferences
    import pywapi
except ImportError:
    print('The pywapi module not found! Please install it!')
    exit()


def get_weather(location):
    location_getter = pywapi.get_loc_id_from_weather_com(location)
    city = location_getter[0][1]
    # print(city)
    location_id = location_getter[0][0]
    # print(location_id)
    weather = pywapi.get_weather_from_weather_com(location_id)
    cur_weather_temp = weather['current_conditions']['temperature']
    cur_weather_text = weather['current_conditions']['text']
    cur_weather_windspeed = weather['current_conditions']['wind']['speed']
    cur_weather_windtext = weather['current_conditions']['wind']['text']
    weather_last_updated = weather['current_conditions']['last_updated']
    weather_humidity = weather['current_conditions']['humidity']
    weather_station = weather['current_conditions']['station']
    weather_felslike = weather['current_conditions']['feels_like']
    # print(weather.keys())
    # print('[%s]' % ', '.join(map(str, weather['current_conditions']['wind'])))
    print('[%s]' % ', '.join(map(str, weather['current_conditions']['feels_like'])))
    # print(cur_weather_windtext)
    # print('[%s]' % ', '.join(map(str, weather['forecasts'])))

    '''try:
        print(
            '\n' + city + " : \nHőmérséklet: " + cur_weather_temp + "°C, " + cur_weather_text +
            "\nSzél: " + cur_weather_windspeed + " km/h\n")
    except KeyError:
        print('City not found!')'''


get_weather('Győr')
