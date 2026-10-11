import psutil
import time

def get_network_info():
    network = psutil.net_io_counters()

    return {
        "sent": network.bytes_sent,
        "received": network.bytes_recv,
    }

def get_network_speed(interval=1):
    before = psutil.net_io_counters()
    time.sleep(interval)
    after = psutil.net_io_counters()

    download_speed = (after.bytes_sent - before.bytes_sent) / interval
    upload_speed = (after.bytes_recv - before.bytes_recv) / interval

    return {
        "download_speed": download_speed,
        "upload_speed": upload_speed,
    }