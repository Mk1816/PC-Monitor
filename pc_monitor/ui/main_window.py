import logging
import time

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from pc_monitor.config import UPDATE_INTERVAL_SECONDS
from pc_monitor.models import SystemSnapshot
from pc_monitor.services.system_monitor import SystemMonitor
from pc_monitor.ui.theme import APP_STYLESHEET
from pc_monitor.ui.widgets import DiskCard, GaugeCard, NetworkCard, bytes_to_gb


class MainWindow(QMainWindow):
    def __init__(
        self, monitor: SystemMonitor | None = None, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.monitor = monitor or SystemMonitor()
        self.setWindowTitle("PC Monitor")
        self.resize(1040, 760)
        self.setMinimumSize(760, 600)

        self._build_ui()
        self._timer = QTimer(self)
        self._timer.setInterval(round(UPDATE_INTERVAL_SECONDS * 1000))
        self._timer.timeout.connect(self.refresh)
        self._timer.start()
        QTimer.singleShot(0, self.refresh)

    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("central")
        root = QVBoxLayout(central)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(20)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("PC MONITOR")
        title.setObjectName("title")
        subtitle = QLabel("Состояние системы в реальном времени")
        subtitle.setObjectName("subtitle")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()

        self.updated_label = QLabel("Ожидание данных")
        self.updated_label.setObjectName("updated")
        self.status_label = QLabel("●  Запуск мониторинга")
        self.status_label.setObjectName("status")
        header.addWidget(self.updated_label, alignment=Qt.AlignmentFlag.AlignRight)
        header.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignRight)
        root.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        content.setObjectName("scrollContent")
        grid = QGridLayout(content)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(16)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        self.cpu_card = GaugeCard("Процессор")
        self.ram_card = GaugeCard("Оперативная память")
        self.network_card = NetworkCard()
        self.battery_card = GaugeCard("Батарея")
        self.disk_card = DiskCard()
        grid.addWidget(self.cpu_card, 0, 0)
        grid.addWidget(self.ram_card, 0, 1)
        grid.addWidget(self.network_card, 1, 0)
        grid.addWidget(self.battery_card, 1, 1)
        grid.addWidget(self.disk_card, 2, 0, 1, 2)

        scroll.setWidget(content)
        root.addWidget(scroll)
        self.setCentralWidget(central)
        self.setStyleSheet(APP_STYLESHEET)

    def refresh(self) -> None:
        try:
            snapshot = self.monitor.collect()
        except Exception as error:
            logging.exception("Failed to refresh system metrics")
            self.status_label.setText("●  Ошибка обновления")
            self.status_label.setStyleSheet("color: #ff7b83;")
            self.statusBar().showMessage(f"Не удалось получить данные: {error}")
            return

        self._update_view(snapshot)

    def _update_view(self, snapshot: SystemSnapshot) -> None:
        self.cpu_card.set_metrics(
            f"{snapshot.cpu.usage:.0f}%",
            snapshot.cpu.usage,
            f"Ядра: {snapshot.cpu.cores}   ·   Потоки: {snapshot.cpu.threads}",
        )
        self.ram_card.set_metrics(
            f"{snapshot.memory.percent:.0f}%",
            snapshot.memory.percent,
            f"Использовано: {bytes_to_gb(snapshot.memory.used):.1f} ГБ   ·   "
            f"Доступно: {bytes_to_gb(snapshot.memory.available):.1f} ГБ   ·   "
            f"Всего: {bytes_to_gb(snapshot.memory.total):.1f} ГБ",
        )
        self.network_card.set_metrics(
            snapshot.network.download_speed,
            snapshot.network.upload_speed,
            snapshot.network.received,
            snapshot.network.sent,
        )
        self._update_battery(snapshot)
        self.disk_card.set_disks(snapshot.disks)
        self.updated_label.setText(f"Обновлено в {time.strftime('%H:%M:%S')}")
        self.status_label.setText("●  Мониторинг активен")
        self.status_label.setStyleSheet("color: #5cdda5;")
        self.statusBar().clearMessage()

    def _update_battery(self, snapshot: SystemSnapshot) -> None:
        battery = snapshot.battery
        if battery.percent is None:
            self.battery_card.set_metrics(
                "Нет батареи", 0, "Устройство работает от сети"
            )
            return

        if battery.plugged is None:
            power_state = "статус неизвестен"
        elif battery.plugged:
            power_state = "заряжается"
        else:
            power_state = "не подключена к сети"
        self.battery_card.set_metrics(
            f"{battery.percent:.0f}%",
            battery.percent,
            f"Состояние питания: {power_state}",
        )
