import pytest

import vfxui.binding


@pytest.mark.parametrize(
    "available_bindings, imported_binding",
    (
        (
            ["Qt", "PySide6", "PySide2", "PyQt5"],
            "Qt",
        ),
        (
            ["PySide6", "PySide2", "PyQt5"],
            "PySide6",
        ),
        (
            ["PySide2", "PyQt5"],
            "PySide2",
        ),
        (
            ["PyQt5"],
            "PyQt5",
        ),
    ),
    ids=(
        "Qt.py-is-available",
        "PySide6-is-available",
        "PySide2-is-available",
        "PyQt5-is-available",
    ),
)
def test_import_binding_respects_binding_order(
    mocker, available_bindings, imported_binding
):
    """Ensure that the binding order is respected while importing a binding."""

    def _mocked_import_module(name=None, package=None):
        if name in available_bindings:
            return mocker.Mock(__name__=name)
        raise ImportError

    mocker.patch(
        "vfxui.binding.importlib.import_module", side_effect=_mocked_import_module
    )

    binding = vfxui.binding.import_binding()

    assert binding and binding.__name__ == imported_binding


def test_import_binding_returns_None_if_no_binding_is_available(mocker):
    """Ensure that import_binding() returns None if no binding is importable."""
    mocker.patch("vfxui.binding.importlib.import_module", side_effect=ImportError)

    binding = vfxui.binding.import_binding()

    assert binding is None


def test_getattr_redirects_unresolved_attributes_into_binding(mocker):
    """"""

    class mocked_binding:
        def __init__(self):
            self.some_attribute = "attribute_value"
            self.__name__ = "mocked_binding"

        def some_method(self):
            return "method_return_value"

    mocker.patch("vfxui.binding.BINDING", mocked_binding())

    assert vfxui.binding.some_attribute == "attribute_value"
    assert vfxui.binding.some_method() == "method_return_value"

    with pytest.raises(ImportError):
        with pytest.raises(AttributeError):
            vfxui.binding.does_not_exist


def test_getattr_raises_AttributeError_if_no_binding_is_found(mocker):
    """"""
    mocker.patch("vfxui.binding.BINDING", None)

    with pytest.raises(AttributeError):
        vfxui.binding.some_attribute
