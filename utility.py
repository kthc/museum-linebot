import json
from flask import jsonify
from math import radians, cos, sin, asin, sqrt

def water_filter(data, max_level=100.0, min_level=0.0):
    '''回傳符合min_level到max_level之水庫數據'''
    return [d for d in data if (float(d['level']) <= max_level) and (float(d['level']) >= min_level)]

def return_to_client_as_str(data):
    '''此為預設之回傳函數，勿動！'''
    jstr=json.dumps(data,ensure_ascii=False, sort_keys = True, indent = 4, separators = (',', ': '))
    return f'''
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <pre>{jstr}</pre>
    </body>
    </html>
    '''

def return_to_client_as_json(data):
    '''此為預設之回傳函數，勿動！'''
    jstr=json.dumps(data,ensure_ascii=False, sort_keys = True, indent = 4, separators = (',', ': ')).encode('utf8')
    return jsonify(json.loads(jstr))
    
def distance(lat1, lat2, lon1, lon2):
    '''
    d = 2R⋅sin⁻¹(√[sin²((θ₂ - θ₁)/2) + cosθ₁⋅cosθ₂⋅sin²((φ₂ - φ₁)/2)])

    where:

    θ₁, φ₁ :First point latitude and longitude coordinates;
    θ₂, φ₂ :Second point latitude and longitude coordinates;
    R :Earth's radius (R = 6371 km); and
    d : Distance between them along Earth's surface.
    '''
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return c * r
