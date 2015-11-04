__author__ = 'labx'

import urllib



XRAY_SERVER_URL = "http://x-server.gmca.aps.anl.gov/"

class HttpManager():

    @classmethod
    def send_xray_server_request(cls, application, parameters):

        data = urllib.parse.urlencode(parameters)
        data = data.encode('utf-8') # data should be bytes
        req = urllib.request.Request(XRAY_SERVER_URL + application, data)
        resp = urllib.request.urlopen(req)

        return resp.read()
