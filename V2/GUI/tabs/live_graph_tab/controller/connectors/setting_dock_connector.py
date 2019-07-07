class SettingDockConnector:
    def __init__(self, view):
        self.view = view

        self.settings_dock = self.view.eeg_dock.settings_dock

    def connect(self):
        self._connect_vertical_axis()
        self._connect_horizontal_axis()

    def _connect_vertical_axis(self):
        # v axis
        for ch in range(8):
            scale_v_axis = self.view.eeg_dock.eeg_plots_dock.plot_docks[ch].scroll_plot.scale_y_axis
            self.settings_dock.vertical_scale_cb.connect_cb(scale_v_axis)

    def _connect_horizontal_axis(self):
        self.settings_dock.horizontal_scale_cb.connect_cb(self._print_shit)

    def _print_shit(self, txt):
        print(txt)

