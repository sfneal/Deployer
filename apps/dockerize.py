from looptools import Timer

from Deployer.docker import Docker, gui
from Deployer.aws.config import DOCKER_HISTORY_JSON


def main():
    params = gui()
    with Timer():
        docker = Docker(source=params['source'],
                        repo=params['docker_repo'],
                        tag=params['docker_repo_tag'],
                        username=params['docker_user'],
                        host_port=params['host_port'],
                        container_port=params['container_port'])

        # Build docker image
        if params['actions']['build']:
            docker.build()

        # Push docker image to Docker Hub
        if params['actions']['push']:
            docker.push()

        # Run docker image locally
        if params['actions']['run']:
            docker.run()

        docker.show_tasks()
        docker.update_history(DOCKER_HISTORY_JSON, params)
        print(docker.available_commands)


if __name__ == '__main__':
    main()
