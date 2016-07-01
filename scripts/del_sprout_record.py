# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 15:11:36 2016

@author: boucherv
"""

import utils
from cloudify import ctx

dns_ip = ctx.target.node.properties.ip


designate_client = utils.get_client(dns_ip)

utils.delete_record(designate_client, "clearwater.local.", "sprout.clearwater.local.", "A", str(ctx.source.instance.host_ip))