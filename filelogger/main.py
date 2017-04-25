# -*- coding:utf-8 -*-
"""
    main
    ~~~~~~~~~~~~~~~~~~~

    logger config by file.

    :copyright: (c) 2017 by Blurt Heart.
    :license: BSD, see LICENSE for more details.
"""
import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
logger = logging.getLogger('simpleExample')

# application code
logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')