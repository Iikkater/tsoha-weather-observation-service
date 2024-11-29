from statistics import mean, mode

def calculate_statistics(observations):
    temperatures = [obs['temperature'] for obs in observations if obs['temperature'] is not None]
    cloudiness = [obs['cloudiness'] for obs in observations if obs['cloudiness'] is not None]
    precipitation_amount = [obs['precipitation_amount'] for obs in observations if obs['precipitation_amount'] is not None]
    precipitation_type = [obs['precipitation_type'] for obs in observations if obs['precipitation_type'] is not None]

    stats = {
        'temperature': {
            'mean': mean(temperatures) if temperatures else None,
            'min': min(temperatures) if temperatures else None,
            'max': max(temperatures) if temperatures else None
        },
        'cloudiness': {
            'mode': mode(cloudiness) if cloudiness else None,
            'min': min(cloudiness) if cloudiness else None,
            'max': max(cloudiness) if cloudiness else None
        },
        'precipitation_amount': {
            'mode': mode(precipitation_amount) if precipitation_amount else None,
            'min': min(precipitation_amount) if precipitation_amount else None,
            'max': max(precipitation_amount) if precipitation_amount else None
        },
        'precipitation_type': {
            'mode': mode(precipitation_type) if precipitation_type else None,
            'min': min(precipitation_type) if precipitation_type else None,
            'max': max(precipitation_type) if precipitation_type else None
        }
    }

    return stats