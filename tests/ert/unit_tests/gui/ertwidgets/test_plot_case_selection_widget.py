from PyQt6.QtCore import Qt
from pytestqt.qtbot import QtBot

from ert.gui.tools.plot.plot_api import EnsembleObject
from ert.gui.tools.plot.plot_ensemble_selection_widget import (
    EnsembleSelectionWidget,
    EnsembleSelectListWidget,
)
from tests.ert.ui_tests.gui.conftest import get_child


def test_ensemble_selection_widget_max_min_selection(qtbot: QtBot):
    test_ensemble_names = [
        EnsembleObject(
            name=f"case{i}",
            id="id",
            hidden=False,
            experiment_name="exp",
            started_at="2012-12-10T00:00:00",
        )
        for i in range(10)
    ]
    widget = EnsembleSelectionWidget(test_ensemble_names, 1)
    qtbot.addWidget(widget)
    list_widget = get_child(widget, EnsembleSelectListWidget, "ensemble_selector")

    assert (
        len(widget.get_selected_ensembles()) == list_widget.MAXIMUM_SELECTED
    )  # initially 5 selected

    qtbot.mouseClick(
        list_widget.viewport(),
        Qt.MouseButton.LeftButton,
        pos=list_widget.visualItemRect(list_widget.item(0)).center(),
    )  # deselect one item

    assert (
        len(widget.get_selected_ensembles()) == list_widget.MAXIMUM_SELECTED - 1
    )  # 4 selected

    for index in range(list_widget.count()):  # deselect all selected items
        it = list_widget.item(index)
        if it and it.data(Qt.ItemDataRole.CheckStateRole):
            qtbot.mouseClick(
                list_widget.viewport(),
                Qt.MouseButton.LeftButton,
                pos=list_widget.visualItemRect(it).center(),
            )

    assert len(widget.get_selected_ensembles()) == list_widget.MINIMUM_SELECTED
