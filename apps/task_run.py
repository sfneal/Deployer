from Deployer.aws.ecs.task import Task
from Deployer.aws.ecs.task_gui import run


def main():
    params = run()
    task = Task(cluster=params['cluster'],
                task=params['task'])

    # Stop the task from running
    task.run(params['launch_type'])

    task.show_tasks()


if __name__ == '__main__':
    main()
