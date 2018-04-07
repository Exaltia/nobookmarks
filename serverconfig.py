import configparser
def serverconfig():
    myconfig = configparser.ConfigParser()
    myconfig.read('serverconfig.cfg')
    return myconfig