# This file is part of morss
#
# Copyright (C) 2013-2020 pictuga <contact@pictuga.com>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/>.

import os
import os.path
import sys


def pkg_path(*path_elements):
    return os.path.join(os.path.dirname(__file__), *path_elements)


data_path_base = None


def data_path(*path_elements):
    global data_path_base

    path = os.path.join(*path_elements)

    if data_path_base is not None:
        return os.path.join(data_path_base, path)

    bases = [
        os.path.join(sys.prefix, "share/morss"),  # when installed as root
        pkg_path("../../../share/morss"),
        pkg_path("../../../../share/morss"),
        pkg_path("../share/morss"),  # for `pip install --target=dir morss`
        pkg_path(".."),  # when running from source tree
    ]

    if "DATA_PATH" in os.environ:
        bases.append(os.environ["DATA_PATH"])

    for base in bases:
        full_path = os.path.join(base, path)

        if os.path.isfile(full_path):
            data_path_base = os.path.abspath(base)
            return data_path(path)

    else:
        raise OSError()
