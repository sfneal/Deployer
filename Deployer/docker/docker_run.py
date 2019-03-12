import os
from databasetools import JSON
from Deployer.utils import TaskTracker
from Deployer.aws.config import REMOTE_SOURCE_EXT


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
