from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QProgressBar,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from pc_monitor.models import DiskMetrics


def bytes_to_gb(value: int) -> float:
    return value / (1024**3)


def format_speed(bytes_per_second: float) -> str:
    if bytes_per_second >= 1024**2:
        return f"{bytes_per_second / (1024**2):.2f} MB/s"
    if bytes_per_second >= 1024:
        return f"{bytes_per_second / 1024:.1f} KB/s"
    return f"{bytes_per_second:.0f} B/s"


def _new_card(title: str, card: QFrame) -> QVBoxLayout:
    card.setObjectName("card")
    card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    layout = QVBoxLayout(card)
    layout.setContentsMargins(20, 18, 20, 18)
    layout.setSpacing(12)
    heading = QLabel(title)
    heading.setObjectName("cardTitle")
    layout.addWidget(heading)
    return layout


class GaugeCard(QFrame):
    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = _new_card(title, self)

        self.value_label = QLabel("—")
        self.value_label.setObjectName("value")
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.details = QLabel("—")
        self.details.setObjectName("detail")
        layout.addWidget(self.value_label)
        layout.addWidget(self.progress)
        layout.addWidget(self.details)

    def set_metrics(
        self, value: str, percent: float, details: str
    ) -> None:
        self.value_label.setText(value)
        self.progress.setValue(round(percent))
        self.details.setText(details)


class NetworkCard(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = _new_card("Сеть", self)

        self.download_label = QLabel("↓  —")
        self.download_label.setObjectName("networkValue")
        self.upload_label = QLabel("↑  —")
        self.upload_label.setObjectName("networkValue")
        self.totals_label = QLabel("Получено: —   Отправлено: —")
        self.totals_label.setObjectName("detail")
        layout.addWidget(self.download_label)
        layout.addWidget(self.upload_label)
        layout.addWidget(self.totals_label)

    def set_metrics(
        self,
        download_speed: float,
        upload_speed: float,
        received: int,
        sent: int,
    ) -> None:
        self.download_label.setText(f"↓  {format_speed(download_speed)}")
        self.upload_label.setText(f"↑  {format_speed(upload_speed)}")
        self.totals_label.setText(
            f"Получено: {bytes_to_gb(received):.2f} ГБ   ·   "
            f"Отправлено: {bytes_to_gb(sent):.2f} ГБ"
        )


class DiskCard(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = _new_card("Накопители", self)

        self.rows_layout = QVBoxLayout()
        self.rows_layout.setSpacing(14)
        layout.addLayout(self.rows_layout)

    def set_disks(self, disks: list[DiskMetrics]) -> None:
        self._clear_rows()
        if not disks:
            empty = QLabel("Подключённые накопители не найдены")
            empty.setObjectName("detail")
            self.rows_layout.addWidget(empty)
            return

        for index, disk in enumerate(disks, start=1):
            row_widget = QWidget()
            row = QVBoxLayout(row_widget)
            row.setSpacing(7)
            heading = QLabel(f"Диск {index} · {disk.mountpoint}")
            heading.setObjectName("cardTitle")
            usage = QProgressBar()
            usage.setRange(0, 100)
            usage.setValue(round(disk.percent))
            usage.setTextVisible(False)
            details = QLabel(
                f"{disk.device}   ·   {bytes_to_gb(disk.used):.1f} / "
                f"{bytes_to_gb(disk.total):.1f} ГБ   ·   "
                f"свободно {bytes_to_gb(disk.free):.1f} ГБ"
            )
            details.setObjectName("detail")
            row.addWidget(heading)
            row.addWidget(usage)
            row.addWidget(details)
            self.rows_layout.addWidget(row_widget)

    def _clear_rows(self) -> None:
        while self.rows_layout.count():
            item = self.rows_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()
