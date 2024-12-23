import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class AlwaysOnBanner(Gtk.Window):
    def __init__(self, position, monitor):
        super().__init__()
        self.set_title("Classification Banner")
        self.display = Gdk.Display.get_default()
        self.monitor = monitor
        self.geometry = self.monitor.get_geometry()
        self.screen_height = self.geometry.height
        self.screen_width = self.geometry.width
        self.type = 0
        if self.type == 0:
            self.set_default_size(150, 15)
        else:
            self.set_default_size(self.screen_width, 10)

        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)

        if self.type == 0:
            if position == "top":
                self.move(self.geometry.x, self.geometry.y + 25)
            elif position == "bottom":
                self.move(
                    self.geometry.x + self.screen_width - 150,  # Adjust `x` to the right
                    self.geometry.y + self.screen_height - 40   # Keep `y` at the bottom
                )
        else:
            if position == "top":
                self.move(self.geometry.x, self.geometry.y)


        self.set_border_width(0)
        self.set_name("banner-window")

        label = Gtk.Label(label="Top Secret")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_name("banner-label")

        css_provider = Gtk.CssProvider()
        if self.type == 0:
            css_provider.load_from_data(
                b"""
                #banner-window {
                    background-color: red;
                }
                #banner-label {
                    color: white;
                    font-weight: bold;
                    font-size: 15px;
                }
                """
            )
        else:
            css_provider.load_from_data(
                b"""
                #banner-window {
                    background-color: red;
                }
                #banner-label {
                    color: white;
                    font-weight: bold;
                    font-size: 12px;
                }
                """
            )
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.add(label)

    def show_banner(self):
        self.show_all()


if __name__ == "__main__":
    display = Gdk.Display.get_default()
    num_monitors = display.get_n_monitors()

    banners = []
    for i in range(num_monitors):
        monitor = display.get_monitor(i)
        top_banner = AlwaysOnBanner("top", monitor)
        bottom_banner = AlwaysOnBanner("bottom", monitor)

        top_banner.show_banner()
        if bottom_banner.type == 0:
            bottom_banner.show_banner()

        banners.append(top_banner)
        banners.append(bottom_banner)

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