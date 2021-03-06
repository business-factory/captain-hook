# -*- coding: utf-8 -*-

import graypy
import logging
from functools import lru_cache

from . import settings
from .publisher import RabbitPublisher


@lru_cache(maxsize=1)
def logger():
    logger = logging.getLogger("hooks")
    logger.setLevel(logging.DEBUG if settings.DEVELOPMENT_MODE else logging.INFO)

    for handler in logging.root.handlers:
        handler.addFilter(logging.Filter("hooks"))

    if not settings.DEVELOPMENT_MODE:
        handler = graypy.GELFHandler(settings.GRAYLOG_HOST, settings.GRAYLOG_PORT)
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "[%(levelname)s] %(asctime)s at %(filename)s:%(lineno)d (%(processName)s) -- %(message)s",
            "%Y-%m-%d %H:%M:%S")
        )

    logger.addHandler(handler)

    return logger


@lru_cache(maxsize=1)
def publisher():
    return RabbitPublisher(
        settings.RABBIT_LOGIN,
        settings.RABBIT_PASSWORD,
        settings.RABBIT_HOST,
        settings.RABBIT_PORT,
        settings.RABBIT_VIRTUAL_HOST,
        settings.RABBIT_EXCHANGE
    )


@lru_cache(maxsize=1)
def publisher_staging():
    if settings.PROFILE == "staging":
        return None

    return RabbitPublisher(
        settings.RABBIT_LOGIN_STAGING,
        settings.RABBIT_PASSWORD_STAGING,
        settings.RABBIT_HOST_STAGING,
        settings.RABBIT_PORT_STAGING,
        settings.RABBIT_VIRTUAL_HOST,
        settings.RABBIT_EXCHANGE
    )
