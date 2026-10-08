import psutil


def get_cpu_info():
    return {
        "usage": psutil.cpu_percent(interval=1),
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
    }


def get_ram_info():
    ram = psutil.virtual_memory()

    return {
        "total": ram.total,
        "used": ram.used,
        "available": ram.available,
        "percent": ram.percent,
    }


def get_disk_info():
    disk = psutil.disk_usage("/")

    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent,
    }


def get_network_info():
    network = psutil.net_io_counters()

    return {
        "sent": network.bytes_sent,
        "received": network.bytes_recv,
    }


def bytes_to_gb(value):
    return value / (1024 ** 3)


def main():
    print("=" * 40)
    print("           PC MONITOR")
    print("=" * 40)

    # CPU
    cpu = get_cpu_info()

    print("\nCPU")
    print(f"Usage:   {cpu['usage']}%")
    print(f"Cores:   {cpu['cores']}")
    print(f"Threads: {cpu['threads']}")

    # RAM
    ram = get_ram_info()

    print("\nRAM")
    print(f"Usage:     {ram['percent']}%")
    print(f"Used:      {bytes_to_gb(ram['used']):.2f} GB")
    print(f"Available: {bytes_to_gb(ram['available']):.2f} GB")
    print(f"Total:     {bytes_to_gb(ram['total']):.2f} GB")

    # Disk
    disk = get_disk_info()

    print("\nDISK")
    print(f"Usage: {disk['percent']}%")
    print(f"Used:  {bytes_to_gb(disk['used']):.2f} GB")
    print(f"Free:  {bytes_to_gb(disk['free']):.2f} GB")
    print(f"Total: {bytes_to_gb(disk['total']):.2f} GB")

    # Network
    network = get_network_info()

    print("\nNETWORK")
    print(f"Sent:     {bytes_to_gb(network['sent']):.2f} GB")
    print(f"Received: {bytes_to_gb(network['received']):.2f} GB")

    print("\n" + "=" * 40)


if __name__ == "__main__":
    main()