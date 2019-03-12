"""
 _____ _           _   _      ____                       _        _ _
| ____| | __ _ ___| |_(_) ___| __ )  ___  __ _ _ __  ___| |_ __ _| | | __
|  _| | |/ _` / __| __| |/ __|  _ \ / _ \/ _` | '_ \/ __| __/ _` | | |/ /
| |___| | (_| \__ \ |_| | (__| |_) |  __/ (_| | | | \__ \ || (_| | |   <
|_____|_|\__,_|___/\__|_|\___|____/ \___|\__,_|_| |_|___/\__\__,_|_|_|\_\

"""
import os
from ruamel.yaml import YAML
from datetime import datetime
from databasetools import JSON

from Deployer import Docker, TaskTracker
from Deployer.aws.config import DOCKER_USER, JSON_PATH, DOCKER_REPO_TAG, AWS_REGION, REMOTE_SOURCE_EXT
from Deployer.aws.eb.gui import gui


# Required ElasticBeanstalk parameters that do not have a default value
REQUIRED = ('source', 'aws_application_name', 'aws_environment_name', 'aws_version')


class Dockerrun(TaskTracker):
    def __init__(self, source, aws_environment_name, docker_user, remote_source_ext=REMOTE_SOURCE_EXT):
        """

        :param aws_environment_name:
        :param docker_user:
        :param remote_source_ext: Extension given to the directory containing a Dockerrun file
        """
        self.source = source
        self.docker_user = docker_user
        self.aws_environment_name = aws_environment_name

        self._remote_source_ext = remote_source_ext

    @property
    def remote_source(self):
        """Path to source directory with '-remote' extension."""
        return self.source + self._remote_source_ext

    @property
    def path(self):
        """Path to Dockerrun file."""
        return os.path.join(self.remote_source, 'Dockerrun.aws.json')

    @property
    def data(self):
        """Default values for a Dockerrun.aws.json file."""
        return {"AWSEBDockerrunVersion": "1",
                "Image": {
                    "Name": "{user}/{app}".format(user=self.docker_user, app=self.aws_environment_name),
                    "Update": "true"},
                "Ports": [{"ContainerPort": "5000"}]}

    def create(self):
        """Create a Dockerrun.aws.json file in the default directory with default data."""
        JSON(os.path.join(self.path)).write(self.data, sort_keys=False, indent=2)
        self.add_task('Make Dockerrun.aws.json file with default deployment config')


