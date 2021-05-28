# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""
import os

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

common = gcp.CommonTemplates()

default_version = "v1"

for library in s.get_staging_dirs(default_version):
    # rename library to google-cloud-service-directory
    s.replace(
        [library / "google/**/*.py", library / "tests/**/*.py"],
        "google-cloud-servicedirectory",
        "google-cloud-service-directory",
    )

    # surround path with * with ``
    s.replace(library / "google/**/*.py", """["'](projects/\*/.*)["']\.""", "``\g<1>``")

    s.move(
        library,
        excludes=[
            "setup.py",
            "README.rst",
            "docs/index.rst",
            f"scripts/fixup_servicedirectory_{library.name}_keywords.py",
        ],
    )

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(cov_level=100, samples=False, microgenerator=True,)

s.move(
    templated_files, excludes=[".coveragerc"]
)  # the microgenerator has a good coveragerc file

s.shell.run(["nox", "-s", "blacken"], hide_output=False)