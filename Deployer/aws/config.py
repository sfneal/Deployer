import os


JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'eb_history.json')

ROOT_DIRECTORY = '/Users/Stephen/Scripts'

DOCKER_USER = 'stephenneal'

DOCKER_REPO_TAG = 'latest'

AWS_REGION = 'us-east-1'

REMOTE_SOURCE_EXT = '-remote'

LAUNCH_TYPES = ('EC2', 'FARGATE')
