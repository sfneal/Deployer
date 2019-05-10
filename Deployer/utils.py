# Task tracker to universally track completed steps across multiple instances
import os
import re
from RuntimeWatch import TaskTracker, most_recent_history, get_json


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
