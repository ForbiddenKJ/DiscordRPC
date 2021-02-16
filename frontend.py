## Import

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GLib, GObject
from backend import discordrpc
import sys
import json

## Main Class

class Window(Gtk.Window):
    def __init__(self):
        ## Variables

        self.connectCalled = False

        ## Window Level Code

        Gtk.Window.__init__(self, title = 'Discord RPC')

        # Quit Window and Program
        def stop(x, y):
            Gtk.main_quit(x, y)
            sys.exit()

        # Connect
        self.connect('delete-event', stop)

        ## Non-Boxbound Widgets

        # Main Grid
        self.grid = Gtk.Grid()
        self.add(self.grid)

        # Branding Label
        self.branding = Gtk.Label()
        self.branding.set_label('Discord RPC')

        # Preset Label
        self.preset_label = Gtk.Label()
        self.preset_label.set_label('Presets')

        ## Define All Widgets

        # Client ID
        self.client_id_box = Gtk.Box(spacing = 1)

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

        # Save Button
        self.save_button = Gtk.Button(label = 'Save')
        self.save_button.connect('clicked', self.save_func)

        # Load Button
        self.load_button = Gtk.Button(label = 'Load')
        self.load_button.connect('clicked', self.load_func)

        # Stop Button
        self.stop_button = Gtk.Button(label = 'Stop')
        self.stop_button.connect('clicked', self.stop_func)

        # Button Box
        self.button_box = Gtk.Box(spacing = 5)
        self.button_box.pack_start(self.set_status, True, True, 0)
        self.button_box.pack_start(self.save_button, True, True, 0)
        self.button_box.pack_start(self.load_button, True, True, 0)
        self.button_box.pack_start(self.stop_button, True, True, 0)

        ## Preset

        # CPU & RAM Presets
        self.usage_button = Gtk.Button(label = 'Usage')
        self.usage_button.connect('clicked', self.usage_func)

        # Preset Box
        self.preset_box = Gtk.Box(spacing = 5)
        self.preset_box.pack_start(self.usage_button, True, True, 0)

        ## Widget Adds

        self.grid.attach(self.branding, 0, 0, 2, 1)
        self.grid.attach(self.client_id_box, 0, 1, 2, 1)
        self.grid.attach(self.state_box, 0, 2, 2, 1)
        self.grid.attach(self.details_box, 0, 3, 2, 1)
        self.grid.attach(self.large_image_box, 0, 4, 1, 1)
        self.grid.attach(self.small_image_box, 0, 5, 1, 1)
        self.grid.attach(self.button_box, 0, 6, 3, 2)
        self.grid.attach(self.preset_label, 2, 0, 2, 1)
        self.grid.attach(self.preset_box, 2, 1, 2, 1)

        self.handler = discordrpc()

    def get_info(self):
        getText = lambda x: x.get_properties('text')[0]

        # Get Input Results

        self.C_ID = getText(self.client_id_entry)
        self.state = getText(self.state_entry)
        self.details = getText(self.details_entry)
        self.large_image = getText(self.large_image_entry)
        self.small_image = getText(self.small_image_entry)

        return self.C_ID, self.state, self.details, self.large_image, self.small_image

    def set_status_func(self, widget):

        # Get Info

        self.get_info()

        if self.connectCalled == False or self.C_ID != self.connectCalled:
            self.handler.connect(self.C_ID)
            self.connectCalled = self.C_ID

        # Set Discord Status and Thread
        self.handler.backProcess(self.C_ID, self.state, self.details, self.large_image, self.small_image)

        return

    def save_func(self, widget):

        # Get Info

        self.get_info()

        with open('./data.json', 'w') as file:
            file.write(json.dumps({"C_ID": self.C_ID, "state": self.state, "details": self.details, "large_image": self.large_image, "small_image": self.small_image}))

    def load_func(self, widget):
        with open('./data.json', 'r') as file:
            self.data = json.loads(file.read())

        self.client_id_entry.set_text(self.data['C_ID'])
        self.state_entry.set_text(self.data['state'])
        self.details_entry.set_text(self.data['details'])
        self.large_image_entry.set_text(self.data['large_image'])
        self.small_image_entry.set_text(self.data['small_image'])

    def stop_func(self, widget):
        self.handler.stopConnection()

    def usage_func(self, widget):

        # Get Info

        self.get_info()

        ## Define Usage Preset Variables

        if self.C_ID == '':
            self.C_ID = '808689187799826494'

        if self.state == '':
            self.state = 'CPU: [CPU]% RAM: [RAM]%'

        if self.details == '':
            self.details = 'RAM & CPU Usage'

        if self.large_image is not None:
            self.large_image = 'large'

        if self.connectCalled == False or self.C_ID != self.connectCalled:
            self.handler.connect(self.C_ID)
            self.connectCalled = self.C_ID

        self.handler.customRPC('self.realTimeCPUUpdateLoop', self.C_ID, self.state, self.details, self.large_image, self.small_image)

        return

## Run Function

def run():
    window = Window()
    window.show_all()
    Gtk.main()
