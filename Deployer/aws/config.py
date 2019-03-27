import os
from databasetools import JSON


_HISTORY_JSON_ROOT = os.path.join(os.path.expanduser('~'), '.Deployer')

EB_HISTORY_JSON = os.path.join(_HISTORY_JSON_ROOT, 'eb_history.json')
ECS_HISTORY_JSON = os.path.join(_HISTORY_JSON_ROOT, 'ecs_history.json')
DOCKER_HISTORY_JSON = os.path.join(_HISTORY_JSON_ROOT, 'docker_history.json')

# Create '.Deployer' folder in the home directory if it doesn't exist
if not os.path.exists(_HISTORY_JSON_ROOT):
    os.mkdir(_HISTORY_JSON_ROOT)

# Create each history file if they don't exist
for history in (EB_HISTORY_JSON, ECS_HISTORY_JSON, DOCKER_HISTORY_JSON):
    if not os.path.exists(history):
        JSON(history).write({'history': []}, sort_keys=False)

REMOTE_SOURCE_EXT = '-remote'

HOST_PORT = 80
CONTAINER_PORT = 80

AWS_REGION = 'us-east-1'
LAUNCH_TYPES = ('EC2', 'FARGATE')

S3_ACL = ('public-read', 'private', 'public-read-write')
