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

import monasca_analytics.banana.typeck.type_util as util


class ParamDescriptor(object):
    """
    Description of a component parameter. This object contains
    information such as the name of the parameter, the type,
    the default value and a validator that will be evaluated
    when the component is instantiated.
    """

    def __init__(self, name, _type, default=None, validator=None):
        """
        Construct a parameter descriptor.
        :type name: str
        :param name: The name of the parameter
        :type _type: u.String | u.Number | u.Object | u.Enum | u.Any
        :param _type: The type of the parameter
        :type default: str | float | int | dict
        :param default: The default value for the parameter.
        :param validator: Additional validator for the parameter.
        """
        if (not isinstance(_type, util.String) and
                not isinstance(_type, util.Number) and
                not isinstance(_type, util.Object) and
                not isinstance(_type, util.Enum) and
                not isinstance(_type, util.Any)) \
                or \
                (default is not None and
                 not isinstance(default, str) and
                 not isinstance(default, float) and
                 not isinstance(default, int) and
                 not isinstance(default, dict)):
            raise Exception("ParamDescriptor type incorrectly defined")

        self.param_name = name
        self.default_value = default
        self.param_type = _type
        self.validator = validator
