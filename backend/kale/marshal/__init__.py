#  Copyright 2019-2020 The Kale Authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from .resource_save import resource_save
from .resource_load import resource_load

from .backends import *


def setup_logging():
    """Configure logging."""
    # Setup root logger
    root_stream_handler = logging.StreamHandler()
    root_stream_handler.setLevel(logging.INFO)
    root_stream_handler.setFormatter(logging.Formatter(
        "%(asctime)s Kale Marshalling [%(levelname)s] %(message)s",
        "%H:%M:%S"))

    _log = logging.getLogger("kale.marshal")
    _log.setLevel(logging.INFO)
    _log.addHandler(root_stream_handler)


setup_logging()