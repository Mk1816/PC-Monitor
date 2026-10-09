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
    virtual_filesystems = {
        "proc",
        "sysfs",
        "tmpfs",
        "devtmpfs",
        "devpts",
        "securityfs",
        "cgroup",
        "cgroup2",
        "pstore",
        "bpf",
        "fusectl",
        "hugetlbfs",
        "mqueue",
        "debugfs",
        "tracefs",
        "efivarfs",
        "autofs",
        "overlay",
        "aufs",
    }

    disks = []

    for partition in psutil.disk_partitions(all=True):
        if partition.fstype.lower() in virtual_filesystems:
            continue

        if partition.mountpoint.startswith(("/proc", "/sys", "/dev", "/run")):
            continue

        try:
            usage = psutil.disk_usage(partition.mountpoint)
        except OSError:
            continue

        disks.append({
            "device": partition.device,
            "mountpoint": partition.mountpoint,
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": usage.percent,
        })

    return disks


def get_network_info():
    network = psutil.net_io_counters()

    return {
        "sent": network.bytes_sent,
        "received": network.bytes_recv,
    }

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
    disks = get_disk_info()

    print("\nDISK")
    for index, disk in enumerate(disks, start=1):
        print(f"\nDisk {index}: {disk['mountpoint']}")
        print(f"Device: {disk['device']}")
        print(f"Usage: {disk['percent']}%")
        print(f"Used:  {bytes_to_gb(disk['used']):.2f} GB")
        print(f"Free:  {bytes_to_gb(disk['free']):.2f} GB")
        print(f"Total: {bytes_to_gb(disk['total']):.2f} GB")

    # Network
    network = get_network_info()

    print("\nNETWORK")
    print(f"Sent:     {bytes_to_gb(network['sent']):.2f} GB")
    print(f"Received: {bytes_to_gb(network['received']):.2f} GB")

    # Battery
    battery = get_battery_info()

    print("\nBATTERY")
    if battery['percent'] is None:
        print("Percent: N/A")
    else:
        print(f"Percent: {battery['percent']:.1f}%")
    print(f"Plugged: {battery['plugged']}")

    
    print("\n" + "=" * 40)

if __name__ == "__main__":
    main()