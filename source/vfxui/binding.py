"""@package vfxui.binding

Import a valid binding and store it in `BINDING`.

Try to import a binding in this order:
    - Qt.py
    - PySide6
    - PySide2
    - PyQt5

"""
import importlib
import logging


BINDING = None
"""Resolved binding"""


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
