#!/usr/bin/env python

# Copyright (c) 2016 Hewlett Packard Enterprise Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from monasca_analytics.source import base


class MockBaseSource(base.BaseSource):

    validation_cnt = 0

    def __init__(self, _id, _config):
        MockBaseSource.validation_cnt = 0
        self.before_binding_cnt = 0
        self.after_binding_cnt = 0
        self.before_unbinding_cnt = 0
        self.after_unbinding_cnt = 0
        super(MockBaseSource, self).__init__(_id, _config)

    @staticmethod
    def validate_config(_config):
        MockBaseSource.validation_cnt += 1

    @staticmethod
    def get_default_config():
        return {"module": MockBaseSource.__name__}

    @staticmethod
    def get_params():
        return []

    # TODO(MARCO): deprecate
    def create_dstream(self, ssc):
        self.before_binding_cnt += 1
        return None

    def create_pcollection(self, ssc):
        self.before_binding_cnt += 1
        return None

    def terminate_source(self):
        pass

    def get_feature_list(self):
        pass
