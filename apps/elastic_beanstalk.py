from Deployer.aws.eb import ElasticBeanstalk, gui


def main():
    params = gui()
    eb = ElasticBeanstalk(source=params['source'],
                          aws_application_name=params['aws_application-name'],
                          aws_environment_name=params['aws_environment-name'],
                          aws_instance_key=params['aws_instance-key'],
                          aws_version=params['aws_version'],
                          docker_user=params['docker_user'],
                          docker_repo=params['docker_repo'],
                          docker_repo_tag=params['docker_repo_tag'])
    eb.deploy()
    eb.show_tasks()


if __name__ == '__main__':
    main()
