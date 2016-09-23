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

import copy

SOURCES = "sources"
INGESTORS = "ingestors"
SMLS = "smls"
VOTERS = "voters"
SINKS = "sinks"
LDPS = "ldps"
CONNECTIONS = "connections"
FEEDBACK = "feedback"

components_types = [SOURCES, INGESTORS, SMLS, VOTERS, SINKS, LDPS]


_default_spark_base_config = {
    "spark_config": {
        "appName": "testApp",
        "streaming": {
            "batch_interval": 1
        }
    },
    "server": {
        "port": 3000,
        "debug": False
    },
    "sources": {},
    "ingestors": {},
    "smls": {},
    "voters": {},
    "sinks": {},
    "ldps": {},
    "connections": {},
    "feedback": {}
}

# TODO(Marco) Generate a apache beam base config


def get_default_base_config():
    return copy.deepcopy(_default_spark_base_config)
