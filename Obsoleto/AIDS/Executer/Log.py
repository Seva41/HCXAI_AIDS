#!/usr/bin/python
#-*- coding: utf-8 -*-
import logging

def log(funcExec):
    try:
        logger = logging.getLogger()
        hdlr = logging.FileHandler('eventos.log')
        formatter = logging.Formatter('%(levelname)s: %(message)s - %(asctime)s ')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)

        if (logger.hasHandlers()):
            logger.handlers.clear()
        logger.addHandler(hdlr)
        logger.info(funcExec)
        return "ok"
    except IndexError:
        return "error"
    except:
        return "error"