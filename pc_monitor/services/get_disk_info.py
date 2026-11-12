import psutil

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