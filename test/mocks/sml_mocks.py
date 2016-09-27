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

import numpy as np

from monasca_analytics.exception import monanas as err
from monasca_analytics.ingestor import base as base_ing
from monasca_analytics.ldp import base as base_ldp
from monasca_analytics.sink import base as base_snk
from monasca_analytics.sml import base as base_sml
from monasca_analytics.source import base as base_src
from monasca_analytics.spark import aggregator
from monasca_analytics.voter import base as base_voter


class SMLMocks(object):
    """
    Auxiliary class to track modules instantiations, classes got by name,
    and validated configuration.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """
        Resets all the elements (counts and lists)
        """
        self.instantiated = {"src_module1": [],
                             "src_module2": [],
                             "IPTablesSource": [],
                             "ingestor_module": [],
                             "sml_module": [],
                             "voter_module": [],
                             "sink_module1": [],
                             "sink_module2": [],
                             "ldp_module1": []
                             }
        self.classes_got_by_name = []
        self.bound_sources = []
        self.terminated_sources = []
        self.killed = False

    def reset_connections(self):
        """
        Resets the variables of the instantiated elements only
        """
        for comp_type in self.instantiated.values():
            for comp in comp_type:
                comp.reset_vars()

sml_mocks = SMLMocks()


class MockClass_src(base_src.BaseSource):

    def __init__(self, _id, _config):
        super(MockClass_src, self).__init__(_id, _config)
        self.reset_vars()

    def reset_vars(self):
        self.get_feature_list_cnt = 0
        self.create_pcollection_cnt = 0
        self.create_dstream_cnt = 0
        self.terminate_source_cnt = 0

    @staticmethod
    def validate_config(_config):
        pass

    @staticmethod
    def get_default_config():
        return {"module": MockClass_src.__name__}

    @staticmethod
    def get_params():
        return []

    def get_feature_list(self):
        self.get_feature_list_cnt += 1
        return ["a", "b"]

    def create_dstream(self, ssc):
        self.create_dstream_cnt += 1
        return ssc.mockDStream()

    def create_pcollection(self, ssc):
        self.create_pcollection_cnt += 1
        # TODO(MARCO) return Mock.PCollection return ssc.mockDStream()

    def terminate_source(self):
        self.terminate_source_cnt += 1


class MockClass_src_module1(MockClass_src):

    def __init__(self, _id, _config):
        sml_mocks.instantiated["src_module1"].append(self)
        super(MockClass_src_module1, self).__init__(_id, _config)


class MockClass_src_module2(MockClass_src):

    def __init__(self, _id, _config):
        sml_mocks.instantiated["src_module2"].append(self)
        super(MockClass_src_module2, self).__init__(_id, _config)


class MockClass_src_module3(MockClass_src):

    def __init__(self, _id, _config):
        sml_mocks.instantiated["IPTablesSource"].append(self)
        super(MockClass_src_module3, self).__init__(_id, _config)


class MockClass_ingestor_module(base_ing.BaseIngestor):

    def __init__(self, _id, _config):
        super(MockClass_ingestor_module, self).__init__(_id, _config)
        sml_mocks.instantiated["ingestor_module"].append(self)
        self.reset_vars()

    @staticmethod
    def validate_config(_config):
        pass

    @staticmethod
    def get_default_config():
        return {"module": MockClass_ingestor_module.__name__}

    @staticmethod
    def get_params():
        return []

    def reset_vars(self):
        self.map_dstream_cnt = 0
        self.map_pcollection_cnt = 0

    def map_dstream(self, dstream):
        self.map_dstream_cnt += 1
        return dstream

    def map_pcollection(self, pcollection):
        self.map_pcollection_cnt += 1
        return pcollection


class MockClass_aggr_module(aggregator.Aggregator):

    def __init__(self, driver):
        super(MockClass_aggr_module, self).__init__(driver)
        self.reset_vars()

    @staticmethod
    def validate_config(_config):
        pass

    @staticmethod
    def get_default_config():
        return {"module": MockClass_aggr_module.__name__}

    @staticmethod
    def get_params():
        return []

    def reset_vars(self):
        self.accumulate_dstream_samples_cnt = 0
        self.accumulate_pcollection_samples_cnt = 0
        self.append_sml_cnt = 0
        self._smls = []

    def append_sml(self, sml):
        super(MockClass_aggr_module, self).append_sml(sml)
        self.append_sml_cnt += 1

    def accumulate_dstream_samples(self, dstream):
        self._samples = np.array([])
        self._combined_stream = None
        super(MockClass_aggr_module, self).accumulate_dstream_samples(dstream)
        self.accumulate_dstream_samples_cnt += 1

    #TODO(Marco) accumulate pcollection samples
    def accumulate_pcollection_samples(self, pcollection):
        self._samples = np.array([])
        self._combined_stream = None
        super(MockClass_aggr_module, self).accumulate_pcollection_samples(pcollection)
        self.accumulate_pcollection_samples_cnt += 1


class MockClass_sml_module(base_sml.BaseSML):

    def __init__(self, _id, _config):
        super(MockClass_sml_module, self).__init__(_id, _config)
        sml_mocks.instantiated["sml_module"].append(self)
        self.reset_vars()

    @staticmethod
    def validate_config(_config):
        pass

    @staticmethod
    def get_default_config():
        return {"module": MockClass_sml_module.__name__}

    @staticmethod
    def get_params():
        return []

    def reset_vars(self):
        self._voter = None
        self.learn_structure_cnt = 0

    def learn_structure(self, _):
        self.learn_structure_cnt += 1

    def number_of_samples_required(self):
        return 0


class MockClass_voter_module(base_voter.BaseVoter):

    def __init__(self, _id, _config):
        super(MockClass_voter_module, self).__init__(_id, _config)
        sml_mocks.instantiated["voter_module"].append(self)
        self.reset_vars()

    @staticmethod
    def validate_config(_config):
        pass

    @staticmethod
    def get_default_config():
        return {"module": MockClass_voter_module.__name__}

    @staticmethod
    def get_params():
        return []

    def reset_vars(self):
        self.elect_structure_cnt = 0

    def elect_structure(self, _):
        self.elect_structure_cnt += 1


class MockClass_sink(base_snk.BaseSink):

    def __init__(self, _id, _config):
        super(MockClass_sink, self).__init__(_id, _config)
        self.reset_vars()

    def reset_vars(self):
        self.sink_dstream_cnt = 0
        self.sink_pcollection_cnt = 0
        self.sink_sml_cnt = 0

    @staticmethod
    def validate_config(_config):
        pass

    @staticmethod
    def get_default_config():
        return {"module": MockClass_sink.__name__}

    @staticmethod
    def get_params():
        return []

    def sink_dstream(self, _):
        self.sink_dstream_cnt += 1

    def sink_pcollection(self, _):
        self.sink_pcollection_cnt += 1

    def sink_ml(self, *_):
        self.sink_sml_cnt += 1


class MockClass_sink_module1(MockClass_sink):

    def __init__(self, _id, _config):
        sml_mocks.instantiated["sink_module1"].append(self)
        super(MockClass_sink_module1, self).__init__(_id, _config)


class MockClass_sink_module2(MockClass_sink):

    def __init__(self, _id, _config):
        sml_mocks.instantiated["sink_module2"].append(self)
        super(MockClass_sink_module2, self).__init__(_id, _config)


class MockClass_ldp_module1(base_ldp.BaseLDP):

    def __init__(self, _id, _config):
        super(MockClass_ldp_module1, self).__init__(_id, _config)
        sml_mocks.instantiated["ldp_module1"].append(self)
        self.reset_vars()

    @staticmethod
    def validate_config(_config):
        pass

    @staticmethod
    def get_default_config():
        return {"module": MockClass_ldp_module1.__name__}

    @staticmethod
    def get_params():
        return []

    def map_dstream(self, dstream):
        self.map_dstream_cnt += 1
        return dstream

    def map_pcollection(self, pcollection):
        self.map_pcollection_cnt += 1
        return pcollection

    def reset_vars(self):
        #TODO(Marco) remove reference to dstream
        self.map_dstream_cnt = 0
        self.map_pcollection_cnt += 0


def mock_kill(pid, code):
    sml_mocks.killed = True


def mock_get_class_by_name(module, class_type):
    sml_mocks.classes_got_by_name.append([module, class_type])
    if module == "src_module1":
        return MockClass_src_module1
    elif module == "src_module2":
        return MockClass_src_module2
    elif module == "IPTablesSource":
        return MockClass_src_module3
    elif module == "ingestor_module":
        return MockClass_ingestor_module
    elif module == "aggr_module":
        return MockClass_aggr_module
    elif module == "sml_module":
        return MockClass_sml_module
    elif module == "voter_module":
        return MockClass_voter_module
    elif module == "sink_module1":
        return MockClass_sink_module1
    elif module == "sink_module2":
        return MockClass_sink_module2
    elif module == "ldp_module1":
        return MockClass_ldp_module1
    raise err.MonanasNoSuchClassError("testing NoSuchClassError")
