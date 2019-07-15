from pyqtgraph.dockarea import *
from PyQt5.QtWidgets import *
# --My packages--
from V2.GUI.tabs.live_graph_tab.view.docks.main_dock import MainDock
# EEG
from V2.GUI.tabs.live_graph_tab.view.docks.eeg_dock.eeg_dock import EegDock
# FFT
from V2.GUI.tabs.live_graph_tab.view.docks.fft_dock.fft_dock import FftDock
# Viz 3D
from V2.GUI.tabs.live_graph_tab.view.docks.visualization_3d_dock.inner_docks.visualization_3d_settings_dock import Visualisation3dSettingsDock
from V2.GUI.tabs.live_graph_tab.view.docks.visualization_3d_dock.inner_docks.plot.visualization_3d_plot_dock import Visualization3dPlotsDock
#
from .connectors.eeg_dock.eeg_plot_dock_connector import EegPlotsDockConnector
from .connectors.eeg_dock.fft_setting_dock_connector import FftSettingDockConnector
from .connectors.fft_dock.fft_plot_dock_connector import FftPlotsDockConnector
from ..model.model import Model
from ..controller.controller import Controller


class View(QWidget):
    def __init__(self, model: Model, controller: Controller):
        super().__init__()
        self.model = model
        self.controller = controller

        self._init_ui()
        self._connect()
        # listen for model event signals

    def _connect(self):
        """connect widgets to controller"""
        # Plots
        EegPlotsDockConnector(
            n_ch=self.model.N_CH, view=self, model=self.model).connect()
        # Settings
        FftSettingDockConnector(
            n_ch=self.model.N_CH, view=self).connect()
        # Fft
        FftPlotsDockConnector(view=self, model=self.model).connect()

    def _init_ui(self):
        self.area = DockArea()
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.area)
        self._init_docks()

    def _init_docks(self):
        self._init_eeg_dock()
        self._init_fft_dock()
        self._init_visualization_3D_dock()

    def _init_eeg_dock(self):
        self.eeg_dock = EegDock()
        self.area.addDock(self.eeg_dock)

    def _init_fft_dock(self):
        self.fft_dock = FftDock()
        self.area.addDock(self.fft_dock, 'right', self.eeg_dock)

    def _init_visualization_3D_dock(self):
        self.visualization_3D_dock = MainDock(name='Visualization 3D',
            settings_dock=Visualisation3dSettingsDock,
            plot_dock=Visualization3dPlotsDock())
        self.area.addDock(self.visualization_3D_dock, 'bottom', self.fft_dock)




        # fft_dock = EegDock()
        # self.area.addDock(fft_dock, 'right', self.eeg_dock)
        # return fft_dock

        # eeg_inner_dock.dock_area.addDock(PlotDockWidget(
        #     name='Filter Sig out & in',
        #     plot=ScrollPlotWidget(
        #         signals=[self._model.pipeline.filter_stage.output,
        #                  self._model.pipeline.filter_stage.input])))
        #
        # eeg_inner_dock.dock_area.addDock(PlotDockWidget(
        #     name='Timestamp',
        #     plot=ScrollPlotWidget(
        #         signals=[self._model.pipeline.signal_collector.timestamps])))
        #
        # eeg_inner_dock.dock_area.addDock(PlotDockWidget(
        #     name='FFT',
        #     plot=ScrollPlotWidget(
        #         signals=[self._model.pipeline.fft_stage.output])))
        #
        # eeg_inner_dock.dock_area.addDock(PlotDockWidget(
        #     name='Spectogram',
        #     plot=SpectogramPlotWidget(
        #         signals=[self._model.pipeline.fft_stage.output])))

