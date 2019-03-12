from Deployer.docker import Docker, gui


def main():
    params = gui()
    docker = Docker(source=params['source'],
                    repo=params['docker_repo'],
                    tag=params['docker_repo_tag'],
                    username=params['docker_user'])

    # Build docker image
    if params['build']:
        docker.build()

    # Push docker image to Docker Hub
    if params['push']:
        docker.push()

    # Run docker image locally
    if params['run']:
        docker.run()

    docker.show_tasks()


if __name__ == '__main__':
    main()
