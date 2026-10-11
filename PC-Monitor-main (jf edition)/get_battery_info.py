import psutil


def get_battery_info():
    battery = psutil.sensors_battery()

    if battery is None:
        return {
            "percent": None,
            "plugged": None,
        }

    percent = battery.percent
    if percent is not None:
        percent = round(percent, 1)

    return {
        "percent": percent,
        "plugged": battery.power_plugged,
    }