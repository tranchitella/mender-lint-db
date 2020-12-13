# Copyright 2020 Northern.tech AS
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http:#www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from setuptools import setup, find_packages

import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="mender-lint-db",
    version="1.0.0",
    description="Mender database linter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tranchitella/mender-lint-db",
    author="Fabio Tranchitella",
    author_email="fabio.tranchitella@northern.tech",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: Apache 2 License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.5, <4",
    install_requires=["click>=7.1", "pymongo>=3.11", "colorlog"],
    entry_points={
        "console_scripts": [
            "mender-lint-db=mender_lint_db.main:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/tranchitella/mender-lint-db/issues",
        "Source": "https://github.com/tranchitella/mender-lint-db/",
    },
)
