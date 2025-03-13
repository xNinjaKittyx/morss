
from datetime import datetime
from glob import glob
import json
import os

from hatchling.metadata.plugin.interface import MetadataHookInterface


def get_version():
    with open("src/morss/__init__.py", "r+") as file:
        lines = file.readlines()

        # look for hard coded version number
        for i in range(len(lines)):
            if lines[i].startswith("__version__"):
                version = lines[i].split('"')[1]
                break

        # create (& save) one if none found
        if version == "":
            version = datetime.now().strftime("%Y%m%d.%H%M")
            lines[i] = '__version__ = "' + version + '"\n'

            file.seek(0)
            file.writelines(lines)

        # return version number
        return version


class JSONMetaDataHook(MetadataHookInterface):
    def update(self, metadata):
        metadata["version"] = get_version()
