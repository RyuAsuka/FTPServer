# coding:utf-8

import logging
from conf import setting


def config_logger():
    logging.basicConfig(level=logging.DEBUG,
                        filename=setting.logging_name)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    logging.getLogger('').addHandler(console)
