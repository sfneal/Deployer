from Deployer.aws.ecs.task.task import Task
from Deployer.aws.ecs.task.gui import register


def main():
    params = register()
    task = Task(task_name=params['task'])

    # Register the task
    task.register(docker_container=params['docker_container'],
                  docker_image=params['docker_image'],
                  port_protocol=params['port_protocol'],
                  port_host=params['port_host'],
                  port_container=params['port_container'],
                  volume_name=params['volume_name'],
                  volume_path=params['volume_path'],
                  container_path=params['container_path'])

    task.show_tasks()


if __name__ == '__main__':
    main()
