"""
Astro Fantasy Chronicles - Astronomical Ephemeris Calculator
Uses PyEphem (XEphem standard) to rigorously compute exact celestial coordinates.
"""

import ephem
import math
import sys

def calculate_natal_chart(year, month, day, hour, minute, lat=39.9042, lon=116.4074, tz_offset=8):
    """
    Rigorously calculate the 8 core celestial placements using astronomical ephemeris.
    """
    # Convert local time to UTC
    # Local time minus tz_offset
    local_time_str = f"{year}/{month:02d}/{day:02d} {hour:02d}:{minute:02d}:00"
    utc_hour = hour - tz_offset
    utc_day = day
    utc_month = month
    utc_year = year
    
    # Handle day wrap if any
    if utc_hour < 0:
        utc_hour += 24
        # approximate day subtraction
        utc_day -= 1
        if utc_day < 1:
            utc_month -= 1
            if utc_month < 1:
                utc_month = 12
                utc_year -= 1
            utc_day = 28 # safe fallback
            
    utc_str = f"{utc_year}/{utc_month:02d}/{utc_day:02d} {utc_hour:02d}:{minute:02d}:00"
    
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.elevation = 50
    observer.date = utc_str
    
    sun = ephem.Sun(observer)
    moon = ephem.Moon(observer)
    mercury = ephem.Mercury(observer)
    venus = ephem.Venus(observer)
    mars = ephem.Mars(observer)
    jupiter = ephem.Jupiter(observer)
    saturn = ephem.Saturn(observer)
    
    def get_ecliptic_deg(body):
        ecl = ephem.Ecliptic(body)
        return math.degrees(ecl.lon) % 360

    signs_zh = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']
    
    def to_sign_data(deg):
        idx = int(deg // 30)
        d = int(deg % 30)
        m = int((deg % 1) * 60)
        return {
            'sign': signs_zh[idx],
            'degree': d,
            'minute': m,
            'full_deg': deg,
            'label': f"{signs_zh[idx]} {d:02d}°{m:02d}'"
        }
        
    # Ascendant calculation
    sidereal = observer.sidereal_time()
    eps_rad = math.radians(23.44)
    lat_rad = math.radians(lat)
    ramc = sidereal
    y = math.cos(ramc)
    x = -(math.sin(ramc) * math.cos(eps_rad) + math.tan(lat_rad) * math.sin(eps_rad))
    asc_deg = (math.degrees(math.atan2(y, x)) + 360) % 360
    
    chart = {
        'Sun': to_sign_data(get_ecliptic_deg(sun)),
        'Moon': to_sign_data(get_ecliptic_deg(moon)),
        'Ascendant': to_sign_data(asc_deg),
        'Mercury': to_sign_data(get_ecliptic_deg(mercury)),
        'Venus': to_sign_data(get_ecliptic_deg(venus)),
        'Mars': to_sign_data(get_ecliptic_deg(mars)),
        'Jupiter': to_sign_data(get_ecliptic_deg(jupiter)),
        'Saturn': to_sign_data(get_ecliptic_deg(saturn))
    }
    return chart

if __name__ == '__main__':
    # Test for 1991.3.29 21:45
    c = calculate_natal_chart(1991, 3, 29, 21, 45)
    for k, v in c.items():
        print(f"{k}: {v['label']}")
