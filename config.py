import os
import ConfigParser

class ConfigOP(iniName):
    config = ConfigParser.ConfigParser();
    config.read(iniName)

    def sections()
    def readSectionMap(section):
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

    
    
        bStartTime = False
        preTime = datetime
        difflist = collections.OrderedDict()
        startTime = datetime
        for item in self.performanceDict:
            difflist[item] = collections.OrderedDict()
            for item1 in self.CompStr[item]:
                if bStartTime == False:
                    difflist[item][item1] = 0
                    preTime = startTime = timelist[item][item1]
                    bStartTime = True
                else:
                    if item1 in timelist[item]:
                        difflist[item][item1] = (timelist[item][item1]-preTime).total_seconds()
                        stimelist[item] = timelist[item][item1] - startTime
                        preTime = timelist[item][item1]
                    else:
                        difflist[item][item1] = 0


        for item in self.performanceDict:
            print(item+':', stimelist[item].total_seconds())
            for item1 in self.CompStr[item]:
                print('    '+self.CompStr[item][item1]+': ',difflist[item][item1])
                    