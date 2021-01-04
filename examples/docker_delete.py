#!/usr/bin/env python
import os
import pprint
import time

from atsd_client import connect, connect_url
from atsd_client.services import EntitiesService, MetricsService

'''
Locate entities (Docker hosts) that have not inserted data for more than 7 days.
Delete dependent entities (containers, images, network, volumes) based on entity-tag set to the given Docker host.
Delete Docker host entities themselves.
'''

# Uncomment the next two lines to set custom local timezone
# os.environ['TZ'] = 'Europe/London'
# time.tzset()

tags_printer = pprint.PrettyPrinter(indent=4)

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'username', 'password')

# Initialize services
entity_service = EntitiesService(connection)
metric_service = MetricsService(connection)

# select all entities that collect this metric
# this metric is collected by docker hosts
docker_hosts = metric_service.series('docker.cpu.sum.usage.total.percent')

print("Docker hosts found: " + str(len(docker_hosts)))

for docker_host_series in docker_hosts:
    print("--------------")

    if len(docker_host_series.tags) > 0:
        print("- SKIP series with tags (do not delete): " + docker_host_series.entity + " : " + str(elapsed_minutes) + " : " + str(docker_host_series.tags))
        continue

    # get minutes since last insert
    elapsed_minutes = docker_host_series.get_elapsed_minutes()

    # keep entities that have recent data (inserted within the last 7 days)
    if elapsed_minutes < 7*24*60:
        print("- RETAIN (do not delete): " + docker_host_series.entity + " : " + str(elapsed_minutes))
        continue

    entity_filter = "lower(tags.docker-host) = lower('" + docker_host_series.entity + "')"
    # find related entities, which tag value equals docker host
    entities = entity_service.list(expression=entity_filter, limit=0, tags="*")

    print("- DELETE " + str(len(entities)) + " objects for docker_host= " + docker_host_series.entity +
          " : " + docker_host_series.last_insert_date.isoformat() + " : elapsed_minutes= " + str(elapsed_minutes))

    for entity in entities:

        if entity.name == docker_host_series.entity:
            # ignore the docker host itself, host is deleted later
            continue

        #print(" - Deleting " + entity.tags.get('docker-type', '') + " : " + entity.name + " : " + entity.tags.get('name', ''))
        #tags_printer.pprint(entity.tags)
        # Uncomment next line to delete
        # entity_service.delete(entity)

    print("- DELETE docker host: " + docker_host_series.entity)
    # Uncomment next line to delete
    # entity_service.delete(docker_host_series.entity)
