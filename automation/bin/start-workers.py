import sys
import os
import uuid
import random
from pprint import pprint

import digitalocean

TOKEN = '8154c657e91690c37c6b6ee670aa8fcb0090e87ebb71593f1127fe20d6f7f31e'
num_to_start = int(sys.argv[1])
regions = ['nyc1','nyc2', 'nyc3','sfo1','sfo2', 'ams2', 'ams3', 'sgp1', 'lon1', 'fra1','tor1', 'blr1']

manager = digitalocean.Manager(token=TOKEN)
keys = manager.get_all_sshkeys()

for ctr in range(num_to_start):
    _region = random.choice(regions)
    droplet = digitalocean.Droplet(token=TOKEN,name=str(uuid.uuid4()),region=_region,image='19113329',size_slug='512mb',backups=False, ssh_keys=keys)
    droplet.create()

    print 'Successfully started worker #{}'.format(ctr)



