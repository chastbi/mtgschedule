import xmltodict, os
from mtgschedule.settings import MRF_LIST


def get_mrf_list():
    mrflist = []
    for filename in os.listdir(MRF_LIST):
        mrfpath = os.path.join(MRF_LIST, filename)
        with open(mrfpath) as fd:
            mrf = xmltodict.parse(fd.read())
        fd.close()
        mrflist.append(mrf['my:PEMeetingRequestForm'])
    return mrflist
