import sys
import time
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pc_monitor.models import (
    BatteryMetrics,
    CpuMetrics,
    DiskMetrics,
    MemoryMetrics,
    NetworkMetrics,
    SystemSnapshot,
)
from pc_monitor.services.get_battery_info import get_battery_info
from pc_monitor.services.get_cpu_info import get_cpu_info
from pc_monitor.services.get_disk_info import get_disk_info
from pc_monitor.services.get_network_info import get_network_info, get_network_speed
from pc_monitor.services.get_ram_info import get_ram_info


class SystemMonitor:
    """Collects and combines metrics from the system information providers."""

    def __init__(self) -> None:
        self._previous_network = get_network_info()
        self._previous_network_time = time.monotonic()
        get_cpu_info()

    def collect(self) -> SystemSnapshot:
        cpu = get_cpu_info()
        memory = get_ram_info()
        disks = get_disk_info()
        network = get_network_info()
        network_time = time.monotonic()
        network_speed = get_network_speed(
            self._previous_network,
            network,
            network_time - self._previous_network_time,
        )
        battery = get_battery_info()

        self._previous_network = network
        self._previous_network_time = network_time

        return SystemSnapshot(
            cpu=CpuMetrics(**cpu),
            memory=MemoryMetrics(**memory),
            disks=[DiskMetrics(**disk) for disk in disks],
            network=NetworkMetrics(**network, **network_speed),
            battery=BatteryMetrics(**battery),
        )
