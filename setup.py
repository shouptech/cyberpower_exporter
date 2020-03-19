# Copyright 2020 Mike Shoup
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

from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
# Get contents of README
with open(path.join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

install_requires = [
    "prometheus-client==0.7.1",
]

setup(
    name="cyberpower_exporter",
    version="0.1",
    url="https://github.com/shouptech/cyberpower_exporter",
    author="Mike Shoup",
    author_email="mike@shoup.io",
    description="Prometheus exporter for cyberpower ups units.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=install_requires,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "console_scripts": [
            "cyberpower_exporter = cyberpower_exporter.command:main"
        ]
    },
)
