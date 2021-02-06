import gi.repository

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from backend import discordrpc
import sys

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = 'Discord RPC')

        # Main Grid
        self.grid = Gtk.Grid()
        self.add(self.grid)

        # Branding Label
        self.branding = Gtk.Label()
        self.branding.set_label('Discord RPC')

        # Client ID
        self.client_id_box = Gtk.Box(spacing = 10)

        self.client_id_label = Gtk.Label()
        self.client_id_label.set_label('Client ID:')

        self.client_id_entry = Gtk.Entry()

        self.client_id_box.pack_start(self.client_id_label, True, True, 0)
        self.client_id_box.pack_start(self.client_id_entry, True, True, 0)

        # State
        self.state_box = Gtk.Box()

        self.state_label = Gtk.Label()
        self.state_label.set_label('State:')

        self.state_entry = Gtk.Entry()

        self.state_box.pack_start(self.state_label, True, True, 0)
        self.state_box.pack_start(self.state_entry, True, True, 0)

        # Details
        self.details_box = Gtk.Box()

        self.details_label = Gtk.Label()
        self.details_label.set_label('Details:')

        self.details_entry = Gtk.Entry()

        self.details_box.pack_start(self.details_label, True, True, 0)
        self.details_box.pack_start(self.details_entry, True, True, 0)

        # Large Image
        self.large_image_box = Gtk.Box()

        self.large_image_label = Gtk.Label()
        self.large_image_label.set_label('* Large Image:')

        self.large_image_entry = Gtk.Entry()

        self.large_image_box.pack_start(self.large_image_label, True, True, 0)
        self.large_image_box.pack_start(self.large_image_entry, True, True, 0)

        # Small Image
        self.small_image_box = Gtk.Box()

        self.small_image_label = Gtk.Label()
        self.small_image_label.set_label('* Small Image:')

        self.small_image_entry = Gtk.Entry()

        self.small_image_box.pack_start(self.small_image_label, True, True, 0)
        self.small_image_box.pack_start(self.small_image_entry, True, True, 0)

        # Update Status Button
        self.set_status = Gtk.Button(label = 'Set Status')
        self.set_status.connect('clicked', self.set_status_func)

        # Widget Adds
        self.grid.attach(self.branding, 0, 0, 2, 1)
        self.grid.attach(self.client_id_box, 0, 1, 2, 1)
        self.grid.attach(self.state_box, 0, 2, 2, 1)
        self.grid.attach(self.details_box, 0, 3, 2, 1)
        self.grid.attach(self.large_image_box, 0, 4, 2, 1)
        self.grid.attach(self.small_image_box, 0, 5, 2, 1)
        self.grid.attach(self.set_status, 0, 6, 2, 1)

        self.handler = None

    def set_status_func(self, widget):
        getText = lambda x: x.get_properties('text')[0]

        C_ID = getText(self.client_id_entry)
        state = getText(self.state_entry)
        details = getText(self.details_entry)
        large_image = getText(self.large_image_entry)
        small_image = getText(self.small_image_entry)

        print(C_ID, state, details)

        self.handler = discordrpc(C_ID, state, details)
        self.handler.connect()
        self.handler.updateStatus()
        self.handler.stayConnected()

def stop(x, y):
    Gtk.main_quit(x, y)
    sys.exit()

def run():
    window = Window()
    window.connect('delete-event', stop)
    window.show_all()
    Gtk.main()