class ElasticBeanstalk(TaskTracker):
    def __init__(self, source=None,
                 aws_application_name=None,
                 aws_environment_name=None,
                 aws_version=None,
                 aws_instance_key=None,
                 aws_region=AWS_REGION,
                 docker_user=DOCKER_USER,
                 docker_repo=None,
                 docker_repo_tag=DOCKER_REPO_TAG,
                 edit_eb_config=False,
                 json_path=JSON_PATH):
        """
        AWS Elastic Beanstalk deployment helper.

        :param source: Local directory containing source code
        :param aws_application_name: AWS application name/GitHub repo name
        :param aws_environment_name: AWS environment name/GitHub branch name
        :param aws_version: AWS version/GitHub release
        :param docker_user: DockerHub username
        :param docker_repo: DockerHub repository name
        :param docker_repo_tag: DockerHub repository tag
        :param edit_eb_config: config.yml editing enabled flag
        :param json_path: Path to history.json deployment history file
        """
        # Directory settings
        self.source = source

        # AWS settings
        self.aws_application_name = aws_application_name
        self.aws_environment_name = aws_environment_name
        self.aws_version = aws_version
        self.aws_instance_key = aws_instance_key if aws_instance_key else aws_environment_name
        self.aws_region = aws_region

        # Docker settings
        self.docker_user = docker_user
        self.docker_repo = docker_repo if docker_repo else aws_environment_name
        self.docker_repo_tag = docker_repo_tag
        self.edit_eb_config = edit_eb_config
        self.json_path = json_path

        # Initialize Docker
        self.Docker = Docker(self.source, self.docker_repo, self.docker_repo_tag, self.docker_user)

        # Initialize Dockerrun
        self.Dockerrun = Dockerrun(self.source, self.aws_environment_name, self.docker_user)

        self._tasks = []

        # Launch GUI form if all required parameters are NOT set
        if any(getattr(self, p) is None for p in REQUIRED):
            self.gui()

    @property
    def parameters(self):
        """Return dictionary of deployment parameters for dumping to history.json."""
        return {'aws_application-name': self.aws_application_name,
                'aws_environment-name': self.aws_environment_name,
                'aws_version': self.aws_version,
                'aws_instance-key': self.aws_instance_key,
                'docker_user': self.docker_user,
                'docker_repo': self.docker_repo,
                'docker_repo_tag': self.docker_repo_tag,
                'source': self.source,
                'time': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'tasks': self.tasks}

    def initialize(self, source=None):
        """Initialize the docker application if it hasn't been previously initialized."""
        # Path to .elasticbeanstalk directory
        source = self.source if not source else source

        # Initialize docker
        os.chdir(source)
        os.system('eb init --region {0} --keyname {1} -p docker {1}'.format(self.aws_region, self.aws_instance_key,
                                                                            self.aws_application_name))
        self.add_task("Initialized '{0}' as an EB application".format(source.rsplit(os.sep, 1)[-1]))

        # Edit default region value in config.yaml
        self.set_region(source)

    def deploy(self):
        """Deploy a docker image from a DockerHub repo to a AWS elastic beanstalk environment instance."""
        # Check to see if the Dockerrun already exists
        if not os.path.exists(self.Dockerrun.path):
            print('Creating Elastic Beanstalk environment')
            self._create()
        else:
            print('Deploying Elastic Beanstalk environment')
            self._deploy()

        # Dump deployment data/results to JSON
        self.update_history(self.json_path, self.parameters)

        # Open Elastic Beanstalk in a browser
        os.system('eb open')

    def _create(self):
        """Use awsebcli command `$ eb create` to create a new Elastic Beanstalk environment."""
        # Create directory with '-remote' extension next to source
        if not os.path.exists(self.Dockerrun.remote_source):
            os.mkdir(self.Dockerrun.remote_source)
            self.add_task(
                "Created directory '{0}' for storing Dockerrun file".format(self.Dockerrun.remote_source))

        # Create a Dockerrun.aws.json file in -remote directory
        self.Dockerrun.create()

        # Initialize application in -remote directory
        self.initialize(self.Dockerrun.remote_source)

        # Create Elastic Beanstalk environment in current application
        os.chdir(self.source)
        os.system('eb create {env} --keyname {key}'.format(env=self.aws_environment_name, key=self.aws_instance_key))
        self.add_task('Created Elastic Beanstalk environment {0}'.format(self.aws_environment_name))

    def _deploy(self):
        """Use awsebcli command '$eb deploy' to deploy an updated Elastic Beanstalk environment."""
        os.chdir(self.Dockerrun.remote_source)
        os.system('eb deploy {env} --label {version}'.format(env=self.aws_environment_name, version=self.aws_version))
        self.add_task('Deployed Elastic Beanstalk environment {0}'.format(self.aws_environment_name))

    def set_region(self, source):
        """
        Change the default AWS region.

        Editing the config.yml file in the .elasticbeanstalk directory to
        ensure correct region is used.

        :param source: Code base root directory
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
            if eb_config['global']['default_region'] is not self.aws_region:
                eb_config['global']['default_region'] = self.aws_region

                # Dump updated config to config.yml
                with open(yaml_config, 'w') as yaml_file:
                    yaml.dump(eb_config, yaml_file)
                self.add_task('Set application region to {0}'.format(self.aws_region))

    def gui(self):
        """PySimpleGUI form for setting ElasticBeanstalk deployment parameters."""
        params = gui(aws_application_name=self.aws_application_name, aws_environment_name=self.aws_environment_name,
                     aws_version=self.aws_version, aws_instance_key=self.aws_instance_key,
                     docker_user=self.docker_user,  docker_repo=self.docker_repo, docker_tag=self.docker_repo_tag)
        self.aws_application_name = params['aws_application_name']
        self.aws_environment_name = params['aws_environment_name']
        self.aws_version = params['aws_version']
        self.aws_instance_key = params['aws_instance_key']
        self.docker_user = params['docker_user']
        self.docker_repo = params['docker_repo']
        self.docker_repo_tag = params['docker_repo_tag']
