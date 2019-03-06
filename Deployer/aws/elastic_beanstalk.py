import os
from ruamel.yaml import YAML
from databasetools import JSON


ROOT_DIRECTORY = '/Users/Stephen/Scripts'
DOCKER_USER = 'stephenneal'


class ElasticBeanstalk:
    def __init__(self, source, app, env, version, root=ROOT_DIRECTORY, docker_user=DOCKER_USER):
        """
        AWS Elastic Beanstalk deployment helper.

        :param source: Local directory containing source code
        :param app: AWS application name/GitHub repo name
        :param env: AWS environment name/GitHub branch name
        :param version: AWS version/GitHub release
        """
        self.source = os.path.join(root, source)
        self.app = app
        self.env = env
        self.version = version
        self.docker_user = docker_user
        self._steps = []

    @property
    def docker_tag(self):
        """Concatenate DockerHub user name and environment name to create docker image tag."""
        return '{user}/{env}:latest'.format(user=self.docker_user, env=self.env)

    def steps(self):
        """Print a list of all the _steps taken."""
        for i, step in enumerate(self._steps):
            print('{0}: {1}'.format(i, step))

    def deploy(self):
        """Deploy a Docker image application to an AWS Elastic Beanstalk environment."""
        # Ensure directory has been initialized as an Elastic Beanstalk app and that config is correct
        self.initialize()

        # Build and push Docker image to DockerHub
        self.build()
        self.push()

        # Deploy application by creating or updating an environment
        self.distribute()

    def initialize(self, source=None):
        """Initialize the docker application if it hasn't been previously initialized."""
        # Path to .elasticbeanstalk directory
        source = self.source if not source else source
        path = os.path.join(source, '.elasticbeanstalk')

        # Check to see if the elasticbeanstalk directory was already created
        if not os.path.exists(path):
            os.chdir(self.source)
            os.system('eb init -p docker {0}'.format(self.app))
            self._steps.append("Initialized '{0}' as an EB application".format(source.rsplit(os.sep, 1)[0]))

        # Check to see if we are initializing the '-remote' directory
        if not source.endswith('-remote'):
            # Open Elastic Beanstalk configuration file
            yaml = YAML()
            with open(os.path.join(path, 'config.yml'), 'r') as yaml_file:
                eb_config = yaml.load(yaml_file)

            # Ensure that default region is set to us-east-1
            if eb_config['global']['default_region'] is not 'us-east-1':
                eb_config['global']['default_region'] = 'us-east-1'

                # Dump updated config to config.yml
                with open(os.path.join(path, 'config.yml'), 'w') as yaml_file:
                    yaml.dump(eb_config, yaml_file)
                self._steps.append('Set application region to us-east-1')

    def build(self):
        """Build a docker image for distribution to DockerHub."""
        cmd = 'docker build -t {0}'.format(
            '{tag} {source}'.format(tag=self.docker_tag, source=self.source)
        )
        os.system(cmd)
        self._steps.append('Built Docker image {0}'.format(self.docker_tag))

    def push(self):
        """Push a docker image to a DockerHub repo."""
        cmd = 'docker push {user}/{env}:latest'.format(user=self.docker_user, env=self.env)
        os.system(cmd)
        self._steps.append('Pushed Docker image {0} to DockerHub repo'.format(self.docker_tag))

    def distribute(self):
        """Deploy a docker image from a DockerHub repo to a AWS elastic beanstalk environment instance."""
        # Path to Dockerrun file
        path = os.path.join(self.source + '-remote', 'Dockerrun.aws.json')

        # Check to see if the Dockerrun already exists
        if not os.path.exists(path):
            # Create directory with '-remote' extension next to source
            if not os.path.exists(self.source + '-remote'):
                os.mkdir(self.source + '-remote')
                self._steps.append("Created directory '{0}' for storing Dockerrun file".format(os.path.dirname(path)))

            # Create a Dockerrun.aws.json file in -remote directory
            JSON(os.path.join(self.source + '-remote', 'Dockerrun.aws.json')).write(
                {"AWSEBDockerrunVersion": "1",
                 "Image": {
                     "Name": "{user}/{app}".format(user=self.docker_user, app=self.app),
                     "Update": "true"},
                 "Ports": [{"ContainerPort": "5000"}]},
                sort_keys=False, indent=2)
            self._steps.append('Make Dockerrun.aws.json file with default deplpyment config')

            # Initialize application in -remote directory
            self.initialize(self.source + '-remote')

            # Create Elastic Beanstalk environment in current application
            os.system('eb create {env}'.format(env=self.env))
            self._steps.append('Created Elastic Beanstalk environment {0}'.format(self.env))
        else:
            os.system('eb deploy {env} --label {version}'.format(env=self.env, version=self.version))
            self._steps.append('Deployed Elastic Beanstalk environment {0}'.format(self.env))
        os.system('eb open')


def main():
    eb = ElasticBeanstalk(source='_practice/flask-docker-tutorial/flask-basic5',
                          app='flask-docker-tutorials',
                          env='flask-basic5',
                          version='v1.0')
    eb.deploy()
    eb.steps()


if __name__ == '__main__':
    main()
