import os


EB_HISTORY_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'eb_history.json')
ECS_HISTORY_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ecs_history.json')
DOCKER_HISTORY_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docker_history.json')

ROOT_DIRECTORY = '/Users/Stephen/Scripts'
REMOTE_SOURCE_EXT = '-remote'

DOCKER_USER = 'stephenneal'
DOCKER_REPO_TAG = 'latest'

HOST_PORT = 5000
CONTAINER_PORT = 5000

AWS_REGION = 'us-east-1'
LAUNCH_TYPES = ('EC2', 'FARGATE')
