import psutil

def get_network_info():
    network = psutil.net_io_counters()

    return {
        "sent": network.bytes_sent,
        "received": network.bytes_recv,
    }

def get_network_speed(before, after, interval):
    if interval <= 0:
        raise ValueError("interval must be greater than zero")

    return {
        "download_speed": max(0, after["received"] - before["received"]) / interval,
        "upload_speed": max(0, after["sent"] - before["sent"]) / interval,
    }