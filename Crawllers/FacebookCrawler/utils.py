import time
import re
import calendar

def time_parser(time_):
    try:
        if 'hrs' in time_:
            time_=int((time.time()-int(time_.replace('hrs',''))))
        elif len(re.findall(r"20[0-2][0-9]",time_))==0:
            time_=(time_+' 2021').replace(' at','')
            time_=calendar.timegm(time.strptime(time_,"%B %d %H:%M %p %Y"))
        else:
            time_=time_.replace(',','').replace(' at','')
            time_=calendar.timegm(time.strptime(time_,"%B %d %Y %H:%M %p"))
    except:
        try:
            time_ = calendar.timegm(time.strptime("1 "+time_+" 0:01 AM", "%d %B %Y %H:%M %p"))
        except:
            try:
                time_ = calendar.timegm(time.strptime(time_ + " 0:01 AM", "%B %d %Y %H:%M %p"))
            except:
                return "**"+time_
    return time_