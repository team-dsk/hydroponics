#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.config

class LOG_UTIL(object):
    def __init__(self):

    def getLogger(name):
        logging.config.fileConfig('logging.config')

        logging.basicConfig(format="%(asctime)s - %(levelname)s - line %(lineno)d - %(name)s - %(filename)s - \n*** %(message)s") # defaultはlevel=logging.DEBUG)
        logging.getLogger("googleapiclient.discovery_cache").setLevel(level=logging.ERROR) # ImportErrorがおびただしく出てくるので、ここのlogは不要
        logging.getLogger("googleapiclient.discovery").setLevel(level=logging.DEBUG) # このログは出してほしい

        return logger = logging.getLogger(name)
