import sys
from pkg_resources import resource_stream, resource_exists, resource_isdir, \
        resource_listdir
import json
import re

__version__ = '0.1.2'

cache = dict()


def fetch_resource(name):
    if name not in cache:
        cache[name] = json.loads(resource_stream(__name__,
            name).read().decode('utf-8'))
    return cache[name]


def get_categories(category=None):
    if category is None:
        return resource_listdir(__name__, "data")
    else:
        return [item for item
                in resource_listdir(__name__, "data/" + category)
                if resource_isdir(__name__, "data/" + category + "/" + item)]


def get_files(category):
    return [re.sub(r"\.json$", "", item) for item
            in resource_listdir(__name__, "data/" + category)
            if not resource_isdir(__name__, "data/" + category + "/" + item)]


def get_file(*components):
    return fetch_resource("/".join(["data"] + list(components)) + ".json")


class CorpusLoader(object):
    def __init__(self, directory):
        self.directory = directory

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __getattr__(self, attr):
        file_loc = "data/" + self.directory + "/" + attr + ".json"
        dir_loc = "data/" + self.directory + "/" + attr
        if resource_exists(__name__, file_loc):
            return fetch_resource(file_loc)
        elif resource_exists(__name__, dir_loc) and \
                resource_isdir(__name__, dir_loc):
            return CorpusLoader(self.directory + "/" + attr)
        else:
            raise AttributeError("no resource named " + attr)

    def get_categories(self):
        return get_categories(self.directory)

    def get_files(self):
        return get_files(self.directory)

    def get_file(self, *components):
        return get_file(self.directory, *components)

module = sys.modules[__name__]
for directory in resource_listdir(__name__, "data"):
    setattr(module, directory, CorpusLoader(directory))
