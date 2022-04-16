import logging
import json
import os
from random import randint
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = 'test-pi'
THING_NAME = 'test-pi'
HOST = os.getenv('HOST')
PORT = 8883
# Hardcode these for now
ROOT_CA_PATH = '/home/pi/certs/Amazon-root-CA-1.pem'
PRIVATE_KEY_PATH = '/home/pi/certs/private.pem.key'
CERT_PATH = '/home/pi/certs/certificate.pem.cert'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Function called when a shadow is updated
def customShadowCallback_Update(payload, response_status, token):
    """Display status and data from update request"""
    if response_status == 'timeout':
        print(f'Update request {token} timeout!')
        print("Update request " + token + " time out!")

    if response_status == 'accepted':
        payload_dict = json.loads(payload)
        print('~~~~~~~~~~~~~~~~~~~~~~~')
        print(f'Update request with token: {token} accepted!')
        print('num: ' + str(payload_dict['state']['reported']['num']))
        print('~~~~~~~~~~~~~~~~~~~~~~~\n\n')

    if response_status == 'rejected':
        print(f'Update request {token} rejected!')

# Function called when a shadow is deleted
def customShadowCallback_Delete(payload, responseStatus, token):
    """Display status and data from delete request"""
    if responseStatus == "timeout":
        print(f'Delete request {token} time out!')

    if responseStatus == 'accepted':
        print('~~~~~~~~~~~~~~~~~~~~~~~')
        print(f'Delete request with token: {token} accepted!')
        print('~~~~~~~~~~~~~~~~~~~~~~~\n\n')

    if responseStatus == 'rejected':
        print(f'Delete request {token} rejected!')

def init_mqtt_shadow_client(client_id, host, port,
    root_ca_path, private_key_path, cert_path):
    # Init AWSIoTMQTTShadowClient
    mqtt_shadow_client = None
    mqtt_shadow_client = AWSIoTMQTTShadowClient(client_id)
    mqtt_shadow_client.configureEndpoint(host, port)
    mqtt_shadow_client.configureCredentials(root_ca_path, private_key_path, cert_path)

    # Configure connection
    mqtt_shadow_client.configureAutoReconnectBackoffTime(1, 32, 20)
    mqtt_shadow_client.configureConnectDisconnectTimeout(10)
    mqtt_shadow_client.configureMQTTOperationTimeout(5)

    # Connect to AWS IoT
    mqtt_shadow_client.connect()

    return mqtt_shadow_client

def create_shadow_handler(mqtt_shadow_client, thing_name):
    # Create a device shadow handler, use this to update and delete shadow document
    shadow_handler = mqtt_shadow_client.createShadowHandlerWithName(
        thing_name, True)
    # Delete current shadow JSON doc
    shadow_handler.shadowDelete(customShadowCallback_Delete, 5)
    return shadow_handler

if __name__ == '__main__':
    logger.info('initializing mqtt shadow client...')
    shadow_client = init_mqtt_shadow_client(
        CLIENT_ID, HOST, PORT, ROOT_CA_PATH, PRIVATE_KEY_PATH, CERT_PATH
    )
    logger.info('initializing shadow handler...')
    shadow_handler = create_shadow_handler(shadow_client, 'test-pi')

    while True:
        rand_int = randint(1, 100)

        # Display readings:
        logger.info(f'num: {rand_int}')
        
        # Create message payload
        payload = {
            'state': {
                'reported': {
                    'num': rand_int
                }
            }
        }
        # Update shadow
        shadow_handler.shadowUpdate(json.dumps(payload), customShadowCallback_Update, 5)
        time.sleep(5)
