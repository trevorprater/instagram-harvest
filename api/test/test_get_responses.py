import os, sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pprint import pprint

import ujson as json

content = open('sample_response1.json').read()
d = json.loads(content)
pprint(d)
print len(d)
