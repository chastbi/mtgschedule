import xmltodict, os
from mtgschedule.settings import MRF_LIST
from datetime import datetime


def get_mrf_list():
    '''
    makes dictionary of all xml data from each mrf in a directory
    '''
    mrflist = {}
    for filename in os.listdir(MRF_LIST):
        mrfpath = os.path.join(MRF_LIST, filename)
        with open(mrfpath) as fd:
            mrf = xmltodict.parse(fd.read())
        fd.close()
        mrflist[filename] = {}
        mrflist[filename] = (mrf['my:PEMeetingRequestForm'])
    return mrflist


def create_mrf_dict():
    '''
    creates an easier dictionary of mrf data to work with. contains only data needed for the schedules
    '''
    xmllist = get_mrf_list()
    mrf_dict = {}
    for mrf, value in xmllist.items():

        mrf_dict[mrf] = {'clientname':value['my:ClientInfoGroup']['my:ClientName']['#text'],
                         'date':datetime.date(datetime.strptime(value['my:MTGInfoGroup']['my:MtgDate']['#text'],
                                                                '%Y-%m-%d')),
                         'city':value['my:OnsiteInfoGrp']['my:City'],
                         'state':value['my:OnsiteInfoGrp']['my:State'],
                         'status':value['my:MTGGroup']['my:SchedulerStatus'],
                         }
        if value['my:MTGGroup']['my:Presenter1']['#text']:
            mrf_dict[mrf]['presenter1'] = value['my:MTGGroup']['my:Presenter1']['#text']
        try:
            mrf_dict[mrf]['presenter2'] = value['my:MTGGroup']['my:Presenter2']['#text']
        except:
            mrf_dict[mrf]['presenter2'] = None
        try:
            mrf_dict[mrf]['presenter3'] = value['my:MTGGroup']['my:Presenter3']['#text']
        except:
            mrf_dict[mrf]['presenter3'] = None
        try:
            mrf_dict[mrf]['presenter4'] = value['my:MTGGroup']['my:Presenter4']['#text']
        except:
            mrf_dict[mrf]['presenter4'] = None
        try:
            mrf_dict[mrf]['meetinglead'] = value['my:MTGGroup']['my:MtgLead']['#text']
        except:
            mrf_dict[mrf]['meetinglead'] = None
        mtgcount = 0
        for timegroup in value['my:MTGRequestGroup']['my:MTGTimesGroup']:
            mtgcount += 1
            newmtg = 'mtgtime' + str(mtgcount)
            newtopic = 'mtgtopic' + str(mtgcount)
            mrf_dict[mrf][newmtg] = timegroup['my:Times']['#text']
            mrf_dict[mrf][newtopic] = timegroup['my:MtgTopic']
    return mrf_dict

