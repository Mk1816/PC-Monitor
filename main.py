import logging
import time

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QProgressBar,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

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

#CPU
    print("\nCPU")
    print(f"Usage:   {cpu['usage']}%")
    print(f"Cores:   {cpu['cores']}")
    print(f"Threads: {cpu['threads']}")

#RAM
    print("\nRAM")
    print(f"Usage:     {ram['percent']}%")
    print(f"Used:      {bytes_to_gb(ram['used']):.2f} GB")
    print(f"Available: {bytes_to_gb(ram['available']):.2f} GB")
    print(f"Total:     {bytes_to_gb(ram['total']):.2f} GB")

#Disks
    print("\nDISK")
    for index, disk in enumerate(disks, start=1):
        print(f"\nDisk {index}: {disk['mountpoint']}")
        print(f"Device: {disk['device']}")
        print(f"Usage: {disk['percent']}%")
        print(f"Used:  {bytes_to_gb(disk['used']):.2f} GB")
        print(f"Free:  {bytes_to_gb(disk['free']):.2f} GB")
        print(f"Total: {bytes_to_gb(disk['total']):.2f} GB")

#Network
    print("\nNETWORK")
    print(f"Sent:     {bytes_to_gb(network['sent']):.2f} GB")
    print(f"Received: {bytes_to_gb(network['received']):.2f} GB")
    print(f"Download Speed:  {bytes_to_mb(network_speed['download_speed']):.2f} MB/s")
    print(f"Upload Speed:    {bytes_to_mb(network_speed['upload_speed']):.2f} MB/s")

#Battery
    print("\nBATTERY")
    if battery['percent'] is None:
        print("Percent: N/A")
    else:
        print(f"Percent: {battery['percent']:.1f}%")
    print(f"Plugged: {battery['plugged']}")
    print("\n" + "=" * 40)


class MonitorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PC Monitor")
        self.resize(1040, 760)
        self.setMinimumSize(760, 600)

        self.previous_network = get_network_info()
        self.previous_network_time = time.monotonic()
        get_cpu_info()

        self._build_ui()

        self.timer = QTimer(self)
        self.timer.setInterval(int(UPDATE_INTERVAL * 1000))
        self.timer.timeout.connect(self.refresh)
        self.timer.start()
        QTimer.singleShot(0, self.refresh)

    def _build_ui(self):
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

        self.status_label = QLabel("●  Запуск мониторинга")
        self.status_label.setObjectName("status")
        self.updated_label = QLabel("Ожидание данных")
        self.updated_label.setObjectName("updated")
        header.addWidget(self.updated_label, alignment=Qt.AlignmentFlag.AlignRight)
        header.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignRight)
        root.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        grid = QGridLayout(content)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(16)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

        self.cpu_value, self.cpu_bar, cpu_card = self._make_gauge_card("Процессор")
        self.cpu_details = QLabel("Ядра: —   Потоки: —")
        self.cpu_details.setObjectName("detail")
        cpu_card.layout().addWidget(self.cpu_details)
        grid.addWidget(cpu_card, 0, 0)

        self.ram_value, self.ram_bar, ram_card = self._make_gauge_card(
            "Оперативная память"
        )
        self.ram_details = QLabel("Использовано: —")
        self.ram_details.setObjectName("detail")
        ram_card.layout().addWidget(self.ram_details)
        grid.addWidget(ram_card, 0, 1)

        network_card, self.download_value, self.upload_value = self._make_network_card()
        grid.addWidget(network_card, 1, 0)

        self.battery_value, self.battery_bar, battery_card = self._make_gauge_card(
            "Батарея"
        )
        self.battery_details = QLabel("Состояние питания: —")
        self.battery_details.setObjectName("detail")
        battery_card.layout().addWidget(self.battery_details)
        grid.addWidget(battery_card, 1, 1)

        self.disk_rows, disk_card = self._make_disk_card()
        grid.addWidget(disk_card, 2, 0, 1, 2)

        scroll.setWidget(content)
        root.addWidget(scroll)
        self.setCentralWidget(central)
        self.setStyleSheet(
            """
            QMainWindow, QWidget#central {
                background: #0c111b;
                color: #e8edf6;
                font-family: "Inter", "Segoe UI", sans-serif;
            }
            QLabel#title { color: #f3f6fc; font-size: 25px; font-weight: 700; }
            QLabel#subtitle, QLabel#updated, QLabel#detail {
                color: #8995a9;
                font-size: 12px;
            }
            QLabel#status { color: #5cdda5; font-size: 12px; padding-left: 18px; }
            QFrame#card {
                background: #151d2b;
                border: 1px solid #253148;
                border-radius: 14px;
            }
            QLabel#cardTitle { color: #aeb9ca; font-size: 13px; font-weight: 600; }
            QLabel#value { color: #f3f6fc; font-size: 30px; font-weight: 700; }
            QLabel#networkValue { color: #f3f6fc; font-size: 20px; font-weight: 650; }
            QProgressBar {
                background: #263248;
                border: none;
                border-radius: 5px;
                height: 10px;
                text-align: center;
            }
            QProgressBar::chunk { background: #63a7ff; border-radius: 5px; }
            QScrollArea { background: transparent; }
            """
        )

    @staticmethod
    def _new_card(title):
        card = QFrame()
        card.setObjectName("card")
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)
        heading = QLabel(title)
        heading.setObjectName("cardTitle")
        layout.addWidget(heading)
        return card, layout

    def _make_gauge_card(self, title):
        card, layout = self._new_card(title)
        value = QLabel("—%")
        value.setObjectName("value")
        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(0)
        bar.setTextVisible(False)
        layout.addWidget(value)
        layout.addWidget(bar)
        return value, bar, card

    def _make_network_card(self):
        card, layout = self._new_card("Сеть")
        self.download_value = QLabel("↓  — MB/s")
        self.download_value.setObjectName("networkValue")
        self.upload_value = QLabel("↑  — MB/s")
        self.upload_value.setObjectName("networkValue")
        self.network_totals = QLabel("Получено: —   Отправлено: —")
        self.network_totals.setObjectName("detail")
        layout.addWidget(self.download_value)
        layout.addWidget(self.upload_value)
        layout.addWidget(self.network_totals)
        return card, self.download_value, self.upload_value

    def _make_disk_card(self):
        card, layout = self._new_card("Накопители")
        rows = QVBoxLayout()
        rows.setSpacing(14)
        layout.addLayout(rows)
        return rows, card

    def _update_disks(self, disks):
        self._clear_layout(self.disk_rows)

        if not disks:
            empty = QLabel("Подключённые накопители не найдены")
            empty.setObjectName("detail")
            self.disk_rows.addWidget(empty)
            return

        for index, disk in enumerate(disks, start=1):
            row = QVBoxLayout()
            row.setSpacing(7)
            heading = QLabel(f"Диск {index} · {disk['mountpoint']}")
            heading.setObjectName("cardTitle")
            usage = QProgressBar()
            usage.setRange(0, 100)
            usage.setValue(round(disk["percent"]))
            usage.setTextVisible(False)
            details = QLabel(
                f"{disk['device']}   ·   "
                f"{bytes_to_gb(disk['used']):.1f} / "
                f"{bytes_to_gb(disk['total']):.1f} ГБ   ·   "
                f"свободно {bytes_to_gb(disk['free']):.1f} ГБ"
            )
            details.setObjectName("detail")
            row.addWidget(heading)
            row.addWidget(usage)
            row.addWidget(details)
            self.disk_rows.addLayout(row)

    @classmethod
    def _clear_layout(cls, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()
            elif item.layout() is not None:
                cls._clear_layout(item.layout())
                item.layout().deleteLater()

    @staticmethod
    def _format_speed(bytes_per_second):
        if bytes_per_second >= 1024 ** 2:
            return f"{bytes_per_second / (1024 ** 2):.2f} MB/s"
        if bytes_per_second >= 1024:
            return f"{bytes_per_second / 1024:.1f} KB/s"
        return f"{bytes_per_second:.0f} B/s"

    def refresh(self):
        try:
            cpu = get_cpu_info()
            ram = get_ram_info()
            disks = get_disk_info()
            network = get_network_info()
            network_time = time.monotonic()
            network_speed = get_network_speed(
                self.previous_network,
                network,
                network_time - self.previous_network_time,
            )
            battery = get_battery_info()
        except Exception as error:
            logging.exception("Failed to refresh system metrics")
            self.status_label.setText("●  Ошибка обновления")
            self.status_label.setStyleSheet("color: #ff7b83;")
            self.statusBar().showMessage(f"Не удалось получить данные: {error}")
            return

        self.previous_network = network
        self.previous_network_time = network_time

        self.cpu_value.setText(f"{cpu['usage']:.0f}%")
        self.cpu_bar.setValue(round(cpu["usage"]))
        self.cpu_details.setText(
            f"Ядра: {cpu['cores']}   ·   Потоки: {cpu['threads']}"
        )

        self.ram_value.setText(f"{ram['percent']:.0f}%")
        self.ram_bar.setValue(round(ram["percent"]))
        self.ram_details.setText(
            f"Использовано: {bytes_to_gb(ram['used']):.1f} ГБ   ·   "
            f"Доступно: {bytes_to_gb(ram['available']):.1f} ГБ   ·   "
            f"Всего: {bytes_to_gb(ram['total']):.1f} ГБ"
        )

        self.download_value.setText(
            f"↓  {self._format_speed(network_speed['download_speed'])}"
        )
        self.upload_value.setText(
            f"↑  {self._format_speed(network_speed['upload_speed'])}"
        )
        self.network_totals.setText(
            f"Получено: {bytes_to_gb(network['received']):.2f} ГБ   ·   "
            f"Отправлено: {bytes_to_gb(network['sent']):.2f} ГБ"
        )

        if battery["percent"] is None:
            self.battery_value.setText("Нет батареи")
            self.battery_bar.setValue(0)
            self.battery_details.setText("Устройство работает от сети")
        else:
            self.battery_value.setText(f"{battery['percent']:.0f}%")
            self.battery_bar.setValue(round(battery["percent"]))
            if battery["plugged"] is None:
                power_state = "статус неизвестен"
            elif battery["plugged"]:
                power_state = "заряжается"
            else:
                power_state = "не подключена к сети"
            self.battery_details.setText(f"Состояние питания: {power_state}")

        self._update_disks(disks)
        self.updated_label.setText(
            f"Обновлено в {time.strftime('%H:%M:%S')}"
        )
        self.status_label.setText("●  Мониторинг активен")
        self.status_label.setStyleSheet("color: #5cdda5;")
        self.statusBar().clearMessage()


def main():
    app = QApplication([])
    window = MonitorWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
