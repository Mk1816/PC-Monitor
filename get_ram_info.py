
import psutil


def get_ram_info():
    ram = psutil.virtual_memory()

    return {
        "total": ram.total,
        "used": ram.used,
        "available": ram.available,
        "percent": ram.percent,
    }