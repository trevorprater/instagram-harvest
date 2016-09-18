import sys
from pprint import pprint

import digitalocean

manager = digitalocean.Manager(token='8154c657e91690c37c6b6ee670aa8fcb0090e87ebb71593f1127fe20d6f7f31e')
droplets = manager.get_all_droplets()
num_to_kill = int(sys.argv[1])

for ctr, droplet in enumerate(droplets):
    pprint(droplet.__dict__['created_at'])
    if ctr > num_to_kill:
        sys.exit()

    if droplet.__dict__['size']['memory'] == 512:
        print 'Destroying droplet: {}'.format(droplet.__dict__['name'])
        res = False
        try:
            res = droplet.destroy()
        except Exception as e:
            print e
            continue
        if res:
            print 'Destroy successful!'
        else:
            print 'Could not destroy droplet!'
