# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 15:11:36 2016

@author: boucherv
"""


from cloudify import ctx
import designateclient.v2.client as dgclient
from keystoneauth1 import session as keystone_session


def get_client(dns_ip):
    session = keystone_session.Session()
    return dgclient.Client(endpoint_override="http://" + dns_ip + ":9001/v2", session=session)
    

def create_record(designate_client, zone_name, recordset_name, type_, new_record):
    recordsets = designate_client.recordsets.list(zone_name)
    recordset_exist = False
    for recordset in recordsets:
        if recordset['name'] == recordset_name:
            recordset_exist = True

    if not recordset_exist:
        return designate_client.recordsets.create(zone_name, recordset_name, type_, [new_record])
    else:
        recordset = designate_client.recordsets.get(zone_name, recordset_name)
        records = recordset.get('records')
        records.append(new_record)
        data = {
                'name': recordset_name,
                'type': type_,
                'records': records
        }
        return designate_client.recordsets.update(zone_name, recordset_name, data)
        
dns_ip = ctx.target.node.properties.ip


designate_client = get_client(dns_ip)

create_record(designate_client, "clearwater.local.", "sprout.clearwater.local.", "A", str(ctx.source.instance.host_ip))