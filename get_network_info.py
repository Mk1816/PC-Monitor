import psutil


def get_network_info():
    network = psutil.net_io_counters()

    return {
        "sent": network.bytes_sent,
        "received": network.bytes_recv,
    }
