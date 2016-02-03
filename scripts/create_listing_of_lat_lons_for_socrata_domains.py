import os
os.system('wget -O domains.csv https://gsa.github.io/data/dotgov-domains/2014-12-01-full.csv')

import csv
import sys
domains = {}
f = open('domains.csv', 'rt')
try:
    reader = csv.reader(f)
    next(reader, None)
    for row in reader:
        domains[row[0].lower()] = row[-2] + ', '+ row[-1]
finally:
    f.close()
import requests
import os
import re
portals = []
domains = {}
results = requests.get('http://api.us.socrata.com/api/catalog/v1/domains').json()['results']
print '# of results', len(results)
print 'pass get'
domains = dict(domains)
for portal in results:
    #print portal
    d = {'domain': str(portal['domain'])}
    if d['domain'].endswith('.gov'):
        for gov_domain in domains:
            #print gov_domain
            if gov_domain in d['domain']:
                d['location'] = str(domains[gov_domain])

                break
    else:
        root_domain = d['domain'].split('.')
        root_domain = root_domain[-2]+'.'+root_domain[-1]
        whois = os.popen('whois %s' % root_domain).read()
        m = re.search('Billing Contact City:\s*(?P<city>.*)', whois)
        if m:
            city = m.group('city')
        m = re.search('Billing Contact State/Province:\s*(?P<state>.*)', whois)
        if m:
            state = m.group('state')
        if city and state:
            d['location'] = '%s, %s' % (city, state)

    if 'location' in d:
        #print 'http://nominatim.openstreetmap.org/search/?q=%s,usa&format=json' % (d['location'])
        geo = requests.get('http://nominatim.openstreetmap.org/search/?q=%s,usa&format=json' % (d['location'])).json()
        if not len(geo) > 0:
            continue
        geo = geo[0]
        d['lat'] = geo['lat']
        d['lon'] = geo['lon']
        domains[str(portal['domain'])] = {'lat': geo['lat'], 'lon': geo['lon']}
with open('data/lat_lons_for_socrata_domains.json', 'w') as f:
    f.write(json.dumps(portals))
