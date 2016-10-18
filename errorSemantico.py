#!/usr/bin/env python
# -*- coding: utf-8 -*-

#error semántico
class errorSemantico(Exception):
      def __init__(self,value):
        self.value = value
      def __str__(self):
        return repr(self.value)