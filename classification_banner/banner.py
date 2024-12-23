import gi
import os
import cairo
import argparse
import configparser

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


CONF_FILE = "/etc/classification-banner/banner.conf"

# Check for DISPLAY environment variable
if "DISPLAY" not in os.environ:
    print("Error: DISPLAY environment variable is not set.")
    exit(1)

# Preset configurations
PRESETS = {
    "u": {"message": "UNCLASSIFIED", "fgcolor": "#FFFFFF", "bgcolor": "#007A33"},
    "confidential": {
        "message": "CONFIDENTIAL",
        "fgcolor": "#FFFFFF",
        "bgcolor": "#0033A0",
    },
    "secret": {"message": "SECRET", "fgcolor": "#FFFFFF", "bgcolor": "#C8102E"},
    "ts": {"message": "TOP SECRET", "fgcolor": "#FFFFFF", "bgcolor": "#FF671F"},
    "ts-sci": {
        "message": "TOP SECRET//SCI",
        "fgcolor": "#000000",
        "bgcolor": "#F7EA48",
    },
}


def configure():
    """Read global configuration and parse command-line arguments."""
    # Read configuration file
    conf = configparser.ConfigParser()
    conf.read(CONF_FILE)

    # Set default values from the configuration or fallbacks
    defaults = {
        "message": conf.get("global", "message", fallback="UNCLASSIFIED"),
        "fgcolor": conf.get("global", "fgcolor", fallback="#FFFFFF"),
        "bgcolor": conf.get("global", "bgcolor", fallback="#007A33"),
        "style": conf.get("global", "style", fallback="Modern"),
    }

    # Argument parsing
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

    # Flags for preset configurations
    parser.add_argument(
        "-u", "--unclassified", action="store_true", help="Set to UNCLASSIFIED"
    )
    parser.add_argument(
        "-ts", "--top-secret", action="store_true", help="Set to TOP SECRET"
    )
    parser.add_argument(
        "-c", "--confidential", action="store_true", help="Set to CONFIDENTIAL"
    )
    parser.add_argument("-s", "--secret", action="store_true", help="Set to SECRET")
    parser.add_argument(
        "-tssci", "--ts-sci", action="store_true", help="Set to TOP SECRET//SCI"
    )

    args = parser.parse_args()

    # Apply the preset values based on the flags
    preset_flags = {
        "unclassified": "u",
        "top_secret": "ts",
        "confidential": "confidential",
        "secret": "secret",
        "ts_sci": "ts_sci",
    }

    # Check each flag and apply the corresponding preset
    for flag, key in preset_flags.items():
        if getattr(args, flag):  # Check for the presence of the flag in the args object
            args.message, args.fgcolor, args.bgcolor = PRESETS[key].values()
            break

    return args


class AlwaysOnBanner(Gtk.Window):
    def __init__(self, position, monitor, message, fgcolor, bgcolor, style):
        super().__init__()
        self.set_title("Classification Banner")
        self.display = Gdk.Display.get_default()
        self.geometry = monitor.get_geometry()
        self.screen_height, self.screen_width = (
            self.geometry.height,
            self.geometry.width,
        )

        font_size = 15 if style == "Modern" else 12
        self.css = self.create_css(fgcolor, bgcolor, font_size)

        adjusted_width = self.screen_width // 15
        self.setup_window(position, adjusted_width, style)

        label = Gtk.Label(label=message)
        label.set_justify(Gtk.Justification.CENTER)
        label.set_name("banner-label")

        self.apply_css()

        self.add(label)
        self.make_click_through()

    def create_css(self, fgcolor, bgcolor, font_size):
        return f"""
            #banner-window {{
                background-color: {bgcolor};
            }}
            #banner-label {{
                color: {fgcolor};
                font-weight: bold;
                font-size: {font_size}px;
            }}
        """.encode(
            "utf-8"
        )

    def setup_window(self, position, adjusted_width, style):
        if style == "Modern":
            self.set_default_size(adjusted_width, 15)
            self.move_banner(position, adjusted_width)
        else:
            self.set_default_size(self.screen_width, 10)
            if position == "top":
                self.move(self.geometry.x, self.geometry.y)

        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.set_border_width(0)
        self.set_name("banner-window")

    def move_banner(self, position, adjusted_width):
        if position == "top":
            self.move(self.geometry.x, self.geometry.y + 45)
        elif position == "bottom":
            self.move(
                self.geometry.x + self.screen_width - adjusted_width,
                self.geometry.y + self.screen_height - 45,
            )

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(self.css)

        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def make_click_through(self):
        """Set the input shape of the window to make it click-through."""
        window = self.get_window()
        if window:
            region = cairo.Region()
            window.input_shape_combine_region(region, 0, 0)

    def show_banner(self):
        self.show_all()
        self.make_click_through()


def main():
    options = configure()
    display = Gdk.Display.get_default()
    num_monitors = display.get_n_monitors()

    banners = []
    for i in range(num_monitors):
        monitor = display.get_monitor(i)
        top_banner = AlwaysOnBanner(
            "top",
            monitor,
            options.message,
            options.fgcolor,
            options.bgcolor,
            options.style,
        )
        top_banner.show_banner()
        banners.append(top_banner)

        if options.style == "Modern":
            bottom_banner = AlwaysOnBanner(
                "bottom",
                monitor,
                options.message,
                options.fgcolor,
                options.bgcolor,
                options.style,
            )
            bottom_banner.show_banner()
            banners.append(bottom_banner)
    Gtk.main()


if __name__ == "__main__":
    main()

# import gi
# gi.require_version("Gtk", "4.0")
# from gi.repository import Gtk, Gdk

# class AlwaysOnBanner(Gtk.Window):
#     def __init__(self, position):
#         super().__init__()
#         self.set_title("Classification Banner")

#         display = Gdk.Display.get_default()
#         monitor = display.get_primary_monitor()
#         geometry = monitor.get_geometry()
#         self.screen_width = geometry.width
#         self.screen_height = geometry.height

#         self.type = 0  # Adjust type logic as needed
#         if self.type == 0:
#             self.set_default_size(150, 15)
#         else:
#             self.set_default_size(self.screen_width, 10)

#         self.set_decorated(False)
#         self.set_modal(True)
#         self.set_resizable(False)

#         self.set_name("banner-window")

#         label = Gtk.Label(label="Top Secret")
#         label.set_halign(Gtk.Align.CENTER)
#         label.set_valign(Gtk.Align.CENTER)
#         label.set_name("banner-label")

#         css_provider = Gtk.CssProvider()
#         css_data = (
#             b"""
#             #banner-window {
#                 background-color: red;
#             }
#             #banner-label {
#                 color: white;
#                 font-weight: bold;
#                 font-size: 15px;
#             }
#             """ if self.type == 0 else
#             b"""
#             #banner-window {
#                 background-color: red;
#             }
#             #banner-label {
#                 color: white;
#                 font-weight: bold;
#                 font-size: 12px;
#             }
#             """
#         )
#         css_provider.load_from_data(css_data)

#         Gtk.StyleContext.add_provider_for_display(
#             display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
#         )

#         self.set_child(label)

#     def show_banner(self):
#         self.present()

# if __name__ == "__main__":
#     app = Gtk.Application(application_id="com.example.Banner")

#     def on_activate(app):
#         top_banner = AlwaysOnBanner("top")
#         top_banner.set_application(app)
#         top_banner.show_banner()

#         bottom_banner = AlwaysOnBanner("bottom")
#         bottom_banner.set_application(app)
#         if bottom_banner.type == 0:
#             bottom_banner.show_banner()

#     app.connect("activate", on_activate)
#     app.run()
