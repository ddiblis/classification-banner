import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class AlwaysOnBanner(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Classification Banner")
        self.set_default_size(1920, 10)  # Rectangle: 1920px width, 40px height

        # Remove window decorations and make it always on top
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)

        # Set a fixed position at the top of the screen
        self.move(0, 0)

        # Remove any potential invisible border
        self.set_border_width(0)

        # Assign a CSS name to the window
        self.set_name("banner-window")

        # Create the banner label
        label = Gtk.Label(label="CLASSIFICATION: TOP SECRET")
        label.set_justify(Gtk.Justification.CENTER)
        label.set_name("banner-label")  # Name the label for CSS styling

        # Apply CSS styling
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(
            b"""
            #banner-window {
                background-color: red;
            }
            #banner-label {
                color: white;
                font-weight: bold;
                font-size: 10px;
            }
            """
        )
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Add the label to the window
        self.add(label)

    def run(self):
        self.show_all()
        Gtk.main()

if __name__ == "__main__":
    banner = AlwaysOnBanner()
    banner.run()
