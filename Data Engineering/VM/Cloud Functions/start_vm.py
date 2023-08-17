import functions_framework
import logging
from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import json

@functions_framework.http
def start_vm(request):
    
    name = request.args.get('name', 'World')
    
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    
    # Project ID for this request.
    project = 'terra-safe-391718' # here you project ID name
    
    # The name of the zone for this request.
    zone = 'us-central1-c' # put here your zone
    
    # Name of the instance resource to start.
    instance = 'terrasafe' # put here the name of the vm to start
    req = service.instances().start(project=project, zone=zone, instance=instance)
    
    pprint(credentials)
    pprint(service)
    pprint(project)
    pprint(zone)
    pprint(instance)

    # Registrar los resultados en los registros de la función
    logging.info('Credentials: %s', credentials)
    logging.info('Service: %s', service)
    logging.info('Project: %s', project)
    logging.info('Zone: %s', zone)
    logging.info('Instance: %s', instance)
     
    response = req.execute()
    pprint(response)

    # Construir la respuesta JSON
    message = {'message': f'Start VM Ok!'}

    # Devolver la respuesta como JSON
    return json.dumps(message), 200, {'Content-Type': 'application/json'}

