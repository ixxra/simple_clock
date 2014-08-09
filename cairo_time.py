import time
import math as m
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk
from gi.repository import Pango


PI2 = m.pi / 2
CIRC = 2 * m.pi

RED = Gdk.RGBA(red=1.0, blue=0.0, green=0.0, alpha=0.5)
GREEN = Gdk.RGBA(red=0.0, blue=0.0, green=1.0, alpha=0.5)
BLUE = Gdk.RGBA(red=0.0, blue=1.0, green=0.0, alpha=0.5)


def update(data):
    data['l'].set_text(time.asctime())
    data['da'].queue_draw()
    return True


def draw(widget, cr):
    def pie_slice(xc, yc, radius, angle):
        cr.move_to(xc, yc)
        cr.rel_line_to(0, -radius)
        cr.arc(xc, yc, radius, 
                -PI2 + 0.01, angle -  PI2
        )
        cr.line_to(xc, yc)

    def brush(cr, color):
        Gdk.cairo_set_source_rgba(cr, color)
        cr.fill()

    localtime = time.localtime()

    hour = localtime.tm_hour % 12
    minutes = localtime.tm_min
    secs = localtime.tm_sec

    width = widget.get_allocated_width()
    height = widget.get_allocated_height()

    xc, yc, max_radius = width/2.0, height/2.0, min(width, height)/2.0

    pie_slice(xc, yc, 
            max_radius, 
            CIRC * secs / 60.0
    )

    brush(cr, BLUE)

    pie_slice(xc, yc, 
            max_radius * 2. / 3., 
            CIRC * minutes / 60.0
    )

    brush(cr, GREEN)

    pie_slice(xc, yc, 
            max_radius / 3., 
            CIRC * hour / 12.0
    )

    brush(cr, RED)

    return False


def make_window(update_func=update, draw_func=draw):
    w = Gtk.Window()
    w.connect('delete-event', lambda w, e: Gtk.main_quit())

    w.set_title(time.strftime('%a %d %B %Y', time.localtime()))
    w.resize(250, 100)

    da = Gtk.DrawingArea()
    da.connect('draw', draw_func)
    da.set_size_request(50, 50)

    l = Gtk.Label()

    frame = Gtk.Frame()
    frame.add(da)

    vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    vbox.pack_start(frame, True, True, 5)
    vbox.pack_start(l, False, True, 5)

    w.add(vbox)

    GLib.timeout_add_seconds(0.5, update_func, {'l':l, 'da': da})

    return w


if __name__ == '__main__':
    make_window().show_all()
    Gtk.main()  
