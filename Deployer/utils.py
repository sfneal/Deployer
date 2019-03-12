# Task tracker to universally track completed steps across multiple instances
from datetime import datetime
from databasetools import JSON


class TaskTracker:
    _tasks = []

    @property
    def tasks(self):
        """Create a numbered list of completed steps."""
        return ['{0}: {1}'.format(i, step) for i, step in enumerate(self._tasks)]

    def show_tasks(self):
        """Print a list of all the tasks completed."""
        print('\nCompleted to following tasks:')
        for step in self.tasks:
            print('\t{0}'.format(step))

    @classmethod
    def add_task(cls, task):
        """Add a complete task to the tasks list."""
        print(task)
        cls._tasks.append(task)

    def update_history(self, json_path):
        """Store deployment parameters in history.json."""
        json = JSON(json_path)
        history_json = json.read()
        history_json['history'].append({'aws_application-name': self.aws_application_name,
                                        'aws_environment-name': self.aws_environment_name,
                                        'aws_version': self.aws_version,
                                        'aws_instance-key': self.aws_instance_key,
                                        'docker_user': self.docker_user,
                                        'docker_repo': self.docker_repo,
                                        'docker_repo_tag': self.docker_repo_tag,
                                        'source': self.source,
                                        'time': datetime.now().strftime("%Y-%m-%d %H:%M"),
                                        'tasks': self.tasks})
        json.write(history_json, sort_keys=False)
