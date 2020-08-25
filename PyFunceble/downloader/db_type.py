"""
The tool to check the availability or syntax of domain, IP or URL.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

Provides the downloader of the desired database type file.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/special-thanks.html

Contributors:
    https://pyfunceble.github.io/contributors.html

Project link:
    https://github.com/funilrys/PyFunceble

Project documentation:
    https://pyfunceble.readthedocs.io/en/master/

Project homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from os import sep as directory_separator

import PyFunceble

from .base import DownloaderBase


class DBTypeDownloader(DownloaderBase):
    """
    Provides the downloader of the desired database type file.
    """

    DOWNTIME_INDEX = "db_type"
    REDOWNLOAD_AFTER = 0

    def __init__(self):
        is_cloned_version = PyFunceble.abstracts.Version.is_local_cloned()
        destination_directory = (
            f"{PyFunceble.CONFIG_DIRECTORY}"
            f"{PyFunceble.CONFIGURATION.outputs.db_type.directory}"
        )

        if not destination_directory.endswith(directory_separator):
            destination_directory += directory_separator

        destination_dir_instance = PyFunceble.helpers.Directory(destination_directory)

        not_supported_db_types = ["json"]

        self.destination = (
            f"{destination_directory}"
            f"{PyFunceble.OUTPUTS.db_type.files[PyFunceble.CONFIGURATION.db_type]}"
        )

        if not is_cloned_version and (
            PyFunceble.CONFIGURATION.db_type not in not_supported_db_types
        ):
            destination_dir_instance.delete()

            if PyFunceble.CONFIGURATION.db_type not in not_supported_db_types:
                destination_dir_instance.create()

                self.DOWNTIME_INDEX += f"_{PyFunceble.CONFIGURATION.db_type}"  # pylint: disable=invalid-name

                self.download_link = PyFunceble.converter.InternalUrl(
                    PyFunceble.CONFIGURATION.links[PyFunceble.CONFIGURATION.db_type]
                ).get_converted()

                super().__init__()

                self.process()