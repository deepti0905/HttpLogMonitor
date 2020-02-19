# Is a structure which contains log attributes stored as member variables
import json
class LogLine(object):
    """Will Have information of one line of Log"""
    #"remotehost","rfc931","authuser","date","request","status","bytes"

    def __init__(self):
      #  self.temp=line
      # x=self.temp.spit(",")
        self.remotehost_=""
        self.rfc_=""
        self.authuser_=""
        self.date_=""
        self.request_=""
        self.status_=""
        self.bytes_=""
        return

    def populate(self,line):
        temp=line
        x=temp.split(",")
        self.remotehost_=x[0]
        self.rfc_=x[1]
        self.authuser_=x[2]
        self.date_=x[3]
        self.request_=x[4]
        self.status_=x[5]
        self.bytes_=x[6]
        return

    def getDate(self):
        return self.date_
    def getRemoteHost(self):
        return self.remotehost_
    def getUser(self):
        return self.authuser_
    def getRequest(self):
        return self.request_
    def getStatus(self):
        return self.status_
    def __repr__(self):
        ret = json.loads("{}")
        ret["remotehost"]=self.remotehost_
        ret["rfc"]=self.rfc_
        ret["authuser"]=self.authuser_
        ret["date"]=self.date_
        ret["request"]=self.request_
        ret["status"]=self.status_
        ret["bytes"]=self.bytes_
        return ret.__repr__()

    def __eq__(self, other):
        return self.remotehost_ == other.remotehost_ and self.rfc_==other.rfc_ and  self.authuser_== other.authuser_ and self.date_== other.date_ and   self.request_== other.request_ and  self.status_== other.status_ and    self.bytes_== other.bytes_




