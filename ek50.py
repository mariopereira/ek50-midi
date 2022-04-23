#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import ek50config
import ek50data
import ek50midi

class Application(Gtk.Window):
    def __init__(self):
        """Application initialization"""
        Gtk.Window.__init__(self, title = 'Korg EK-50 Midi Program Changer', border_width = 5)
        Gtk.Window.set_default_size(self, 1000, 500)
        Gtk.Window.maximize(self)

        self.midi = ek50midi.Ek50Midi()

        self.init_config()
        self.create_controls()
        self.layout_app()

        msb, lsb, pc = self.configuration.get_default_sound()

        if self.sound_select_by_patch(msb, lsb, pc):
            self.on_activate_sound(self.buttonSoundActivate)


    def init_config(self):
        """Application configuration initialization"""
        self.currentCategory = None
        self.configuration = ek50config.Ek50Config(self)
        self.configuration.save()


    def create_controls(self):
        """Create all needed controls"""
        self.buttonQuit = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('application-exit', Gtk.IconSize.DIALOG))
        self.buttonQuit.set_vexpand(True)
        self.buttonQuit.set_hexpand(True)
        self.buttonQuit.set_tooltip_text('Exit')
        self.buttonQuit.connect('clicked', Gtk.main_quit)

        self.buttonPanic = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('media-eject', Gtk.IconSize.DIALOG))
        self.buttonPanic.set_vexpand(True)
        self.buttonPanic.set_hexpand(True)
        self.buttonPanic.set_tooltip_text('Panic!')

        self.headerBar = Gtk.HeaderBar()
        self.headerBar.set_show_close_button(True)
        self.headerBar.set_title('-- No sound --')
        self.headerBar.set_subtitle('Korg EK-50 Midi Program Changer')
        self.set_titlebar(self.headerBar)

        self.buttonCatUp = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('go-up', Gtk.IconSize.DIALOG))
        self.buttonCatUp.set_vexpand(True)
        self.buttonCatUp.set_hexpand(True)
        self.buttonCatUp.set_tooltip_text('Previous Category')
        self.buttonCatUp.connect('clicked', self.on_category_up)

        self.buttonCatDown = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('go-down', Gtk.IconSize.DIALOG))
        self.buttonCatDown.set_vexpand(True)
        self.buttonCatDown.set_hexpand(True)
        self.buttonCatDown.set_tooltip_text('Next Category')
        self.buttonCatDown.connect('clicked', self.on_category_down)

        self.buttonPcUp = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('go-up', Gtk.IconSize.DIALOG))
        self.buttonPcUp.set_vexpand(True)
        self.buttonPcUp.set_hexpand(True)
        self.buttonPcUp.set_tooltip_text('Program up')
        self.buttonPcUp.connect('clicked', self.on_pc_up)

        self.buttonPcDown = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('go-down', Gtk.IconSize.DIALOG))
        self.buttonPcDown.set_vexpand(True)
        self.buttonPcDown.set_hexpand(True)
        self.buttonPcDown.set_tooltip_text('Program down')
        self.buttonPcDown.connect('clicked', self.on_pc_down)

        self.buttonSoundUp = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('go-up', Gtk.IconSize.DIALOG))
        self.buttonSoundUp.set_vexpand(True)
        self.buttonSoundUp.set_hexpand(True)
        self.buttonSoundUp.set_tooltip_text('Previous Sound')
        self.buttonSoundUp.connect('clicked', self.on_prev_sound)

        self.buttonSoundDown = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('go-down', Gtk.IconSize.DIALOG))
        self.buttonSoundDown.set_vexpand(True)
        self.buttonSoundDown.set_hexpand(True)
        self.buttonSoundDown.set_tooltip_text('Next Sound')
        self.buttonSoundDown.connect('clicked', self.on_next_sound)

        self.buttonSoundPageUp = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('go-previous', Gtk.IconSize.DIALOG))
        self.buttonSoundPageUp.set_vexpand(True)
        self.buttonSoundPageUp.set_hexpand(True)
        self.buttonSoundPageUp.set_tooltip_text('Back 10 Sounds')
        self.buttonSoundPageUp.connect('clicked', self.on_pageup_sound)

        self.buttonSoundPageDown = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('go-next', Gtk.IconSize.DIALOG))
        self.buttonSoundPageDown.set_vexpand(True)
        self.buttonSoundPageDown.set_hexpand(True)
        self.buttonSoundPageDown.set_tooltip_text('Forward 10 Sounds')
        self.buttonSoundPageDown.connect('clicked', self.on_pagedown_sound)

        self.buttonSoundFirst = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('go-top', Gtk.IconSize.DIALOG))
        self.buttonSoundFirst.set_vexpand(True)
        self.buttonSoundFirst.set_hexpand(True)
        self.buttonSoundFirst.set_tooltip_text('First Sound')
        self.buttonSoundFirst.connect('clicked', self.on_first_sound)

        self.buttonSoundLast = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('go-bottom', Gtk.IconSize.DIALOG))
        self.buttonSoundLast.set_vexpand(True)
        self.buttonSoundLast.set_hexpand(True)
        self.buttonSoundLast.set_tooltip_text('Last Sound')
        self.buttonSoundLast.connect('clicked', self.on_last_sound)

        self.buttonClearCats = Gtk.ToolButton.new(label = 'Clear')
        self.buttonClearCats.set_vexpand(True)
        self.buttonClearCats.set_hexpand(True)
        self.buttonClearCats.connect('clicked', self.on_clear_category)

        self.buttonSoundActivate = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('media-playback-start', Gtk.IconSize.DIALOG))
        self.buttonSoundActivate.set_vexpand(True)
        self.buttonSoundActivate.set_hexpand(True)
        self.buttonSoundActivate.set_tooltip_text('Activate Sound')
        self.buttonSoundActivate.connect('clicked', self.on_activate_sound)

        self.buttonFavs = []

        for n in range(self.configuration.get_fav_count()):
            self.buttonFavs.append(Gtk.ToolButton.new(label = 'Fav #' + str(n)))
            self.buttonFavs[n].set_vexpand(True)
            self.buttonFavs[n].set_hexpand(True)
            self.buttonFavs[n].connect('clicked', self.on_favourite, n)

        self.buttonsFavSet = []

        for n in range(self.configuration.get_fav_count()):
            label = 'Set fav #' + str(n)

            if self.configuration.has_favourite(n):
                label = label + ' (*)'

            self.buttonsFavSet.append(Gtk.ToolButton.new(label = label))
            self.buttonsFavSet[n].set_vexpand(True)
            self.buttonsFavSet[n].set_hexpand(True)
            self.buttonsFavSet[n].connect('clicked', self.on_favourite_set, n)

        self.soundFilter = ek50data.sounds.filter_new()
        self.soundFilter.set_visible_func(self.sounds_filter_func)

        self.soundView = Gtk.TreeView.new_with_model(self.soundFilter)

        for n, column_title in enumerate(['Category', 'Sound']):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text = n + 3)
            self.soundView.append_column(column)

        select = self.soundView.get_selection()
        select.connect('changed', self.on_sound_selection_changed)

        self.soundViewScrollable = Gtk.ScrolledWindow()
        self.soundViewScrollable.set_vexpand(True)

        self.comboCategories = Gtk.ComboBox.new_with_model(ek50data.categories)
        self.comboCategories.set_vexpand(True)
        self.comboCategories.set_hexpand(True)
        renderer = Gtk.CellRendererText()
        self.comboCategories.pack_start(renderer, True)
        self.comboCategories.add_attribute(renderer, 'text', 0)
        self.comboCategories.connect('changed', self.on_category_changed)
        self.comboCategories.set_active(0)

        self.inputList = Gtk.ListStore(str)

        for device in self.midi.input_list():
            self.inputList.append([device])

        self.outputList = Gtk.ListStore(str)

        for device in self.midi.output_list():
            self.outputList.append([device])

        self.comboInputDevice = Gtk.ComboBox.new_with_model(self.inputList)
        renderer = Gtk.CellRendererText()
        self.comboInputDevice.pack_start(renderer, True)
        self.comboInputDevice.add_attribute(renderer, 'text', 0)
        self.comboInputDevice.connect('changed', self.on_input_device_changed)

        self.comboOutputDevice = Gtk.ComboBox.new_with_model(self.outputList)
        renderer = Gtk.CellRendererText()
        self.comboOutputDevice.pack_start(renderer, True)
        self.comboOutputDevice.add_attribute(renderer, 'text', 0)
        self.comboOutputDevice.connect('changed', self.on_output_device_changed)

        channels = Gtk.ListStore(int)
        for ch in range(1, 17):
            channels.append([ch])

        self.comboInputChannel = Gtk.ComboBox.new_with_model(channels)
        renderer = Gtk.CellRendererText()
        self.comboInputChannel.pack_start(renderer, True)
        self.comboInputChannel.add_attribute(renderer, 'text', 0)
        self.comboInputChannel.connect('changed', self.on_input_channel_changed)

        channels = Gtk.ListStore(int)
        for ch in range(1, 17):
            channels.append([ch])

        self.comboOutputChannel = Gtk.ComboBox.new_with_model(channels)
        renderer = Gtk.CellRendererText()
        self.comboOutputChannel.pack_start(renderer, True)
        self.comboOutputChannel.add_attribute(renderer, 'text', 0)
        self.comboOutputChannel.connect('changed', self.on_output_channel_changed)

        self.buttonRefreshDevices = Gtk.ToolButton.new(label = 'Refresh Devices')
        self.buttonRefreshDevices.connect('clicked', self.on_refresh_devices)


    def layout_app(self):
        """Create the application layout"""
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        page1 = self.layout_page1()
        page2 = self.layout_page2()
        page3 = self.layout_page3()
        pageConfig = self.layout_page_config()

        self.notebook.append_page(page1, Gtk.Label(label = 'Sounds'))
        self.notebook.append_page(page2, Gtk.Label(label = 'Favourites'))
        self.notebook.append_page(page3, Gtk.Label(label = 'Set Favourite'))
        self.notebook.append_page(pageConfig, Gtk.Label(label = 'Configuration'))

        self.show_all()


    def layout_page1(self):
        """Create the main page"""
        grid = Gtk.Grid()
        grid.column_homogenous = True
        grid.row_homogenous = True
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)

        grid.attach(self.buttonCatUp, 0, 0, 2, 2)
        grid.attach(self.buttonCatDown, 2, 0, 2, 2)

        grid.attach(self.comboCategories, 4, 0, 1, 1)
        grid.attach(self.buttonClearCats, 4, 1, 1, 1)

        grid.attach(self.buttonPcUp, 6, 0, 2, 2)
        grid.attach(self.buttonPcDown, 8, 0, 2, 2)

        grid.attach(self.soundViewScrollable, 0, 3, 4, 9)
        self.soundViewScrollable.add(self.soundView)

        grid.attach(self.buttonSoundFirst, 4, 3, 2, 3)
        grid.attach(self.buttonSoundLast, 4, 6, 2, 3)
        grid.attach(self.buttonSoundPageUp, 4, 9, 2, 3)

        grid.attach(self.buttonSoundUp, 6, 3, 2, 3)
        grid.attach(self.buttonSoundDown, 6, 6, 2, 3)
        grid.attach(self.buttonSoundPageDown, 6, 9, 2, 3)

        grid.attach(self.buttonSoundActivate, 8, 3, 2, 3)
        grid.attach(self.buttonPanic, 8, 6, 2, 3)
        grid.attach(self.buttonQuit, 8, 9, 2, 3)

        return grid


    def layout_page2(self):
        """Creats the favourites page"""
        grid = Gtk.Grid()
        grid.column_homogenous = True
        grid.row_homogenous = True
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)

        rows = self.configuration.get_fav_rows()
        cols = self.configuration.get_fav_cols()

        for row in range(rows):
            for col in range(cols):
                index = (row * cols) + col
                msb, lsb, _pc, name = self.configuration.get_favourite(index)

                if msb is not None and lsb is not None:
                    self.buttonFavs[index].set_label(name)

                grid.attach(self.buttonFavs[index], col, row, 1, 1)

        return grid


    def layout_page3(self):
        """Create the set favourites page"""
        grid = Gtk.Grid()
        grid.column_homogenous = True
        grid.row_homogenous = True
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)

        rows = self.configuration.get_fav_rows()
        cols = self.configuration.get_fav_cols()

        for row in range(rows):
            for col in range(cols):
                index = (row * cols) + col

                grid.attach(self.buttonsFavSet[index], col, row, 1, 1)

        return grid


    def layout_page_config(self):
        """Create the configuration page"""
        grid = Gtk.Grid()
        grid.set_row_spacing(15)
        grid.set_column_spacing(10)
        grid.set_border_width(10)

        grid.attach(Gtk.Label(label = 'Input Device'), 0, 0, 1, 1)
        grid.attach(self.comboInputDevice, 1, 0, 1, 1)
        grid.attach(self.comboInputChannel, 2, 0, 1, 1)

        grid.attach(Gtk.Label(label = 'Output Device'), 0, 1, 1, 1)
        grid.attach(self.comboOutputDevice, 1, 1, 1, 1)
        grid.attach(self.comboOutputChannel, 2, 1, 1, 1)

        grid.attach(self.buttonRefreshDevices, 1, 2, 1, 1)

        return grid


    def sounds_filter_func(self, model, iter, data):
        """Test if the category in the row is the selected category"""
        if (self.currentCategory is None or self.currentCategory == ''):
            return True

        return model[iter][3] == self.currentCategory


    def sound_get_selection(self):
        """Get currently selected sound"""
        selection = self.soundView.get_selection()
        model, treeIter = selection.get_selected()

        return model, treeIter


    def sound_get_selection_info(self):
        """Get the lsb, pc, sound and category of the currently selected sound"""
        msb = None
        lsb = None
        pc = None
        sound = None
        category = None

        model, treeIter = self.sound_get_selection()

        if treeIter is None:
            return msb, lsb, pc, sound, category

        msb = model[treeIter][0]
        lsb = model[treeIter][1]
        pc = model[treeIter][2]
        category = model[treeIter][3]
        sound = model[treeIter][4]

        return msb, lsb, pc, sound, category


    def sound_scroll_to_selection(self):
        """Scrolls the sound view to the selected item"""
        model, treeIter = self.sound_get_selection()

        if treeIter is None:
            return

        self.soundView.scroll_to_cell(model.get_path(treeIter))


    def sound_select_first(self):
        """Select the first available sound"""
        model, treeIter = self.sound_get_selection()
        treeIter = model.get_iter(0)

        if treeIter is not None:
            self.soundView.get_selection().select_iter(treeIter)


    def sound_select_by_patch(self, msb, lsb, pc):
        """Select a sound by its lsb and pc values"""
        # first, we must clear the category selection and refilter
        self.comboCategories.set_active_iter(None)
        self.soundFilter.refilter()

        # now, search all model for the entry we want
        model, treeIter = self.sound_get_selection()

        treeIter = model.get_iter(0)

        if msb is None or lsb is None or pc is None or treeIter is None:
            self.sound_select_first()
            return False

        wanted = hex(msb) + hex(lsb) + hex(pc)
        current = hex(model[treeIter][0]) + hex(model[treeIter][1]) + hex(model[treeIter][2])

        if wanted == current:
            self.soundView.get_selection().select_iter(treeIter)
            return True

        while wanted != current and treeIter is not None:
            treeIter = model.iter_next(treeIter)

            if treeIter is not None:
                current = hex(model[treeIter][0]) + hex(model[treeIter][1]) + hex(model[treeIter][2])

        result = True

        if treeIter is None:
            treeIter = model.get_iter(0)
            result = False

        self.soundView.get_selection().select_iter(treeIter)
        return result


    def on_sound_selection_changed(self, selection):
        """Called when the user selects another sound from the list"""
        _model, treeIter = selection.get_selected()

        if treeIter is None:
            return

        self.sound_scroll_to_selection()

    def on_category_changed(self, combo):
        """Change the current category displayed"""
        treeIter = combo.get_active_iter()

        if treeIter is None:
            self.currentCategory = None
            return

        model = combo.get_model()
        self.currentCategory = model[treeIter][0]

        self.soundFilter.refilter()
        self.sound_select_first()


    def on_clear_category(self, button):
        """Clear the selected category"""
        self.comboCategories.set_active_id(None)
        self.soundFilter.refilter()


    def on_category_up(self, button):
        """Change to the previous category"""
        curSel = self.comboCategories.get_active()

        curSel = curSel - 1

        if curSel < 0:
            curSel = 0

        self.comboCategories.set_active(curSel)
        self.soundFilter.refilter()


    def on_category_down(self, button):
        """Change to the next category"""
        model = self.comboCategories.get_model()
        numCats = len(model)
        curSel = self.comboCategories.get_active()

        curSel = curSel + 1

        if curSel < numCats:
            self.comboCategories.set_active(curSel)
            self.soundFilter.refilter()


    def on_pc_up(self, button):
        """Handles clicks on 'Pc Up' button"""
        selection = self.soundView.get_selection()
        model, treeIter = selection.get_selected()

        if treeIter is None:
            return

        curPc = model[treeIter][1]
        newPc = curPc

        while newPc == curPc and treeIter is not None:
            treeIter = model.iter_previous(treeIter)

            if treeIter is not None:
                newPc = model[treeIter][1]

        if treeIter is None:
            return

        curPc = newPc
        newIter = treeIter

        while newPc == curPc and newIter is not None:
            newIter = model.iter_previous(newIter)

            if newIter is None:
                selection.select_iter(treeIter)
                return

            newPc = model[newIter][1]

            if curPc == newPc:
                treeIter = newIter

        selection.select_iter(treeIter)


    def on_pc_down(self, button):
        """Handles clicks on 'Pc Down' button"""
        selection = self.soundView.get_selection()
        model, treeIter = selection.get_selected()

        if treeIter is None:
            return

        curPc = model[treeIter][1]
        newPc = curPc

        while newPc == curPc and treeIter is not None:
            treeIter = model.iter_next(treeIter)

            if treeIter is not None:
                newPc = model[treeIter][1]

        if treeIter is not None:
            selection.select_iter(treeIter)


    def on_prev_sound(self, button):
        """Handles click on 'Previous Sound" button"""
        selection = self.soundView.get_selection()
        model, treeIter = selection.get_selected()

        if treeIter is None:
            treeIter = model.get_iter(0)
        else:
            treeIter = model.iter_previous(treeIter)

        if treeIter is not None:
            selection.select_iter(treeIter)


    def on_next_sound(self, button):
        """Handles click on 'Next Sound' button"""
        selection = self.soundView.get_selection()
        model, treeIter = selection.get_selected()

        if treeIter is None:
            treeIter = model.get_iter(0)
        else:
            treeIter = model.iter_next(treeIter)

        if treeIter is not None:
            selection.select_iter(treeIter)


    def on_pageup_sound(self, button):
        """ Moves 10 sounds up"""
        selection = self.soundView.get_selection()
        model, treeIter = selection.get_selected()

        if treeIter is None:
            treeIter = model.get_iter(0)
        else:
            n = 0
            while n < 10:
                nextIter = model.iter_previous(treeIter)

                if nextIter is None:
                    break

                treeIter = nextIter
                n = n + 1

        selection.select_iter(treeIter)


    def on_pagedown_sound(self, button):
        """ Moves 10 sounds down"""
        selection = self.soundView.get_selection()
        model, treeIter = selection.get_selected()

        if treeIter is None:
            treeIter = model.get_iter(0)
        else:
            n = 0
            while n < 10:
                nextIter = model.iter_next(treeIter)

                if nextIter is None:
                    break

                treeIter = nextIter
                n = n + 1

        selection.select_iter(treeIter)


    def on_first_sound(self, button):
        """Move to the first sound"""
        self.sound_select_first()


    def on_last_sound(self, button):
        """Move to the last sound"""
        selection = self.soundView.get_selection()
        model, treeIter = selection.get_selected()

        if treeIter is None:
            treeIter = model.get_iter(0)

        nextIter = treeIter

        while nextIter is not None:
            nextIter = model.iter_next(treeIter)

            if nextIter is not None:
                treeIter = nextIter

        selection.select_iter(treeIter)


    def on_activate_sound(self, button):
        """Send the midi program change to activate current sound"""
        msb, lsb, pc, sound, category = self.sound_get_selection_info()

        if msb is None or lsb is None or pc is None:
            return

        self.configuration.set_default_sound(msb, lsb, pc)

        title = sound

        if category != '':
            title = title + ' (' + category + ')'

        self.headerBar.set_title(title)
        self.midi.patch_change(msb, lsb, pc)


    def on_favourite(self, button, *data):
        """Handle click on a favourite button"""
        if len(data) < 1:
            return

        index = data[0]
        section = self.configuration.get_fav_section(index)

        if section is None:
            return

        if not self.configuration.has_favourite(index):
            return

        msb, lsb, pc, _sound = self.configuration.get_favourite(index)

        self.sound_select_by_patch(msb, lsb, pc)
        self.on_activate_sound(self.buttonSoundActivate)


    def on_favourite_set(self, button, *data):
        """Handle click on a set favourite button"""
        if len(data) < 1:
            return

        index = data[0]
        section = self.configuration.get_fav_section(index)

        if section is None:
            return

        msb, lsb, pc, sound, _category = self.sound_get_selection_info()

        if not self.configuration.is_valid_fav_content(msb, lsb, pc, sound):
            return

        if not self.configuration.set_favourite(index, msb, lsb, pc, sound):
            return

        self.buttonFavs[index].set_label(sound)
        self.buttonsFavSet[index].set_label('Set fav #' + str(index) + ' (*)')


    def on_input_device_changed(self, combo):
        """Change the input device"""
        #treeIter = combo.get_active_iter()

        #if treeIter is None:
        #    self.currentCategory = None
        #    return

        #model = combo.get_model()
        #self.currentCategory = model[treeIter][0]
        pass


    def on_output_device_changed(self, combo):
        """Change the output device"""
        pass


    def on_input_channel_changed(self, combo):
        """Change the input channel"""
        pass


    def on_output_channel_changed(self, combo):
        """Change the output channel"""
        pass


    def on_refresh_devices(self, button):
        """Refresh the input and output lists"""
        pass



win = Application()
win.connect('destroy', Gtk.main_quit)
win.show_all()
Gtk.main()
