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

    def update_history(self, json_path, data):
        """Store deployment parameters in history.json."""
        # Add 'time' and 'tasks' keys to data if they're missing
        if 'time' not in data.keys():
            data['time'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        if 'tasks' not in data.keys():
            data['tasks'] = self.tasks

        json = JSON(json_path)
        history_json = json.read()
        history_json['history'].append(data)
        json.write(history_json, sort_keys=False)


def most_recent_history(json_path):
    """Get the most recent deployment parameters from history.json."""
    try:
        return JSON(json_path).read()['history'][-1]
    except IndexError:
        return dict()
