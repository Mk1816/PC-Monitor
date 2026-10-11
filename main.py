import time
from get_cpu_info import get_cpu_info
from get_ram_info import get_ram_info
from get_disk_info import get_disk_info
from get_network_info import get_network_info, get_network_speed
from get_battery_info import get_battery_info

UPDATE_INTERVAL = 1.5


def bytes_to_gb(value):
    return value / (1024 ** 3)


def bytes_to_mb(value):
    return value / (1024 ** 2)


def print_dashboard(cpu, ram, disks, network, network_speed, battery):
    print("\033[2J\033[H", end="")
    print("=" * 40)
    print("           PC MONITOR")
    print("=" * 40)

    print("\nCPU")
    print(f"Usage:   {cpu['usage']}%")
    print(f"Cores:   {cpu['cores']}")
    print(f"Threads: {cpu['threads']}")

    print("\nRAM")
    print(f"Usage:     {ram['percent']}%")
    print(f"Used:      {bytes_to_gb(ram['used']):.2f} GB")
    print(f"Available: {bytes_to_gb(ram['available']):.2f} GB")
    print(f"Total:     {bytes_to_gb(ram['total']):.2f} GB")

    print("\nDISK")
    for index, disk in enumerate(disks, start=1):
        print(f"\nDisk {index}: {disk['mountpoint']}")
        print(f"Device: {disk['device']}")
        print(f"Usage: {disk['percent']}%")
        print(f"Used:  {bytes_to_gb(disk['used']):.2f} GB")
        print(f"Free:  {bytes_to_gb(disk['free']):.2f} GB")
        print(f"Total: {bytes_to_gb(disk['total']):.2f} GB")

    print("\nNETWORK")
    print(f"Sent:     {bytes_to_gb(network['sent']):.2f} GB")
    print(f"Received: {bytes_to_gb(network['received']):.2f} GB")
    print(f"Download Speed:  {bytes_to_mb(network_speed['download_speed']):.2f} MB/s")
    print(f"Upload Speed:    {bytes_to_mb(network_speed['upload_speed']):.2f} MB/s")

    print("\nBATTERY")
    if battery['percent'] is None:
        print("Percent: N/A")
    else:
        print(f"Percent: {battery['percent']:.1f}%")
    print(f"Plugged: {battery['plugged']}")
    print("\n" + "=" * 40)


def main():
    get_cpu_info()  # Get a baseline so the first CPU reading is meaningful.
    previous_network = get_network_info()
    previous_network_time = time.monotonic()

    try:
        time.sleep(UPDATE_INTERVAL)
        while True:
            cycle_start = time.monotonic()

            cpu = get_cpu_info()
            ram = get_ram_info()
            disks = get_disk_info()
            network = get_network_info()
            network_time = time.monotonic()
            battery = get_battery_info()

            network_speed = get_network_speed(
                previous_network,
                network,
                network_time - previous_network_time,
            )
            previous_network = network
            previous_network_time = network_time

            print_dashboard(cpu, ram, disks, network, network_speed, battery)

            elapsed_time = time.monotonic() - cycle_start
            time.sleep(max(0, UPDATE_INTERVAL - elapsed_time))
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()