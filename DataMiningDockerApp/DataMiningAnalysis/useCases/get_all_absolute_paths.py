"""
Hilfsfile um use cases zu testen.
"""

import os


def get_all_absolute_paths(directory):
    """
    :param directory: The directory to search for files
    :return: A list of absolute paths of all files in the directory
    """
    absolute_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            absolute_path = os.path.abspath(os.path.join(root, file)).replace('\\', '/')
            absolute_paths.append(absolute_path)
    for ele in absolute_paths:
        print(ele)
    return absolute_paths
