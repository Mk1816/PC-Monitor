from dataclasses import dataclass


@dataclass(frozen=True)
class CpuMetrics:
    usage: float
    cores: int | None
    threads: int | None


@dataclass(frozen=True)
class MemoryMetrics:
    percent: float
    used: int
    available: int
    total: int


@dataclass(frozen=True)
class DiskMetrics:
    device: str
    mountpoint: str
    used: int
    free: int
    total: int
    percent: float


@dataclass(frozen=True)
class NetworkMetrics:
    sent: int
    received: int
    upload_speed: float
    download_speed: float


@dataclass(frozen=True)
class BatteryMetrics:
    percent: float | None
    plugged: bool | None


@dataclass(frozen=True)
class SystemSnapshot:
    cpu: CpuMetrics
    memory: MemoryMetrics
    disks: list[DiskMetrics]
    network: NetworkMetrics
    battery: BatteryMetrics
