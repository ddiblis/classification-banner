import sys
import os
import argparse
import configparser
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QColor, QFont, QPalette, QRegion
from PyQt5.QtCore import Qt

CONF_FILE = "/etc/classification-banner/banner.conf"

if "DISPLAY" not in os.environ:
    print("Error: DISPLAY environment variable is not set.")
    exit(1)

PRESETS = {
    "unclassified": {
        "message": "UNCLASSIFIED",
        "fgcolor": "#FFFFFF",
        "bgcolor": "#007a33",
    },
    "cui": {
        "message": "CUI",
        "fgcolor": "#FFFFFF",
        "bgcolor": "#502b85",
    },
    "confidential": {
        "message": "CONFIDENTIAL",
        "fgcolor": "#FFFFFF",
        "bgcolor": "#0033a0",
    },
    "secret": {"message": "SECRET", "fgcolor": "#FFFFFF", "bgcolor": "#c8102e"},
    "top_secret": {"message": "TOP SECRET", "fgcolor": "#FFFFFF", "bgcolor": "#ff8c00"},
    "ts_sci": {
        "message": "TOP SECRET//SCI",
        "fgcolor": "#000000",
        "bgcolor": "#fce83a",
    },
}

def configure():
    """Read global configuration and parse command-line arguments."""
    conf = configparser.ConfigParser()
    conf.read(CONF_FILE)

    defaults = {
        "message": conf.get("global", "message", fallback="UNCLASSIFIED"),
        "fgcolor": conf.get("global", "fgcolor", fallback="#FFFFFF"),
        "bgcolor": conf.get("global", "bgcolor", fallback="#007A33"),
        "style": conf.get("global", "style", fallback="Modern"),
    }

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-M",
        "--message",
        default=defaults["message"],
        help="Set the Classification message",
    )
    parser.add_argument(
        "-F",
        "--fgcolor",
        default=defaults["fgcolor"],
        help="Set the Foreground (text) color",
    )
    parser.add_argument(
        "-B", "--bgcolor", default=defaults["bgcolor"], help="Set the Background color"
    )
    parser.add_argument(
        "-S",
        "--style",
        default=defaults["style"],
        help="Style of banner, set between Modern and Classic",
    )

    parser.add_argument(
        "-u", "--unclassified", action="store_true", help="Set to UNCLASSIFIED"
    )
    parser.add_argument(
        "-cui",
        "--cui",
        action="store_true",
        help="Set to Controlled Unclassified Information",
    )
    parser.add_argument(
        "-c", "--confidential", action="store_true", help="Set to CONFIDENTIAL"
    )
    parser.add_argument("-s", "--secret", action="store_true", help="Set to SECRET")
    parser.add_argument(
        "-ts", "--top_secret", action="store_true", help="Set to TOP SECRET"
    )
    parser.add_argument(
        "-tssci", "--ts_sci", action="store_true", help="Set to TOP SECRET//SCI"
    )

    args = parser.parse_args()

    preset_flags = {
        "unclassified": "unclassified",
        "cui": "cui",
        "confidential": "confidential",
        "secret": "secret",
        "top_secret": "top_secret",
        "ts_sci": "ts_sci",
    }

    for flag, key in preset_flags.items():
        if getattr(args, flag):  
            args.message, args.fgcolor, args.bgcolor = PRESETS[key].values()
            break

    return args

class AlwaysOnBanner(QMainWindow):
    def __init__(self, position, screen, message, fgcolor, bgcolor, style):
        super().__init__()
        self.setWindowTitle("Classification Banner")
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.WindowTransparentForInput
        )

        self.fgcolor = QColor(fgcolor)
        self.bgcolor = QColor(bgcolor)

        self._setup_geometry(position, screen, style)
        self._setup_label(message, style)

    def _setup_geometry(self, position, screen, style):
        screen_geom = screen.geometry()
        banner_height = 20 if style == "Modern" else 15
        adjusted_width = screen_geom.width() // 15 if style == "Modern" else screen_geom.width()
        
        top_offset = 45 if style == "Modern" else 0
        bottom_offset = 45 if style == "Modern" else 0

        if position == "top":
            self.setGeometry(screen_geom.x(), screen_geom.y() + top_offset, adjusted_width, banner_height)
        elif position == "bottom":
            right_x = screen_geom.right() - adjusted_width
            self.setGeometry(right_x, screen_geom.bottom() - banner_height - bottom_offset, adjusted_width, banner_height)

    def _setup_label(self, message, style):
        label = QLabel(message, self)
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(self.rect())

        font_size = 10
        font = QFont("Arial", font_size, QFont.Bold)
        label.setFont(font)

        palette = label.palette()
        palette.setColor(QPalette.WindowText, self.fgcolor)
        palette.setColor(QPalette.Window, self.bgcolor)
        label.setAutoFillBackground(True)
        label.setPalette(palette)

        self.setCentralWidget(label)

    def show_banner(self):
        self.show()


def main():
    options = configure()
    app = QApplication(sys.argv)

    screens = app.screens()
    banners = []

    for screen in screens:
        top_banner = AlwaysOnBanner("top", screen, options.message, options.fgcolor, options.bgcolor, options.style)
        top_banner.show_banner()
        banners.append(top_banner)

        if options.style == "Modern":
            bottom_banner = AlwaysOnBanner("bottom", screen, options.message, options.fgcolor, options.bgcolor, options.style)
            bottom_banner.show_banner()
            banners.append(bottom_banner)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
