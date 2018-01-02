# -*- coding: utf-8 -*-
# Copyright 2018 Phidica Veia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import sqlite3

from gi.repository import Gtk
from senf import uri2fsn

from quodlibet import _
from quodlibet import app
from quodlibet import util
from quodlibet.qltk import Icons
from quodlibet.qltk.msg import WarningMessage, ErrorMessage
from quodlibet.util.path import expanduser, normalize_path
from quodlibet.plugins.events import EventPlugin


class BansheeDBImporter:

    def __init__(self, library):

        self._library = library
        self._changed_songs = []

    def read(self, db):
        """Iterate through the library and search for data to import for
        each song
        """

        for song in self._library:
            print("filename: %s" % song["~filename"])

    def finish(self):
        """Call at the end, also returns number of songs with data imported"""

        count = len(self._changed_songs)
        self._library.changed(self._changed_songs)
        self._changed_songs = []
        return count


def do_import(parent, library):
    db_path = expanduser("~/.config/banshee-1/banshee.db")
    msg = _("test db path %s") % db_path
    # FIXME: this is just a warning so it works with older QL
    WarningMessage(parent, BansheeImport.PLUGIN_NAME, msg).run()


class BansheeImport(EventPlugin):
    PLUGIN_ID = "bansheeimport"
    PLUGIN_NAME = _("Banshee Import")
    PLUGIN_DESC = _("Imports ratings and song statistics from Banshee.")
    PLUGIN_ICON = Icons.DOCUMENT_OPEN

    def PluginPreferences(self, *args):
        button = Gtk.Button(label=_("Start Import"))

        def clicked_cb(button):
            do_import(button, app.library)

        button.connect("clicked", clicked_cb)
        return button
