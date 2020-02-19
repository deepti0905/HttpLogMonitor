# Maintains SortedDictionary of Logs
#Information is saved as 
#<TimeStamp>- List of LogLines 
#In the realworld system it can be possible that same log is received multiple times due to change in network topology.
# LogState will only maintain unique logs in memory, duplicate logs will be ignored. 
# LogState also has a support of clearing old logs from memory, this is goverened by parameter flush_state in the config

from LogLine import LogLine
from collections import OrderedDict
from sortedcontainers import SortedDict

class LogState(object):
    """This class will hold the state of log file in case we are unable to hold the complete file in memory we can clean older stats"""
    
    def __init__(self):
        self.logState_=SortedDict()
        return

    def addLog(self,line):
        ll=LogLine()
        ll.populate(line)
        date = ll.getDate()
        
        if int(date) not in self.logState_:
            self.logState_[int(date)]=list()
            
        if len(self.logState_[int(date)]) == 0:
            self.logState_[int(date)].append(ll)
        else:
            #check if it is unique
            #same log can come multiple times but should not impact the logstate
            found=bool(False)
            for elem in self.logState_[int(date)]:
                if elem == ll:
                    
                    found=bool(True)
                    break
            if found:
                return False
            if found == bool(False):
                self.logState_[int(date)].append(ll)
                
        return True
    
    def getElem(self, key):
        return self.logState_[int(key)]

    def FlushOldLogs(self, maxLogCount):
        #print(f'FlushOldLogs ')
        if maxLogCount <=0: #no need to flush
            return
        keyList=self.logState_.keys()
        totalKeys= len(keyList)
        #print(f'FlushOldLogs {totalKeys} {maxLogCount}')
        if totalKeys <= maxLogCount:
            return
        deletKeyCount = totalKeys - maxLogCount
        for i in range(0,deletKeyCount):
            key=keyList[i]
            del self.logState_[key]
        return
    def keys(self):
        return self.logState_.keys()

    def getLowerBound(self, time):
        return list(self.logState_.irange(minimum=int(time)))


    def print(self):
        for key in self.logState_:
            print(f'For Key as {key}')
            value=self.logState_[key]
            for elem in value:
                print(elem)
        return


