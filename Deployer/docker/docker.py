import os


class Docker:
    def __init__(self, source, repo, tag, username):
        """
        Docker hub deployment helper.

        :param source: Docker files source path
        :param repo: Docker repo name
        :param tag: Docker repo tag
        :param username: Docker username
        """
        self.source = source
        self.repo = repo
        self.tag = tag
        self.username = username

        self._tasks = []

    def add_task(self, task):
        """Add a complete task to the tasks list."""
        print(task)
        self._tasks.append(task)

    @property
    def docker_image(self):
        """Concatenate DockerHub user name and environment name to create docker image tag."""
        return '{user}/{repo}:{tag}'.format(user=self.username, repo=self.repo, tag=self.tag)

    def build(self):
        """Build a docker image for distribution to DockerHub."""
        print('Building Docker image')
        os.system('docker build -t {0}'.format('{tag} {source}'.format(tag=self.docker_image, source=self.source)))
        self.add_task('Built Docker image {0}'.format(self.docker_image))

    def run(self):
        """Push a docker image to a DockerHub repo."""
        os.system('docker run -i -t -p 5000:5000 {0}'.format(self.docker_image))

    def push(self):
        """Push a docker image to a DockerHub repo."""
        print('Pushing Docker image')
        os.system('docker push {0}'.format(self.docker_image))
        self.add_task('Pushed Docker image {0} to DockerHub repo'.format(self.docker_image))
