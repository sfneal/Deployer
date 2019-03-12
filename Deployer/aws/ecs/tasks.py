import os
from Deployer.utils import TaskTracker
from Deployer.aws.config import LAUNCH_TYPES


class Tasks(TaskTracker):
    def __init__(self, cluster=None):
        """
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster on which to run your task.
        """
        self.cluster = cluster

    def register(self, json_path):
        """
        Register a task definition in a AWS ECS cluster.

        :param json_path: Path to task definition JSON
        """
        assert json_path.endswith('.json')
        print('Registering task definition')
        os.system('aws ecs register-task-definition --clie-input-json file:://{0}'.format(json_path))
        self.add_task('Registered task definition')

    def run(self, task_definition, launch_type='EC2'):
        """
        Run a defined Task in a EC2 cluster

        :param task_definition: The family and revision (family:revision ) or full ARN of the task definition to run.
        :param launch_type: The launch type on which to run your task.
        :return:
        """
        assert launch_type in LAUNCH_TYPES
        assert self.cluster, 'An EC2 cluster (short name or full Amazon Resource Name) must be specified'
        os.system('aws ecs run-task --cluster {0} --task-definition {1}'.format(self.cluster, task_definition))
        self.add_task('Running task {0} in EC2 cluster {1}'.format(task_definition, self.cluster))
