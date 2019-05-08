"""
 _____ _           _   _      ____                       _        _ _
| ____| | __ _ ___| |_(_) ___| __ )  ___  __ _ _ __  ___| |_ __ _| | | __
|  _| | |/ _` / __| __| |/ __|  _ \ / _ \/ _` | '_ \/ __| __/ _` | | |/ /
| |___| | (_| \__ \ |_| | (__| |_) |  __/ (_| | | | \__ \ || (_| | |   <
|_____|_|\__,_|___/\__|_|\___|____/ \___|\__,_|_| |_|___/\__\__,_|_|_|\_\

"""
import os
from subprocess import Popen, PIPE
from ruamel.yaml import YAML

from Deployer.utils import TaskTracker
from Deployer.docker.docker import Docker
from Deployer.docker.run import Dockerrun
from Deployer.aws.config import EB_HISTORY_JSON, AWS_REGION, HOST_PORT, CONTAINER_PORT, AWS_VERSION_DESCRIPTION


# Required ElasticBeanstalk parameters that do not have a default value
REQUIRED = ('source', 'aws_application_name', 'aws_environment_name', 'aws_version')


class ElasticBeanstalk(TaskTracker):
    def __init__(self, source=None,
                 aws_application_name=None,
                 aws_environment_name=None,
                 aws_version=None,
                 aws_instance_key=None,
                 aws_region=AWS_REGION,
                 aws_version_description=AWS_VERSION_DESCRIPTION,
                 docker_user=None,
                 docker_repo=None,
                 docker_repo_tag=None,
                 host_port=HOST_PORT,
                 container_port=CONTAINER_PORT,
                 dockerfile='Dockerfile',
                 edit_eb_config=False,
                 json_path=EB_HISTORY_JSON):
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
        self.aws_version_description = aws_version_description

        # Docker settings
        self.docker_user = docker_user
        self.docker_repo = docker_repo if docker_repo else aws_environment_name
        self.docker_repo_tag = docker_repo_tag
        self.host_port = host_port
        self.container_port = container_port
        self.dockerfile = dockerfile
        self.edit_eb_config = edit_eb_config
        self.json_path = json_path

        # Initialize Docker
        self.Docker = Docker(self.source, self.docker_repo, self.docker_repo_tag, self.docker_user, self.host_port,
                             self.container_port, self.dockerfile)

        # Initialize Dockerrun
        self.Dockerrun = Dockerrun(self.source, self.docker_repo, self.docker_user, self.container_port,
                                   self.docker_repo_tag)

    @property
    def parameters(self):
        """Return dictionary of deployment parameters for dumping to history.json."""
        return {'aws_application-name': self.aws_application_name,
                'aws_environment-name': self.aws_environment_name,
                'aws_version': self.aws_version,
                'aws_instance-key': self.aws_instance_key,
                'aws_version-description': self.aws_version_description,
                'docker_user': self.docker_user,
                'docker_repo': self.docker_repo,
                'docker_repo_tag': self.docker_repo_tag,
                'container_port': self.container_port,
                'host_port': self.host_port,
                'source': self.source}

    def initialize(self, source=None):
        """Initialize the docker application if it hasn't been previously initialized."""
        # Path to .elasticbeanstalk directory
        source = self.source if not source else source

        # Initialize docker
        os.chdir(source)
        os.system('eb init --region {0} --keyname {1} -p docker {2}'.format(self.aws_region, self.aws_instance_key,
                                                                            self.docker_repo))
        self.add_task("Initialized '{0}' as an EB application".format(self.aws_application_name))

        # Edit default region value in config.yaml
        self.set_region(source)

    def deploy(self):
        """Deploy a docker image from a DockerHub repo to a AWS elastic beanstalk environment instance."""
        # Check to see if AWS EB Environment already exists or if it is 'Terminated'
        try:
            environments = self.environments.get(self.aws_environment_name).get('status', None) == 'Terminated'
        except AttributeError:
            environments = True
        if any(condition for condition in (self.aws_environment_name not in self.environments, environments)):
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
        os.chdir(self.Dockerrun.remote_source)
        cmd = 'eb create {env} --keyname {key}'.format(env=self.aws_environment_name, key=self.aws_instance_key)
        os.system(cmd)
        self.Dockerrun.destroy()
        self.add_task('Created Elastic Beanstalk environment {0}'.format(self.aws_environment_name))

    def _deploy(self):
        """Use awsebcli command '$eb deploy' to deploy an updated Elastic Beanstalk environment."""
        # Update a Dockerrun.aws.json file in -remote directory
        self.Dockerrun.create()

        # Initialize application in -remote directory
        self.initialize(self.Dockerrun.remote_source)

        os.chdir(self.Dockerrun.remote_source)
        os.system('eb deploy {env} --label {version} --message "{message}"'.format(env=self.aws_environment_name,
                                                                                   version=self.aws_version,
                                                                                   message=self.aws_version_description))
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

    @property
    def environments(self):
        """Retrieve a list of environments in the current EB application."""
        cmd = 'aws elasticbeanstalk describe-environments --application-name {0}'.format(self.aws_application_name)
        data = [i.decode("utf-8").strip().split('\t') for i in Popen(cmd, shell=True, stdout=PIPE).stdout]
        return {d[3].split('.', 1)[0]: {'running_version': d[-1], 'status': d[-2]}
                for d in data if d[0].lower() == 'environments'}
