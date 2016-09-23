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

"""Monanas Runner.

This script checks for appropriate arguments and starts Monanas to use
data coming from one or more given sources. The source(s) can be configured
using the optional argument --sources. However, a default source using random
data generator is provided in the config folder.

Usage:
    run.py -f <framework_name> -c <config> -l <log_config> [-s <sources>...
        [<sources>]] [-dvh]
    run.py -v | --version
    run.py -h | --help

Options:
    -c --config          Config file.
    -d --debug           Show debug messages.
    -h --help            Show this screen.
    -l --log_config      Log config file's path.
    -f --framework       spark or flink.
    -s --sources         A list of data sources.
    -v --version         Show version.

"""

import json
import logging
import logging.config as log_conf
import os
import subprocess
import sys

import docopt

import setup_property


class RunnerError(Exception):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return repr(self._value)

    @staticmethod
    def enviromentNotDefined(environmentVariableName):
        return RunnerError(r"$" + environmentVariableName + " environment variable not defined.")

def processing_framework_selection(arguments):
    """Selects between supported processing frameworks"""

    monanas_path = os.environ.get('MONANAS_HOME', "")

    if (monanas_path is None):
        raise RunnerError.enviromentNotDefined("MONANAS_HOME")

    framework = "{0}".format(arguments["<framework_name>"])

    if framework == "spark":
        spark_path = os.environ.get("SPARK_HOME")

        if (spark_path is not None):
            command = generate_command_for_spark(monanas_path, spark_path, arguments)
        else:
            raise RunnerError.enviromentNotDefined("SPARK_HOME")

    elif framework == "flink":
        flink_path = os.environ.get("FLINK_HOME")
        if (flink_path is not None):
            submit_binary_path = flink_path
            # TODO (MARCO) generate command for flink
        else:
            raise RunnerError.enviromentNotDefined("FLINK_HOME")
    else:
        raise RunnerError("{0} framework is not supported.".format(arguments("<framework_name>")))

    return command

def generate_command_for_spark(monanas_path, spark_path, arguments):
    """Generates the command line call for a Spark application"""
    submit_binary_path = spark_path + r"/bin/spark-submit"

    try:
        for filename in os.listdir(spark_path + r"/external/kafka-assembly/target"):
            if filename.startswith("spark-streaming-kafka-assembly") and\
               not any(s in filename for s in ["source", "test"]):
                kafka_jar = filename
                break

        if not kafka_jar:
            raise OSError("Spark's external library required does not exist.")

    except OSError as e:
        raise RunnerError(e.__str__())

    spark_kafka_jar = spark_path + "/external/kafka-assembly/target/" + kafka_jar

    command = [
        submit_binary_path, "--master", "local[2]",
        "--jars", spark_kafka_jar, monanas_path + "/monasca_analytics/monanas.py",
        arguments["<config>"], arguments["<log_config>"]
    ]
    command += arguments["<sources>"]

    return command


def main(arguments):

    command = processing_framework_selection(arguments)

    try:
        logger.info("Executing `{}`...".format(" ".join(command)))
        subprocess.Popen(command).communicate()
    except OSError as e:
        raise RunnerError(e.__str__())


def setup_logging(filename):
    """Setup logging based on a json string."""
    with open(filename, "rt") as f:
        config = json.load(f)

    log_conf.dictConfig(config)

if __name__ == "__main__":

    arguments = docopt.docopt(__doc__, version=setup_property.VERSION)

    try:
        setup_logging(arguments["<log_config>"])
    except IOError:
        raise RunnerError("File not found: {0}.".
                          format(arguments["<log_config>"]))
    except ValueError:
        raise RunnerError("{0} is not a valid logging config file.".
                          format(arguments["<log_config>"]))

    logger = logging.getLogger(__name__)

    try:
        main(arguments)
    except KeyboardInterrupt:
        logger.info("Monanas run script stopped.")
    except RunnerError as e:
        logger.error(e.__str__())
    except Exception as e:
        logger.error("Unexpected error: {0}. {1}.".
                     format(sys.exc_info()[0], e))


