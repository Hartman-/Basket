import ConfigParser

CONFIG_PATH = '../config/'
CONFIG_FILES = ['X:/Classof2017/LobstersAreWeird/basket/config/boiler.conf']

parser = ConfigParser.ConfigParser()


def open_config_files():
    parser.read(CONFIG_FILES)


def unpack_list(in_list):
    return in_list.split(',')


def get_config_value(section, option):
    open_config_files()

    if parser.has_section(section):
        if parser.has_option(section, option):
            value = parser.get(section, option)

            # Unpacking a delimited list from the config file
            if ',' in value:
                return unpack_list(value)

            return value
        else:
            print 'No Option: %s Exists' % option
            return None
    else:
        print 'No Section: %s Exists' % section
        return None


if __name__ == "__main__":
    open_config_files()
    print get_config_value('law', 'stages')