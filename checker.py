from urllib.parse import urlparse
import threading
import whois
import json
import os

with open('sites.json') as json_file:
  data = json.load(json_file)

ads = []

for ad in data:
  site_url = '.'.join(urlparse(ad['site']).netloc.split('.')[-2:])
  found = False
  for adv in ads:
    if site_url == adv['domain']:
      found = True
      break
  if not found:
    ads.append({"domain": site_url, "coords": ad['coords']})

available_sites = []

checked = 0

def check_sites(sites):
  global checked
  for site in sites:
    print("Checking: " + site['domain'] + " (" + str(checked) + "/" + str(len(ads)) + ")")
    checked += 1
    try:
      whois.whois(site['domain'])
      print('{} is registered'.format(site['domain']))
    except:
      print('{} is not registered'.format(site['domain']))
      available_sites.append(site)
      pass

chunk_size = 10

threads = []
for i in range(0, len(ads), chunk_size):
  t = threading.Thread(target=check_sites, args=(ads[i:i+chunk_size],))
  threads.append(t)
  t.start()

# wait for all threads to finish
for t in threads:
  t.join()

sorted_sites = []
for site in available_sites:
  start_coords = [site['coords'].split(',')[0], site['coords'].split(',')[1]]
  end_coords = [site['coords'].split(',')[2], site['coords'].split(',')[3]]

  # calculate size
  x_diff = end_coords[0] - start_coords[0]
  y_diff = end_coords[1] - start_coords[1]
  size = x_diff * y_diff

  if len(sorted_sites) == 0:
    sorted_sites.append({"site": site, "size": size})
  else:
    for i in range(len(sorted_sites)):
      if size < sorted_sites[i]['size']:
        sorted_sites.insert(i, {"site": site, "size": size})
        break
      elif i == len(sorted_sites) - 1:
        sorted_sites.append({"site": site, "size": size})
        break
  

print("\nAvailable sites:")
for site in sorted_sites:
  print('domain: {} - coords: {}'.format(site['site']['domain'], site['site']['coords']))
