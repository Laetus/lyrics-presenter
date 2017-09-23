#!/usr/bin/env python
""" Simple Webapp to present lyrics"""
# -*- coding: utf-8 -*-

import classes.WSServer as WSServer

ws_server = WSServer.WSServer('localhost', 8765)
ws_server.start()
