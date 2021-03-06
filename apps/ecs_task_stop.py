from Deployer.aws.ecs.task.task import Task
from Deployer.aws.ecs.task.gui import stop


def main():
    params = stop()
    task = Task(cluster=params['cluster'],
                task=params['task'])

    # Stop the task from running
    task.stop(params['reason'])

    task.show_tasks()


if __name__ == '__main__':
    main()
