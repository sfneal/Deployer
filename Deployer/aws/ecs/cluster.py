from subprocess import Popen, PIPE
from Deployer.utils import TaskTracker


class Cluster(TaskTracker):
    def __init__(self, name):
        self.name = name

    def arn(self):
        """Describes one of your clusters."""
        r = Popen('aws ecs describe-clusters --clusters {0}'.format(self.name), shell=True, stdout=PIPE)
        for i in r.stdout:
            return str(i.decode("utf-8")).strip().split('\t')[2]
