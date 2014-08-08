import time
from gi.repository import Gtk
from gi.repository import GLib


def update(l):
    l.set_text(time.asctime())
    return True


w = Gtk.Window()
w.connect('delete-event', lambda w, e: Gtk.main_quit())

w.set_title(time.strftime('%a %d %B %Y', time.localtime()))
w.resize(250, 100)

l = Gtk.Label()
w.add(l)

GLib.timeout_add_seconds(0.5, update, l)

w.show_all()
Gtk.main()
