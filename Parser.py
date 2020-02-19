# Parser can be visualized as a real life component that will be receiving streams of logs. I've purposefully went over one line at a time 
# rather than loading complete file in memory. Parser will be maintaining a member variable logState and Alert and will
#  keep updating them from time to time

import pprint
from LogState import LogState
from LogLine import LogLine
from Config import Config
from Alert import Alert
class Parser(object):
    """Will Parse the Log file line by line"""
   # file_path_
    def __init__(self, filePath, config):
        self.filePath_=filePath
        self.config_=config
        self.alert_=Alert(self.config_)
        return
    def Process(self):
        count=0
        self.logState_= LogState()
        timeStampInAction=0
        ll=LogLine()
        with open(self.filePath_) as fp:
            line = fp.readline()
            
            while line:
                count+=1
                if count > 1:
                    #   We keep updating the log state but we'll publish alerts at certain frequency
                    #   This is done to avoid missing logs that are received staggered but belong to the same time stamp
                    #   Also we don't want to delay the log purge till we have read the entire file as that may result in delayed alerts
         
                    if bool(self.config_.printStatsInTheEnd_)== False and self.config_.alertPurgeFreq_ >0 and count%self.config_.alertPurgeFreq_ == 0:
                        self.alert_.displayAlerts()
                    if self.logState_.addLog(line):
                        self.alert_.updateAlertState(self.logState_)
                        self.logState_.FlushOldLogs(self.config_.flushState_)
                line = fp.readline()
        if count%self.config_.alertPurgeFreq_ !=0 or self.config_.printStatsInTheEnd_:
            self.alert_.displayAlerts()

        return
    


