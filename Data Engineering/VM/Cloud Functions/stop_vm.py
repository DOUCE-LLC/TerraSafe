import json
import functions_framework
import logging
from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import json

@functions_framework.http
def stop_vm(request):
    
    #Processing GET parameters
    name = request.args.get('name', 'stop_VM')
    pprint(name)
    
    #Getting credentials and service
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    
    # Project ID for this request.
    project = 'terra-safe-391718' # here you project ID name
    
    # The name of the zone for this request.
    zone = 'us-central1-c' # put here your zone
    
    # Name of the instance resource to start.
    instance = 'terrasafe' # put here the name of the vm to start
    req = service.instances().stop(project=project, zone=zone, instance=instance)
    
    pprint(credentials)
    pprint(service)
    pprint(project)
    pprint(zone)
    pprint(instance)

    # Execute command
    response = req.execute()
    pprint(response)

    # Return operation status
    return json.dumps(response), 200, {'Content-Type': 'application/json'}
