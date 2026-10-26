from config import LOW_PERIOD_BOUNDARY, HIGH_PERIOD_BOUNDARY, LOW_HEIGHT_BOUNDARY, IDEAL_HEIGHT, HIGH_HEIGHT_BOUNDARY, LOW_SWELL_DIRECTION_BOUNDARY, HIGH_SWELL_DIRECTION_BOUNDARY, HEIGHT_WEIGHT, PERIOD_WEIGHT, SWELL_DIRECTION_WEIGHT, WIND_WEIGHT, MIN_SUB_SCORE
import math

def ramp(x, low, high):
    if x <= low:
        return 0
    if x >= high:
        return 1
    return (x - low) / (high - low)

def period_score(period_length):
    return ramp(period_length, LOW_PERIOD_BOUNDARY, HIGH_PERIOD_BOUNDARY)

def height_score(swell_height):
    if swell_height <= IDEAL_HEIGHT:
        return ramp(swell_height, LOW_HEIGHT_BOUNDARY, IDEAL_HEIGHT)
    return 1 - ramp(swell_height, IDEAL_HEIGHT, HIGH_HEIGHT_BOUNDARY)

def angle_diff(facing, angle):
    diff = abs(facing - angle)

    if diff > 180:
        diff = 360 - diff

    return diff

def swell_direction_score(beach_angle, swell_angle):
    diff = angle_diff(beach_angle, swell_angle)

    return 1 - ramp(diff, LOW_SWELL_DIRECTION_BOUNDARY, HIGH_SWELL_DIRECTION_BOUNDARY)

def wind_direction_score(beach_angle, wind_angle):
    diff = angle_diff(beach_angle, wind_angle)

    return (1 - math.cos(math.radians(diff))) / 2

def wind_speed_score(wind_speed):
    return 1 - ramp(wind_speed, 8, 55)

def wind_score(beach_angle, wind_angle, wind_speed):
    direction = wind_direction_score(beach_angle, wind_angle)
    speed = wind_speed_score(wind_speed)

    influence = ramp(wind_speed, 5, 20)

    direction_factor = (
        (1 - influence) + influence * direction
    )

    return direction_factor * speed

def surf_score(swell_height, swell_period, swell_angle, wind_speed, wind_angle, beach_angle):
    period = period_score(swell_period)
    height = height_score(swell_height)
    swell_direction = swell_direction_score(beach_angle, swell_angle)
    wind = wind_score(beach_angle, wind_angle, wind_speed)

    period = max(period, MIN_SUB_SCORE)
    height = max(height, MIN_SUB_SCORE)
    swell_direction = max(swell_direction, MIN_SUB_SCORE)
    wind = max(wind, MIN_SUB_SCORE)

    overall_value = (period ** PERIOD_WEIGHT) * (height ** HEIGHT_WEIGHT) * (swell_direction ** SWELL_DIRECTION_WEIGHT) * (wind ** WIND_WEIGHT)

    overall_score = round(overall_value * 100)

    return overall_score





