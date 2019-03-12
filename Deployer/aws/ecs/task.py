import os
from Deployer.utils import TaskTracker
from Deployer.aws.config import LAUNCH_TYPES


class Task(TaskTracker):
    def __init__(self, cluster=None, task=None):
        """
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster on which to run your task.
        :param task: The family and revision (family:revision ) or full ARN of the task definition to run.
        """
        self.cluster = cluster
        self.task = task

    def register(self, json_path):
        """
        Register a task definition in a AWS ECS cluster.

        :param json_path: Path to task definition JSON
        """
        assert json_path.endswith('.json')
        print('Registering task definition')
        os.system('aws ecs register-task-definition --clie-input-json file:://{0}'.format(json_path))
        self.add_task('Registered task definition')

    def run(self, launch_type='EC2'):
        """
        Run a defined Task in a EC2 cluster

        :param launch_type: The launch type on which to run your task.
        """
        assert launch_type in LAUNCH_TYPES
        self._assert_cluster()
        self._assert_task()
        os.system('aws ecs run-task --cluster {0} --task-definition {1}'.format(self.cluster, self.task))
        self.add_task('Running task {0} in EC2 cluster {1}'.format(self.task, self.cluster))

    def stop(self, reason=None):
        """
        Stop a running Task in a EC2 cluster.

        :param reason: An optional message specified when a task is stopped
        """
        self._assert_cluster()
        self._assert_task()
        cmd = 'aws ecs stop-task --cluster {0} --task {1}'.format(self.cluster, self.task)
        msg = 'Stopped task {0} in cluster {1}'.format(self.task, self.cluster)
        if reason:
            msg += ' because {0}'.format(reason)
            cmd += ' --reason {0}'.format(reason)
        os.system(cmd)

    def _assert_cluster(self):
        """Confirm that a cluster value has been set."""
        assert self.cluster, 'An EC2 cluster (short name or full Amazon Resource Name) must be specified'

    def _assert_task(self):
        """Confirm that a cluster value has been set."""
        assert self.task, 'An Task ID or full ARN must be specified'
