import gi
import os
import argparse
import configparser
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from distutils.util import strtobool

CONF_FILE = "/etc/classification-banner/banner.conf"

# Check if DISPLAY variable is set
try:
    os.environ["DISPLAY"]
except KeyError:
    print("Error: DISPLAY environment variable is not set.")
    sys.exit(1)

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
except ImportError as e:
    raise e

def configure():
    """Read Global configuration"""
    defaults = {}
    defaults["message"] = "UNCLASSIFIED"
    defaults["fgcolor"] = "#FFFFFF"
    defaults["bgcolor"] = "#007A33"
    defaults["style"] = "Modern"

    conf = configparser.ConfigParser()
    conf.read(CONF_FILE)
    for key, val in conf.items("global"):
        defaults[key] = val

    # Use the global config to set defaults for command line options
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--message", default=defaults["message"],  
                        help="Set the Classification message")
    parser.add_argument("-f", "--fgcolor", default=defaults["fgcolor"],
                        help="Set the Foreground (text) color")
    parser.add_argument("-b", "--bgcolor", default=defaults["bgcolor"],
                        help="Set the Background color")
    parser.add_argument("-s", "--style", default=defaults["style"],
                        help="Style of banner, set between Modern and Classic")

    args = parser.parse_args()

    return args

class AlwaysOnBanner(Gtk.Window):
    def __init__(self, position, monitor, message="UNCLASSIFIED", fgcolor="#FFFFFF",
                 bgcolor="#007A33", style="Modern"):
        super().__init__()
        self.set_title("Classification Banner")
        self.display = Gdk.Display.get_default()
        self.geometry = monitor.get_geometry()
        self.screen_height = self.geometry.height
        self.screen_width = self.geometry.width
        font_size = 15 if style == "Modern" else 12
        self.css = f"""
            #banner-window {{
                background-color: {bgcolor};
            }}
            #banner-label {{
                color: {fgcolor};
                font-weight: bold;
                font-size: {font_size}px;
            }}
            """.encode('utf-8')

        adjusted_width = self.screen_width/15

        if style == "Modern":
            self.set_default_size(adjusted_width, 15)
        else:
            self.set_default_size(self.screen_width, 10)

        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)


        if style == "Modern":
            if position == "top":
                self.move(self.geometry.x, self.geometry.y + 70)
            elif position == "bottom":
                self.move(
                    self.geometry.x + self.screen_width - adjusted_width,
                    self.geometry.y + self.screen_height - 70 
                )
        else:
            if position == "top":
                self.move(self.geometry.x, self.geometry.y)


        self.set_border_width(0)
        self.set_name("banner-window")

        label = Gtk.Label(label=message)
        label.set_justify(Gtk.Justification.CENTER)
        label.set_name("banner-label")

        css_provider = Gtk.CssProvider()
        
        css_provider.load_from_data(self.css)

        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.add(label)

        self.connect("realize", self.on_realize)

    def on_realize(self, widget):
        # Make the window click-through after it is realized
        self.get_window().set_override_redirect(True)
        self.set_accept_focus(False)
        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)

    def show_banner(self):
        self.show_all()



if __name__ == "__main__":
    options = configure()
    display = Gdk.Display.get_default()
    num_monitors = display.get_n_monitors()

    banners = []
    for i in range(num_monitors):
        monitor = display.get_monitor(i)
        top_banner = AlwaysOnBanner(
            "top",
            monitor,
            message=options.message,
            bgcolor=options.bgcolor,
            fgcolor=options.fgcolor,
            style=options.style)

        top_banner.show_banner()
        if options.style == "Modern":
            bottom_banner = AlwaysOnBanner(
                "bottom",
                monitor,
                message=options.message,
                bgcolor=options.bgcolor,
                fgcolor=options.fgcolor,
                style=options.style)
            bottom_banner.show_banner()
            banners.append(bottom_banner)


        banners.append(top_banner)

    Gtk.main()



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