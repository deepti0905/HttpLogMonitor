#Config File:
#Sample Config File:
#{
#  "stats_time": 10,
#  "monitor_time": 120,
#  "max_qps": 12,
#  "min_qps": 10,
#  "alert_purge_freq": 50,
#  "print_stats_in_the_end": 1,
#  "flush_state":130
#}
#Meaning of each attribute in the config file
# stats_time : This will indicate the window for which we'll be monitoring statistics. In this code I'm monitoring total hits,
# hits per user, hits per request, hits per status, hits per host
#monitor_time: This will indicate the window for which we'll be generating alerts i.e. QPS allowed in a specific range or not
#max_qps: This indicates the MAX QPS allowed in the monitor time window
#min_qps: This indicates the MIN QPS allowed in the monitor time window
#alert_purge_freq: We are assuming the log file is huge and it can be possible that the user may not want to wait till the 
#entire file is read to generate alerts. With this setting we'll purge statistics and monitor stats on the screen after
# every x logs (where x is alert purge Freq).Please note too low alert_purge_freq can result in false alarms.
#print_stats_in_the_end: This is a boolean parameter, which if provided we will print statistics in the end, by that we'll 
# ignore alert purge freq
#flush_state: We know the log file is huge and we may not be able to contain it in memory. With this setting we'll flush 
#the old keys and we'll always maintain
#timestamps being considered and in memory as maximum as flush_state. The recommended flush_state must be greater than monitor time window

import json

class Config(object):
    """description of class"""
    def __init__(self, *args, **kwargs):
        #Default fields
        self.statsTime_=10 #Print stats every 10 sec
        self.monitorTime_=120 #Print State of the system every 2 min
        self.maxQps_=12 #Max QPS per monitor time
        self.minQps_=10#Min QPS per monitor time
        self.alertPurgeFreq_=50 # after every 50 logs we check for the state, only effective if printStatsInTheEnd is False
        self.printStatsInTheEnd_=True
        self.flushState_=-1
        return super().__init__(*args, **kwargs)

    def populate(self, filePath):
        with open(filePath) as f:
            try:
                data = json.load(f)
            except ValueError as e:
                print(f'Config file {filePath} was invalid, this is a optional argument we are going with the default setting! ')
                return False
            #if config was valid pick arguments provided
            if "stats_time" in data:
                self.statsTime_=int(data["stats_time"])
            if  "monitor_time" in data:
                self.monitorTime_=int(data["monitor_time"])
            if  "max_qps" in data:
                self.maxQps_=int(data["max_qps"])
            if  "min_qps" in data:
                self.minQps_=int(data["min_qps"])
            if  "alert_purge_freq" in data:
                self.alertPurgeFreq_=int(data["alert_purge_freq"])
            if  "print_stats_in_the_end" in data:
                self.printStatsInTheEnd_=bool(data["print_stats_in_the_end"])
            if "flush_state" in data:
                self.flushState_=int(data["flush_state"])
        return



    


