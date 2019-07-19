# -*- coding: utf-8 -*-
#
# Copyright (c) 2017-2019, Martin Chatterjee. All rights reserved.
# Licensed under MIT License (--> LICENSE.txt)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
class Guard(object):

    # -------------------------------------------------------------------------
    def __init__(self):
        """
        """
        self.exc_type = None
        self.exc_value = None
        self.exc_traceback = None

    # -------------------------------------------------------------------------
    def __enter__(self):
        """
        """
        return self

    # -------------------------------------------------------------------------
    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        """
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.exc_traceback = exc_traceback

        return True
