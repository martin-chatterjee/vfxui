# Copyright (c) 2019-2025, Martin Chatterjee. All rights reserved.
# Licensed under the terms of the MIT license. (--> LICENSE.txt)

"""@package vfxui.binding

Import a valid binding and store it in `BINDING`.

Try to import a binding in this order:
    - Qt.py
    - PySide6
    - PySide2
    - PyQt5

Redirect all attribute and submodule imports into `BINDING`.

"""

import importlib
import logging


BINDING = None
"""Resolved binding"""


def __getattr__(name):
    """Redirect all unresolved attribute calls to `BINDING`.

    First try to return an actual attribute. If that does not exist, then
    try to import and return a submodule.

    """
    if BINDING:
        try:
            return getattr(BINDING, name)
        except AttributeError:
            return importlib.import_module(f"{BINDING.__name__}.{name}")
    raise AttributeError(f"Module '{__name__}' has no attribute '{name}'")


def import_binding():
    """Import and return the first valid binding.

    Returns:
        Imported module

    """
    logger = logging.getLogger(f"{__name__}.import_binding")
    supported_bindings = ["Qt", "PySide6", "PySide2", "PyQt5"]

    for binding_name in supported_bindings:
        try:
            binding = importlib.import_module(binding_name)
            logger.debug(f"Using binding: '{binding_name}'")
            return binding
        except ImportError:
            logger.debug(f"Binding not available: '{binding_name}'")
    logger.error(
        f"Found no valid binding. (Supported bindings: '{supported_bindings}')"
    )


BINDING = import_binding()
