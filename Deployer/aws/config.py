import os


_HISTORY_JSON_ROOT = os.path.join(os.path.expanduser('~'), '.Deployer')
if not os.path.exists(_HISTORY_JSON_ROOT):
    os.mkdir(_HISTORY_JSON_ROOT)

EB_HISTORY_JSON = os.path.join(_HISTORY_JSON_ROOT, 'eb_history.json')
ECS_HISTORY_JSON = os.path.join(_HISTORY_JSON_ROOT, 'ecs_history.json')
DOCKER_HISTORY_JSON = os.path.join(_HISTORY_JSON_ROOT, 'docker_history.json')

ROOT_DIRECTORY = '/Users/Stephen/Scripts'
REMOTE_SOURCE_EXT = '-remote'

DOCKER_USER = 'stephenneal'
DOCKER_REPO_TAG = 'latest'

HOST_PORT = 5000
CONTAINER_PORT = 5000

AWS_REGION = 'us-east-1'
LAUNCH_TYPES = ('EC2', 'FARGATE')
