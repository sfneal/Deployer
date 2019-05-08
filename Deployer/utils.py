# Task tracker to universally track completed steps across multiple instances
import os
import re
from datetime import datetime
from databasetools import JSON


def get_json(json_path):
    """
    Retrieve a JSON object ready to read and write history files.

    Create a history json if it does not exist and return a
    JSON object to write to.

    :param json_path: Path to history.json file
    :return: JSON object
    """
    json = JSON(json_path)
    if not os.path.exists(json_path):
        json.write({'history': []})
    return json


class TaskTracker:
    _tasks = []
    _commands = []

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

    @property
    def commands(self):
        """Create a numbered list of completed steps."""
        return ['{0}: {1}'.format(i, cmd) for i, cmd in enumerate(self._commands)]

    def show_commands(self):
        """Print a list of all the tasks completed."""
        print('\nExecuted the following commands:')
        for cmd in self.commands:
            print('\t{0}'.format(cmd))

    @classmethod
    def add_command(cls, cmd):
        """Add an executed command to the commands list."""
        print(cmd)
        cls._commands.append(cmd)

    def update_history(self, json_path, data):
        """Store deployment parameters in history.json."""
        # Add 'time' and 'tasks' keys to data if they're missing
        if 'time' not in data.keys():
            data['time'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        if 'tasks' not in data.keys():
            data['tasks'] = self.tasks

        json = get_json(json_path)
        history_json = json.read()
        history_json['history'].append(data)
        json.write(history_json, sort_keys=False)


def most_recent_history(json_path):
    """Get the most recent deployment parameters from history.json."""
    try:
        return JSON(json_path).read()['history'][-1]
    except IndexError:
        return dict()


# Retrieve version number
def get_version(source):
    """
    Retrieve the version of a python distribution.

    version_file default is the <project_root>/_version.py

    :param source: Path to project root
    :return: Version string
    """
    version_str_lines = open(os.path.join(source, os.path.basename(source), '_version.py'), "rt").read()
    version_str_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(version_str_regex, version_str_lines, re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % os.path.join(source, os.path.basename(source)))


def set_version(source):
    """
    Set the version of a python distribution.

    version_file default is the <project_root>/_version.py

    :param source: Path to project root
    :return: Version string
    """
    with open(os.path.join(source, os.path.basename(source), '_version.py'), "r+") as version_file:
        # Read existing version file
        version_str_lines = version_file.read()

        # Extract current version
        current_version = version_str_lines[version_str_lines.index("'") + 1:len(version_str_lines) - 2]
        parts = current_version.split('.')
        parts[-1] = str(int(parts[-1]) + 1)

        # Concatenate new version parts
        new_version = '.'.join(parts)

        # Write new version
        version_file.seek(0)
        version_file.truncate()
        version_file.write(version_str_lines.replace(current_version, new_version))
    return new_version
