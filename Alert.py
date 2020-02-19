# This module will maintain statistics wrt to time for logs. We can either purge the statistics at a
#  frequency (param alert_purge_freq in the config) or we can generate a consolidated report in the end.

from LogState import LogState
from LogLine import LogLine
from sortedcontainers import SortedDict
import json

class StatsState(object):
    def __init__(self, *args, **kwargs):
        self.totalHits_=0
        self.hitsPerUser_=json.loads("{}")
        self.hitsPerSection_=json.loads("{}")
        self.hitsPerRequest_=json.loads("{}")
        self.hitsPerStatus_=json.loads("{}")
        self.hitsPerHost_=json.loads("{}")
        self.printed_=bool(False)
        return super().__init__(*args, **kwargs)

    def set_total_hits(self, hits):
        self.totalHits_=hits
        return
    def increment_hits_per_section(self, request):
        tokens=request.split();#split on space
        temp=tokens[1].split("/");
        section="/"+temp[1]
        if section not in self.hitsPerSection_:
            self.hitsPerSection_[section]=1
        else:
            self.hitsPerSection_[section]+=1
        return
    def increment_total_hits(self):
        self.totalHits_+=1
        return

    def increment_hits_per_user(self, user):
        if user not in self.hitsPerUser_:
            self.hitsPerUser_[user]=1
        else:
            self.hitsPerUser_[user] +=1
        return

    def increment_hits_per_host(self, host):
        if host not in self.hitsPerHost_:
            self.hitsPerHost_[host]=1
        else:
            self.hitsPerHost_[host] +=1
        return

    def increment_hits_per_request(self, req):
        if req not in self.hitsPerRequest_:
            self.hitsPerRequest_[req]=1
        else:
            self.hitsPerRequest_[req] +=1
        return

    def increment_hits_per_status(self, status):
        if status not in self.hitsPerStatus_:
            self.hitsPerStatus_[status]=1
        else:
            self.hitsPerStatus_[status] +=1
        return

    def __repr__(self):
        self.printed=bool(True)
        ret=json.loads("{}")
        ret["total_hits"]=self.totalHits_
        ret["hits_per_section"]=self.hitsPerSection_
        ret["hits_per_user"]=self.hitsPerUser_
        ret["hits_per_request"]=self.hitsPerRequest_
        ret["hits_per_host"]=self.hitsPerHost_
        ret["hits_per_status"]=self.hitsPerStatus_
        return ret.__repr__()

class MonitorState:
    def __init__(self, time, totalHits,config):
        self.time_=time
        self.totalHits_=totalHits;
        self.printed_=bool(False)
        self.config_=config
        return 

    def __repr__(self):
        self.printed_=bool(True)
        ret=f'INFO: QPS {self.totalHits_/self.config_.monitorTime_} at time {self.time_} is in permissible range'
        if self.totalHits_/self.config_.monitorTime_ > self.config_.maxQps_:
            ret=f'ALERT: High Traffic generated an {self.totalHits_/self.config_.monitorTime_} hits at time {self.time_}'
        elif self.totalHits_/self.config_.monitorTime_ < self.config_.minQps_:
            ret=f'ALERT: Low Traffic generated an {self.totalHits_/self.config_.monitorTime_} at time {self.time_}'

        return ret.__repr__()

class Alert(object):
    """description of class"""
    def __init__(self, config):
        self.config_=config
        self.statsStateDict_=SortedDict()
        self.monitorStateDict_=SortedDict()
        return
    def displayAlerts(self):
        for time in self.statsStateDict_:
            if self.statsStateDict_[time].printed_ == bool(False):
                print(f'stats for last {self.config_.statsTime_} secs for {time} is {self.statsStateDict_[time]}')
        for time in self.monitorStateDict_:
            if self.monitorStateDict_[time].printed_ == bool(False):
                print(f'{self.monitorStateDict_[time]}')
        
        return
    def updateAlertState(self,logState):
        if not logState.keys():
            return

        lastInsertedTime = logState.keys()[-1]
        if lastInsertedTime in self.statsStateDict_.keys():
            logline = logState.getElem(int(lastInsertedTime))[-1]#last inserted element in the list
            self.statsStateDict_[lastInsertedTime].increment_total_hits()
            self.statsStateDict_[lastInsertedTime].increment_hits_per_host(logline.getRemoteHost())
            self.statsStateDict_[lastInsertedTime].increment_hits_per_user(logline.getUser())
            self.statsStateDict_[lastInsertedTime].increment_hits_per_request(logline.getRequest())
            self.statsStateDict_[lastInsertedTime].increment_hits_per_status(logline.getStatus())
            self.statsStateDict_[lastInsertedTime].increment_hits_per_section(logline.getRequest())
        else:
            statsTimeBack = logState.getLowerBound(int(lastInsertedTime)-int(self.config_.statsTime_))
            diffStartTime = statsTimeBack[0]
            if int(lastInsertedTime)-int(diffStartTime) == self.config_.statsTime_:
                count=0
                currentStatsState=StatsState()
                for time in statsTimeBack:
                    temp = logState.getElem(time)
                    count += len(temp)
                    for logline in temp:
                        currentStatsState.increment_hits_per_host(logline.getRemoteHost())
                        currentStatsState.increment_hits_per_user(logline.getUser())
                        currentStatsState.increment_hits_per_request(logline.getRequest())
                        currentStatsState.increment_hits_per_status(logline.getStatus())
                        currentStatsState.increment_hits_per_section(logline.getRequest())
                currentStatsState.set_total_hits(count)
                self.statsStateDict_._setitem(lastInsertedTime,currentStatsState)
   
        if int(lastInsertedTime) not in self.monitorStateDict_.keys():
            MonitorTimeBack = logState.getLowerBound(int(lastInsertedTime)-int(self.config_.monitorTime_))
            diffStartTime = MonitorTimeBack[0]
            if int(lastInsertedTime) - int(diffStartTime) == int(self.config_.monitorTime_):
                count =0
                currentMonitorState=MonitorState(int(lastInsertedTime),count,self.config_)
                for time in MonitorTimeBack:
                    temp = logState.getElem(time)
                    count += len(temp)
                currentMonitorState.totalHits_=count
                self.monitorStateDict_[lastInsertedTime]=currentMonitorState
        else:
            self.monitorStateDict_.get(int(lastInsertedTime)).totalHits_ +=1
            self.monitorStateDict_.get(int(lastInsertedTime)).printed_=False
        


