#!/usr/bin/env python2
#
# name: ip-check
#
import sys
import json
import urllib2
import re


# r = urllib2.urlopen('http://ipinfo.io/24.39.138.138/geo')
# data = r.read()
# a = json.loads(data)
# print a['ip']

format = "%-16s %-10s %-20s %-20s %-25s"

def showHeader():
    print '-' * 91
    print format % ('IP ADDRESS', 'COUNTRY', 'REGION', 'CITY', 'LOCATION')
    print '-' * 91

class IpCheck(object):
    """IpCheck class methods"""

    def __init__(self, ip):
        self.ip     = ip

    def isValid(self):
       pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
       if re.match(pattern, self.ip):
            return True
       else:
            return False

    def fetchData(self):
        if not self.isValid():
            print "ERROR: Entered IP address (%r) is NOT VALID" % self.ip
            sys.exit(1)

        try: 
            response = urllib2.urlopen('http://ipinfo.io/'+self.ip+'/geo')
            data = response.read()
            data = json.loads(data)
        except urllib2.HTTPError, e:
            print "HTTPError = %r" % str(e.code)
            sys.exit(1)
        except urllib2.URLError, e:
            print "URLError = %r" % str(e.reason)
            sys.exit(1)
        except Exception:
            import traceback
            print "generic exception: %r" % traceback.format_exc()
            sys.exit(1)

        return data

    def show(self, data):
        try:
            print format % (data['ip'], data['country'], data['region'], data['city'], data['loc'])
        except KeyError, e:
            print "%s : KeyError: %s" % (self.ip, str(e))


def main(argv):

    if not argv:
        print "no arg passed. print usage"
        sys.exit(1)

    if len(argv) == 1:
        showHeader()
        ipCheck = IpCheck(argv[0])
        data = ipCheck.fetchData()
        ipCheck.show(data)
    else:
        showHeader()
        for ip in argv:
            ipCheck = IpCheck(ip)
            data = ipCheck.fetchData()
            ipCheck.show(data)

if __name__ == '__main__':
    main(sys.argv[1:])
