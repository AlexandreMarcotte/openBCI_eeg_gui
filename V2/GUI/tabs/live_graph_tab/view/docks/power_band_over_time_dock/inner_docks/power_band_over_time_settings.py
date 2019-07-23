# -- My Packages --
from V2.GUI.tabs.live_graph_tab.view.docks.inner_docks.settings_dock import SettingsDock


# TODO: ALEXM: create a generalSettings class instead of this generic one that
# I use for many of the dock of fft
class PowerBandOverTimeSettings(SettingsDock):
    def __init__(self, main_layout):
        super().__init__(main_layout)
        self.main_layout = main_layout
        self._create_settings_dock()

    def _create_settings_dock(self):
        super()._create_settings_dock()
        self._create_all_combobox()

    def _create_all_combobox(self):
        self.create_choose_channel_cb()
