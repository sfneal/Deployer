from Deployer.docker.docker import Docker
from Deployer.aws.ecs.task.task import Task
from Deployer.aws.ecs.gui import deploy_gui
from Deployer.aws.config import ECS_HISTORY_JSON


def main():
    params = deploy_gui()

    # Build and push Docker image to DockerHub
    docker = Docker(source=params['source'],
                    username=params['docker_user'],
                    repo=params['docker_repo'],
                    tag=params['docker_repo_tag'])
    docker.build()
    docker.push()

    # Restart the previously defined task to pull latest Docker image
    task = Task(params['cluster'], params['task_name'])
    task.stop()
    task.run()

    task.show_tasks()
    task.update_history(ECS_HISTORY_JSON, params)


if __name__ == '__main__':
    main()
