APP_STYLESHEET = """
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
