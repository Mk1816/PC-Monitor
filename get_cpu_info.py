import psutil


def get_cpu_info():
    return {
        "usage": psutil.cpu_percent(interval=None),
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
    }