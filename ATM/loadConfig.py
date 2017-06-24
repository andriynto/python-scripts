# -*- coding: utf-8 -*-
#!/usr/bin/python
#---------------------------------------
# loadConfig.py
# (c) Jansen A. Simanullang
# @Medan City, Juni 2017
#---------------------------------------
# Python usage:
# loadConfig.py
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
import os, ConfigParser
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
scriptDirectory = os.path.dirname(os.path.abspath(__file__)) + "/"
configPath = scriptDirectory+ "conf/config.ini"
configPath = configPath.replace("/","//")
Config = ConfigParser.ConfigParser()
Config.read(configPath)
def readConfig(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
#-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
