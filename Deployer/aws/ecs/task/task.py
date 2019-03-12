import os
from tempfile import NamedTemporaryFile
from subprocess import Popen, PIPE
from databasetools import JSON

from Deployer.utils import TaskTracker
from Deployer.aws.config import LAUNCH_TYPES
from Deployer.aws.ecs.cluster import Cluster


class Task(TaskTracker):
    def __init__(self, cluster=None, task_name=None):
        """
        :param cluster: The short name or full Amazon Resource Name (ARN) of the cluster on which to run your task.
        :param task_name: The family and revision (family:revision ) or full ARN of the task definition to run.
        """
        self.cluster = cluster if cluster and cluster.startswith('arn') else Cluster(cluster).arn()
        self.task_name = task_name

    def register(self, docker_container, docker_image, port_protocol, port_host, port_container,
                 volume_name, volume_path, container_path):
        """
        Register a task definition in a AWS ECS cluster.

        :param task: Name of the task
        :param docker_container: Short name to assign to the docker container
        :param docker_image: Docker image name
        :param port_protocol: Port protocol to use
        :param port_host: Host port #
        :param port_container: Container port #
        :param volume_name: Short name you'd like to assign to a volume
        :param volume_path: Path to the volume relative to instance root (not docker)
        :param container_path: Path to map the volume to within the container
        """
        task_def = dict()

        # Container definitions
        task_def['containerDefinitions'] = []
        task_def['containerDefinitions'].append(
            {"memory": 128,
             "portMappings": [
                 {
                     "hostPort": int(port_host),
                     "containerPort": int(port_container),
                     "protocol": port_protocol
                 }
             ],
             "essential": True,
             "mountPoints": [
                 {
                     "containerPath": container_path,
                     "sourceVolume": volume_name
                 }
             ],
             "name": docker_container,
             "image": docker_image})

        # Volumes
        task_def['volumes'] = []
        task_def['volumes'].append(
            {
                "host": {
                    "sourcePath": volume_path
                },
                "name": volume_name
            }
        )

        # Task family name
        task_def['family'] = self.task_name

        with NamedTemporaryFile(suffix=self.task_name + '.json') as temp:
            # Write task definition
            JSON(temp.name).write(task_def, sort_keys=False, indent=2)

            print('Registering task definition')
            cmd = 'aws ecs register-task-definition --cli-input-json file://{0}'.format(temp.name)
            os.system(cmd)
            self.add_task('Registered task definition')

    def run(self, launch_type='EC2'):
        """
        Run a defined Task in a EC2 cluster

        :param launch_type: The launch type on which to run your task.
        """
        assert launch_type in LAUNCH_TYPES
        self._assert_cluster()
        self._assert_task()
        os.system('aws ecs run-task --cluster {0} --task-definition {1}'.format(self.cluster, self.task_name))
        self.add_task('Running task {0} in EC2 cluster {1}'.format(self.task_name, self.cluster))

    def stop(self, reason='Stopped by Deployer.aws.ecs.task.stop()'):
        """
        Stop a running Task in a EC2 cluster.

        :param reason: An optional message specified when a task is stopped
        """
        self._assert_cluster()
        self._assert_task()
        cmd = 'aws ecs stop-task --cluster {0} --task {1}'.format(self.cluster, self.task_id)
        msg = 'Stopped task {0} in cluster {1}'.format(self.task_name, self.cluster)
        if reason and len(reason) > 1:
            msg += ' because {0}'.format(reason)
            cmd += " --reason '{0}'".format(reason)
        os.system(cmd)
        self.add_task(msg)

    @property
    def task_arn(self):
        """Retrieve a tasks ARN to be used in a stop-task call."""
        return self.task_to_arn.get(self.task_name)

    @property
    def task_id(self):
        """Retrieve a tasks ID by parsing the task's ARN."""
        return self.task_arn.rsplit('/', 1)[-1]

    @property
    def task_to_arn(self):
        """Create a dictionary of task ARN's with task name keys so they can be easily translated."""
        name_to_arns = {}
        for arn in self.cluster_tasks_arns:
            description = Popen('aws ecs describe-tasks --cluster {0} --tasks {1}'.format(self.cluster, arn),
                                shell=True, stdout=PIPE).stdout

            for row in description:
                cols = str(row.decode("utf-8")).strip().split('\t')
                if cols[0] == 'TASKS':
                    name_to_arns[cols[8].strip('family:')] = arn
        return name_to_arns

    @property
    def cluster_tasks_arns(self):
        """Retrieve a task's full Amazon Resource Number (ARN) by listing all tasks in a cluster."""
        return [str(i.decode("utf-8")).strip().split('\t')[1] for i in
                Popen('aws ecs list-tasks --cluster {0}'.format(self.cluster), shell=True, stdout=PIPE).stdout]

    def _assert_cluster(self):
        """Confirm that a cluster value has been set."""
        assert self.cluster, 'An EC2 cluster (short name or full Amazon Resource Name) must be specified'

    def _assert_task(self):
        """Confirm that a cluster value has been set."""
        assert self.task_name, 'An Task ID or full ARN must be specified'


if __name__ == '__main__':
    print(Task('persistent-storage', 'persistent-storage').task_id)
