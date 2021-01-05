from atsd_client import connect, connect_url
from atsd_client.services import MetricsService

'''
Delete metrics based on name and last insert date
'''

# Connect to ATSD server
#connection = connect('/path/to/connection.properties')
connection = connect_url('https://atsd_hostname:8443', 'username', 'password')

# Initialize services
metric_service = MetricsService(connection)

# Search metrics
expression = "name LIKE 'abc.*' OR name LIKE 'cde.*' OR name LIKE '*xyz*'"
metrics = metric_service.list(expression = expression, min_insert_date="2020-07-06T00:00:00.000Z", max_insert_date="2020-07-07T00:00:00.000Z")

print("- DELETE " + str(len(metrics)) + " metrics")

for metric in metrics:
    print(metric.name)
    #metric_service.delete(metric.name)
