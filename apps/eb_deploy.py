from looptools import Timer
from Deployer.aws.eb import ElasticBeanstalk, gui


def get_params():
    """Collect ElasticBeanstalk deployment parameters."""
    parameters = []
    another = True
    while another:
        p = gui()
        parameters.append(p)
        if p['another_deploy'] is False:
            break
    return parameters


def eb_util_init(params):
    """Initialize ElasticBeanstalk class and return instance."""
    return ElasticBeanstalk(source=params['source'],
                            aws_application_name=params['aws_application-name'],
                            aws_environment_name=params['aws_environment-name'],
                            aws_instance_key=params['aws_instance-key'],
                            aws_version=params['aws_version'],
                            aws_version_description=params['aws_version-description'],
                            docker_user=params['docker_user'],
                            docker_repo=params['docker_repo'],
                            docker_repo_tag=params['aws_version'],
                            dockerfile=params['dockerfile'],
                            host_port=params['host_port'],
                            container_port=params['container_port'])


@Timer.decorator
def eb_deploy(eb):
    # Ensure directory has been initialized as an Elastic Beanstalk app and that config is correct
    eb.initialize()

    # Build and push Docker image to DockerHub
    eb.Docker.build()
    eb.Docker.push()

    # Deploy application by creating or updating an environment
    eb.deploy()

    eb.show_tasks()


def main():
    # Executing Elastic Beanstalk deployments
    for params in get_params():
        # eb_deploy(eb_util_init(params))
        eb = eb_util_init(params)
        l = eb.list(verbose=True)
        for k, v in l.items():
            print(k, v)
        print(len(l))


if __name__ == '__main__':
    main()
