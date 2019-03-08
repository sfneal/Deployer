import os
from datetime import datetime
from ruamel.yaml import YAML
from databasetools import JSON
from Deployer.aws.config import ROOT_DIRECTORY, DOCKER_USER, JSON_PATH
from Deployer.aws.gui import gui


class ElasticBeanstalk:
    def __init__(self, source, app, env, version, root=ROOT_DIRECTORY, docker_user=DOCKER_USER, edit_eb_config=False):
        """
        AWS Elastic Beanstalk deployment helper.

        :param source: Local directory containing source code
        :param app: AWS application name/GitHub repo name
        :param env: AWS environment name/GitHub branch name
        :param version: AWS version/GitHub release
        :param edit_eb_config: Allow manual editing of the Elastic Beanstalk config
        """
        self.source = os.path.join(root, source)
        self.app = app
        self.env = env
        self.version = version
        self.docker_user = docker_user
        self.edit_eb_config = edit_eb_config
        self._tasks = []

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

        # Initialize docker
        os.chdir(source)
        os.system('eb init --region us-east-1 -p docker {0}'.format(self.app))
        self.add_task("Initialized '{0}' as an EB application".format(source.rsplit(os.sep, 1)[-1]))

        # Edit default region value in config.yaml
        self.set_region(source)

    def build(self):
        """Build a docker image for distribution to DockerHub."""
        cmd = 'docker build -t {0}'.format('{tag} {source}'.format(tag=self.docker_tag, source=self.source))
        os.system(cmd)
        self.add_task('Built Docker image {0}'.format(self.docker_tag))

    def push(self):
        """Push a docker image to a DockerHub repo."""
        cmd = 'docker push {0}'.format(self.docker_tag)
        os.system(cmd)
        self.add_task('Pushed Docker image {0} to DockerHub repo'.format(self.docker_tag))

    def distribute(self):
        """Deploy a docker image from a DockerHub repo to a AWS elastic beanstalk environment instance."""
        # Path to Dockerrun file
        docker_run_json = os.path.join(self.source + '-remote', 'Dockerrun.aws.json')

        # Check to see if the Dockerrun already exists
        if not os.path.exists(docker_run_json):
            print('Creating Elastic Beanstalk environment')
            self.eb_create(docker_run_json)
        else:
            print('Deploying Elastic Beanstalk environment')
            self.eb_deploy()
        self.update_history()
        os.system('eb open')

    def eb_create(self, docker_run_json):
        """
        Use awsebcli command `$ eb create` to create a new Elastic Beanstalk environment.

        :param docker_run_json: Path to Dockerrun.aws.json file
        """
        # Create directory with '-remote' extension next to source
        if not os.path.exists(self.source + '-remote'):
            os.mkdir(self.source + '-remote')
            self.add_task(
                "Created directory '{0}' for storing Dockerrun file".format(os.path.dirname(docker_run_json)))

        # Create a Dockerrun.aws.json file in -remote directory
        JSON(os.path.join(self.source + '-remote', 'Dockerrun.aws.json')).write(
            {"AWSEBDockerrunVersion": "1",
             "Image": {
                 "Name": "{user}/{app}".format(user=self.docker_user, app=self.env),
                 "Update": "true"},
             "Ports": [{"ContainerPort": "5000"}]},
            sort_keys=False, indent=2)
        self.add_task('Make Dockerrun.aws.json file with default deployment config')

        # Initialize application in -remote directory
        self.initialize(self.source + '-remote')

        # Create Elastic Beanstalk environment in current application
        os.chdir(self.source + '-remote')
        os.system('eb create {env}'.format(env=self.env))
        self.add_task('Created Elastic Beanstalk environment {0}'.format(self.env))

    def eb_deploy(self):
        """Use awsebcli command '$eb deploy' to deploy an updated Elastic Beanstalk environment."""
        os.system('eb deploy {env} --label {version}'.format(env=self.env, version=self.version))
        self.add_task('Deployed Elastic Beanstalk environment {0}'.format(self.env))

    def set_region(self, source, region='us-east-1'):
        """
        Change the default AWS region.

        Editing the config.yml file in the .elasticbeanstalk directory to
        ensure correct region is used.

        :param source: Code base root directory
        :param region: Default AWS region to use
        """
        # Only edit config.yml if edit_eb_config is enabled.
        # Check to see if we are initializing the '-remote' directory
        # because .elasticbeanstalk directory does not need to be
        # edited in deployment directories.
        if self.edit_eb_config and not source.endswith('-remote'):
            # Open Elastic Beanstalk configuration file
            yaml = YAML()
            yaml_config = os.path.join(source, '.elasticbeanstalk', 'config.yml')
            with open(yaml_config, 'r') as yaml_file:
                eb_config = yaml.load(yaml_file)

            # Ensure that default region is set to us-east-1
            if eb_config['global']['default_region'] is not region:
                eb_config['global']['default_region'] = region

                # Dump updated config to config.yml
                with open(yaml_config, 'w') as yaml_file:
                    yaml.dump(eb_config, yaml_file)
                self.add_task('Set application region to {0}'.format(region))

    def update_history(self):
        """Store deployment parameters in history.json."""
        json = JSON(JSON_PATH)
        history_json = json.read()
        history_json['history'].append({'application-name': self.app,
                                        'environment-name': self.env,
                                        'version': self.version,
                                        'source': self.source,
                                        'time': datetime.now().strftime("%Y-%m-%d %H:%M"),
                                        'tasks': self.tasks})
        json.write(history_json)

    @property
    def docker_tag(self):
        """Concatenate DockerHub user name and environment name to create docker image tag."""
        return '{user}/{env}:latest'.format(user=self.docker_user, env=self.env)

    @property
    def tasks(self):
        """Create a numbered list of completed steps."""
        return ['{0}: {1}'.format(i, step) for i, step in enumerate(self._tasks)]

    def add_task(self, task):
        """Add a complete task to the tasks list."""
        self.add_task(task)

    def show_tasks(self):
        """Print a list of all the tasks completed."""
        print('\nCompleted to following tasks:')
        for step in self.tasks:
            print('\t{0}'.format(step))


def main():
    params = gui()
    eb = ElasticBeanstalk(source=params['source'],
                          app=params['application-name'],
                          env=params['environment-name'],
                          version=params['version'],
                          root=params['root'],
                          docker_user=params['docker_user'])
    eb.deploy()
    eb.show_tasks()


if __name__ == '__main__':
    main()
