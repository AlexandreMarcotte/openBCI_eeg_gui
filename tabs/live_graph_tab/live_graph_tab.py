# -*- coding: utf-8 -*-
# -- General packages --
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import pyqtgraph as pg
from pyqtgraph.dockarea import *
# -- My packages --
## Graphes
from .dock.eeg_dock.eeg_plots_creator import EegPlotsCreator
from .dock.wave_dock.wave_graph import WaveGraph
from .dock.fft_dock.fft_graph import FftGraph
from .dock.classif_dock.classification_plot_creator import ClassifPlotCreator
from .dock.banner_dock.banner import Banner
from .dock.Viz_3D_dock.viz_3D import Viz3D
from .dock.fft_over_time_3D_dock.fft_over_time_graph import FftOverTimeGraph3D
from .dock.fft_over_time_2D_dock.fft_over_time_graph import FftOverTimeGraph2D

from save.data_saver import DataSaver
from app.colors import *
from tabs.region import Regions


class LiveGraphTab(QWidget):
    def __init__(self, gv, parent):
        super().__init__()
        self.gv = gv
        self.gv.set_main_window(self)
        self.parent = parent

        self.init_tab_w()
        self.docks_menu = self.create_docks_menu()
        self.init_dock_layout()

    def init_tab_w(self):
        self.layout = QHBoxLayout(self)
        self.area = DockArea()
        self.layout.addWidget(self.area)

    def create_docks_menu(self):
        docks_menu = self.parent.main_menu.addMenu('Live graph docks')
        self.parent.main_menu.addMenu(docks_menu)
        return docks_menu

    def init_dock_layout(self):
        self.eeg = DockHandler(
            'EEG', self, self.docks_menu, EegPlotsCreator, [self.gv], 'left',
            size=(6, 10), scroll=True)

        self.fft = DockHandler(
            'FFT', self, self.docks_menu, FftGraph, [self.gv], 'right',
             size=(5, 10), scroll=True)

        self.Wave = DockHandler(
            'Wave', self, self.docks_menu, WaveGraph, [self.gv], 'below',
            self.fft.dock, size=(5, 10), scroll=True)

        self.fft_over_time_3D = DockHandler(
            'FFt over time 3D', self, self.docks_menu, FftOverTimeGraph3D,
            [self.gv], 'below', self.fft.dock, size=(5, 10), scroll=True)

        self.fft_over_time_2D = DockHandler(
            'FFt over time 2D', self, self.docks_menu, FftOverTimeGraph2D,
            [self.gv], 'below', self.fft.dock, size=(5, 10), scroll=True)

        self.classification = DockHandler(
            'Classification', self, self.docks_menu, ClassifPlotCreator,
             [self.gv], 'bottom', self.fft.dock, size=(5, 10), scroll=True)

        self.banner = DockHandler(
            'Banner', self, self.docks_menu, Banner, [], 'bottom',
            self.eeg.dock)

        self.saving = DockHandler(
            'Saving', self, self.docks_menu, DataSaver, [self, self.gv],
            'below', self.banner.dock)
        self.eeg.dock_obj.set_saver(self.saving.dock_obj)

        self.visualization3D = DockHandler(
            'Visualization3D', self, self.docks_menu, Viz3D, [self.gv],
            'below', self.classification.dock, scroll=True)

        self.setLayout(self.layout)


class DockHandler:
    def __init__(self, name, tab, menu, DockObj, param, pos, related_dock=None,
                 size=(1, 1), hide_title=False, scroll=False):
        self.name = name
        self.DockObj = DockObj
        self.param = param
        self.tab = tab
        self.pos = pos
        self.related_dock = related_dock
        self.size = size
        self.hide_title = hide_title
        self.scroll = scroll

        self.first_time = True

        self.dock = self.init_dock()

        self.dock_obj = DockObj(*param)
        if name == 'EEG':
            x = self.dock_obj.regions

        self.state = 'checked'

        self.check_actn = QtGui.QAction(name, tab, checkable=True)
        self.check_actn.setChecked(True)
        self.check_actn.triggered.connect(self.open_close_dock)
        self.check_actn.setStatusTip(f'Check {name} to open this dock...')

        menu.addAction(self.check_actn)

    def init_dock(self):
        dock = Dock(self.name, size=self.size)
        try:
            self.tab.area.addDock(dock, self.pos, self.related_dock)
        except AttributeError:  # The related dock as been deleted
            print('except')
            self.tab.area.addDock(dock, 'bottom')
        layout = pg.LayoutWidget()
        if self.scroll:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            dock.addWidget(scroll)
            scroll.setWidget(layout)
        else:
            dock.addWidget(layout)
        if self.hide_title:
            dock.hideTitleBar()

        if self.first_time:
            self.param.append(layout)
            self.first_time = False
        else:
            self.param.pop()
            self.param.append(layout)

        return dock

    def open_close_dock(self):
        if self.state == 'checked':
            self.dock.close()
            self.state = 'unchecked'

        elif self.state == 'unchecked':
            # self.tab.init_tab_w()
            self.dock = self.init_dock()
            self.dock_obj = self.DockObj(*self.param)
            self.tab.setLayout(self.tab.layout)
            self.state = 'checked'
            if self.name == 'EEG':
                self.tab.eeg.dock_obj.set_saver(self.tab.saving.dock_obj)



