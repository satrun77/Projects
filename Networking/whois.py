"""
Whois Search Tool - Enter an IP or host address and have it look it up through whois and return the results to you.
"""

import urllib2
import json


if __name__ == '__main__':
    # Query whomsy.com whois API
    #-------------------------------

    # IP address | API URL | Request headers
    ip_address = raw_input("IP or host address >> ").strip()
    api_url = 'http://whomsy.com/api/%s?output=json' % ip_address
    request_headers = {
        "Content-Type": "application/json",
        "Accept": "*/*"
    }

    # Connect to whois API
    request = urllib2.Request(api_url, headers=request_headers)
    file_object = urllib2.urlopen(request)

    try:
        # Convert the string response into JSON object
        response = json.loads(file_object.read())

        # Show error message if domain not found in whois
        if response['type'] != 'success':
            print '**Domain name not found in Whois server.'
        else:
            print 'Domain:\t%s\n' % response['domain']
            print 'Message:' + response['message']
    except:
        print '**Unable to query the whois server.'
