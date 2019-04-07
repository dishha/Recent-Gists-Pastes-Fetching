"""
Module Introduction.

Any module level documentation comes here.
"""
import logging
import re
import requests
import json
from tf_workers import (  # pylint: disable=E0611
    Worker, SettingProperty, WorkerResponse, ResponseCodes as RC
)
from tf_workers.config import ApplicationConfig  # pylint: disable=E

config = ApplicationConfig.get_config()

log = logging.getLogger(__name__)


class MyWorker(Worker):
    """
    MyWorker.

    Description and list of parameters. For example:

    :param domain_or_ip:
        Required - The domain or IP Address to perform whois and IPWhois on
    """

    name = 'myworker'
    resource_requirements = 'LOW'
    requires = [
        # any additional python modules come here
    ]
    os_requires = [
        # Any additional OS (Linux-Ubuntu) packages come here
            ]

    def _init_settings(self):
        """Initialize worker settings."""
        super()._init_settings()
        # Add any arguments/properties required by the worker here.
        # self.settings.add(SettingProperty(
        #     name='property_name', data_type=str,
        #     description='property description'))

        # Note: These are inputs to the worker. If you want any information
        # passed to the worker it must be added to self.settings

        self.settings.add(SettingProperty(
             name='number_of_pates_gists', data_type=int,
             description='no. of fetches'))

        self.settings.add(SettingProperty(
            name='match_patterns', data_type=list,
            description='regex list'))

    def __init__(self, **kwargs):
        """Create worker object."""
        super().__init__(kwargs)
        self.page = 1
        self.gist_url = "https://api.github.com/gists?page=%s&per_page=100" % self.page
        self.paste_url = "https://snippets.glot.io/snippets?page=%s" % self.page
        self.matched_gist_urls = []
        self.matched_paste_urls = []

    def run(self):
        """Call this method to run the WHOIS worker."""
        super().run()
        self.response = WorkerResponse()
        self.response.response_code = RC.SUCCESS
        self.response.data = []

        # TODO: Actual worker code comes here for performing worker task and
        # populating self.response.data with the result.
        # If you have defined any input settings in _init_settings() those
        # are accessible here using self.settings.setting_name.value

        for self.page in range(1, 30):
            gist_url_response = requests.get(self.gist_url)
            gist_data = gist_url_response.text
            gists = json.loads(gist_data)

            paste_url_response = requests.get(self.paste_url)
            paste_data = paste_url_response.text
            pastes = json.loads(paste_data)

            for gist in gists:
                for key in gist["files"]:
                    gist_title = gist["files"][key]["filename"]
                    gist_content = str(gist["description"])
                    gist_url = gist["html_url"]
                    matched_regex = []
                    match = 0
                    for regex in self.settings.match_patterns.value:
                        if re.match(regex, gist_title) or re.match(regex, gist_content):
                            matched_regex.append(regex)
                            if gist_url not in self.matched_gist_urls:
                                self.matched_gist_urls.append(gist_url)
                                match = 1

                    if match == 1:
                        self.response.data.append({"url": self.matched_gist_urls[-1], "match": matched_regex}.copy())
                        if len(self.response.data) == self.settings.number_of_pates_gists.value:
                            return self.response, len(self.response.data)

            for paste in pastes:
                paste_title = paste["title"]
                paste_url = paste["url"]
                matched_regex = []
                match = 0
                for regex in self.settings.match_patterns.value:
                    if re.match(regex, paste_title):
                        matched_regex.append(regex)
                        if paste_url not in self.matched_paste_urls:
                            self.matched_paste_urls.append(paste_url)
                            match = 1

                if match == 1:
                    self.response.data.append({"url": self.matched_paste_urls[-1], "match": matched_regex}.copy())
                    if len(self.response.data) == self.settings.number_of_pates_gists.value:
                        return self.response,len(self.response.data)

        return self.response, len(self.response.data)