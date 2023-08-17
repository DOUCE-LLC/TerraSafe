import functions_framework
from google.cloud import pubsub_v1
import requests
import json

@functions_framework.http
def pubsub_delta(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    # Processing GET HTTPS message   
    request_json = request.get_json(silent=True)
    request_args = request.args

    # Global variables
    project_id = "terra-safe-391718"
    topic_id = "start_delta"
    
    
    #Getting a Pub/Sub client and topic path
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Publishing the Pub/Sub message
    publisher.publish(topic_path, b"Start Delta message")
    
    # Construir la respuesta JSON
    message = {'message': f'Delta started'}

    # Devolver la respuesta como JSON
    return json.dumps(message), 200, {'Content-Type': 'application/json'}
