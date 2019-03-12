# Task tracker to universally track completed steps across multiple instances
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

    @staticmethod
    def update_history(json_path, data):
        """Store deployment parameters in history.json."""
        json = JSON(json_path)
        history_json = json.read()
        history_json['history'].append(data)
        json.write(history_json, sort_keys=False)


def most_recent_history(json_path):
    """Get the most recent deployment parameters from history.json."""
    return JSON(json_path).read()['history'][-1]
