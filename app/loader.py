import json

def load_forecast(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    forecast_data = []
    analysis_time = data['forecastHourly']['metadata']['analysisTime']
    postal_code = data['forecastHourly']['metadata']['area']
    for hour in data['forecastHourly']['hours']:
        forecast_data.append({
            'forecast_time': hour['forecastStart'],
            'temperature': hour['temperature'],
            'cloudiness': hour['cloudCover'],
            'precipitation_amount': hour['precipitationAmount'],
            'precipitation_type': hour['precipitationType'],
            'analysis_time': analysis_time,
            'postal_code': postal_code
        })
    
    return forecast_data