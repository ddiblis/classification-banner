import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class AlwaysOnBanner(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Classification Banner")
        self.set_default_size(1920, 50)

        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)

        self.move(0, 0)

        label = Gtk.Label(label="TOP SECRET")
        label.set_justify(Gtk.Justification.CENTER)
        label.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 1.0, 1.0, 1.0))

        self.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 0.0, 0.0, 1.0))

        self.add(label)

    def run(self):
        self.show_all()
        Gtk.main()

if __name__ == "__main__":
    banner = AlwaysOnBanner()
    banner.run()