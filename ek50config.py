import configparser

class Ek50Config:
    def __init__(self):
        """Initialization"""
        self.config_location = 'ek50.config'
        self.default_fav_rows = 5
        self.default_fav_cols = 4

        self.config = configparser.ConfigParser(strict = True)
        self.set_default_config()
        self.config.read(self.config_location)
        self.adjust_favourites()


    def set_default_config(self):
        """Sets the default configuration"""
        self.config.read_dict({
            'config': {
                'fav_rows': str(self.default_fav_rows),
                'fav_cols': str(self.default_fav_cols),
                'current_msb': '0',
                'current_lsb': '0',
                'current_pc': '0'
            }
        })


    def save(self):
        """Saves the current configuration"""
        with open(self.config_location, 'w') as configfile:
            self.config.write(configfile)


    def get_default_sound(self):
        """Get the last sound activated"""
        msb = self.config['config'].getint('current_msb')
        lsb = self.config['config'].getint('current_lsb')
        pc = self.config['config'].getint('current_pc')

        return msb, lsb, pc


    def set_default_sound(self, msb, lsb, pc):
        """Set the last activated sound"""
        self.config['config']['current_msb'] = str(msb)
        self.config['config']['current_lsb'] = str(lsb)
        self.config['config']['current_pc'] = str(pc)
        self.save()


    def adjust_favourites(self):
        """Guarantee that the favourites in the configuration are ok, so that any other function here
        do not have to check for valid values.
        """
        changed = False

        rows = self.config['config'].getint('fav_rows')

        if type(rows) is not int or rows <= 0:
            rows = self.default_fav_rows
            self.config['config']['fav_rows'] = str(self.default_fav_rows)
            changed = True

        cols = self.config['config'].getint('fav_cols')

        if type(cols) is not int or cols <= 0:
            cols = self.default_fav_cols
            self.config['config']['fav_cols'] = str(self.default_fav_cols)
            changed = True

        for n in range(rows * cols):
            section = self.get_fav_section(n)

            if section is None:
                section = 'fav' + str(n)
                self.config.add_section(section)
                changed = True

            msb = self.config[section].getint('msb')
            lsb = self.config[section].getint('lsb')
            pc = self.config[section].getint('pc')
            name = self.config[section].get('name')

            if not self.is_valid_fav_content(msb, lsb, pc, name):
                self.config[section]['msb'] = '-1'
                self.config[section]['lsb'] = '-1'
                self.config[section]['pc'] = '-1'
                self.config[section]['name'] = ''
                changed = True

        if changed:
            self.save()


    def get_fav_rows(self):
        """Get the number of favourites rows"""
        return self.config['config'].getint('fav_rows')


    def get_fav_cols(self):
        """Get the number of favourites cols"""
        return self.config['config'].getint('fav_cols')


    def get_fav_count(self):
        """Get the number of favourites"""
        rows = self.get_fav_rows()
        cols = self.get_fav_cols()

        return rows * cols


    def get_fav_section(self, favNum):
        """Get the section corresponding to the fav number or None if it does not valid"""
        if type(favNum) is not int or favNum not in range(self.get_fav_count()):
            return None

        section = 'fav' + str(favNum)

        if not self.config.has_section(section):
            return None

        return section


    def is_valid_fav_content(self, msb, lsb, pc, name):
        """Check if this is a valid fav content"""
        if type(msb) is not int or msb < 0:
            return False

        if type(lsb) is not int or lsb < 0:
            return False

        if type(pc) is not int or pc < 0:
            return False

        if type(name) is not str or len(name) < 1:
            return False

        return True


    def has_favourite(self, favNum):
        """Check if we have a favourite defined in the specified position"""
        msb, lsb, pc, name = self.get_favourite(favNum)

        return msb is not None and lsb is not None and pc is not None and name is not None


    def get_favourite(self, favNum):
        """Get a favourite"""
        section = self.get_fav_section(favNum)

        if section is None:
            return None, None, None, None

        msb = self.config[section].getint('msb')
        lsb = self.config[section].getint('lsb')
        pc = self.config[section].getint('pc')
        name = self.config[section].get('name')

        if not self.is_valid_fav_content(msb, lsb, pc, name):
            return None, None, None, None

        return msb, lsb, pc, name


    def set_favourite(self, favNum, msb, lsb, pc, name):
        """Save a favourite"""
        section = self.get_fav_section(favNum)

        if section is None:
            return False

        if not self.is_valid_fav_content(msb, lsb, pc, name):
            return False

        self.config[section]['msb'] = str(msb)
        self.config[section]['lsb'] = str(lsb)
        self.config[section]['pc'] = str(pc)
        self.config[section]['name'] = name
        self.save()

        return True
