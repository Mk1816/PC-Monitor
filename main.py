from get_cpu_info import get_cpu_info
from get_ram_info import get_ram_info
from get_disk_info import get_disk_info
from get_network_info import get_network_info
from get_battery_info import get_battery_info

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

    print("\n" + "Want to refresh? \n(y/n)")
        
    print("\n" + "=" * 40)

    while True:
        choice = input().lower()
        if choice == "y" or choice == "yes":
            main()
        elif choice == "n" or choice == "no":
            continue
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()
