#!/usr/bin/env python
import os
import pprint
import time

from atsd_client import connect, connect_url
from atsd_client.services import EntitiesService

'''
Delete dependent entities (containers, images, network, volumes) based on docker-host tag
'''

tag_name = 'docker-host'
tag_value = 'dockerhost.example.org'

tags_printer = pprint.PrettyPrinter(indent=4)

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'username', 'password')

# Initialize services
entity_service = EntitiesService(connection)

entity_filter = "lower(tags." + tag_name+ ") = '" + tag_value.lower() + "'"
# find dependent entities, with specified docker-host tag
entities = entity_service.list(expression=entity_filter, limit=0, tags="*")

print("- DELETE " + str(len(entities)) + " entities for " + tag_value)

for entity in entities:

    if entity.name == tag_value:
        # ignore the docker host itself, host is deleted later
        continue

    print(" - Deleting " + entity.tags.get('docker-type', '') + " : " + entity.name + " : " + entity.tags.get('name', ''))
    #tags_printer.pprint(entity.tags)
    # Uncomment next line to delete
    #entity_service.delete(entity)
