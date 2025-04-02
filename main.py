import sys
import os
import shutil
import subprocess
import start
import menu_bar
from PyQt6 import QtWidgets
from mainwindow import Ui_MainWindow
from general import load_general_config, apply_general_config, launch_configs_folder, save_config_to_file, load_all_configs, apply_all_configs
from zentimings import launch_zentimings
from functools import partial
from reset import reset_config
from tools import (
    launch_boost_tester,
    launch_pbo2_tuner,
    launch_intel_voltage_control,
    launch_apic_ids,
    launch_core_tuner_x,
    launch_enable_performance_counters,
    open_helpers_folder
)

if sys.platform == "win32":
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, 0)  # 0 is SW_HIDE

# Set working directory to the .exe's location when compiled
if getattr(sys, 'frozen', False):
    exe_dir = os.path.dirname(sys.executable)
    os.chdir(exe_dir)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    load_all_configs(ui)
    ui.apply_config_pushButton.clicked.connect(lambda: apply_all_configs(ui))
    ui.reset_config_pushButton.clicked.connect(partial(reset_config, ui, load_all_configs))
    ui.saveConfig_pushButton.clicked.connect(lambda: save_config_to_file(ui))
    ui.boostTester_pushButton.clicked.connect(launch_boost_tester)
    ui.pbo2Tuner_pushButton.clicked.connect(launch_pbo2_tuner)
    ui.intelVoltageControl_pushButton.clicked.connect(launch_intel_voltage_control)
    ui.apicIds_pushButton.clicked.connect(launch_apic_ids)
    ui.coreTunerX_pushButton.clicked.connect(launch_core_tuner_x)
    ui.enablePerformanceCounters_pushButton.clicked.connect(launch_enable_performance_counters)
    ui.helpers_pushButton.clicked.connect(open_helpers_folder)
    ui.zenTimings_pushButton.clicked.connect(launch_zentimings)
    menu_bar.setup_menu_connections(ui)
    ui.configsFolder_toolButton.clicked.connect(lambda: launch_configs_folder(ui))
    ui.start_test_pushButton.clicked.connect(lambda: start.run_corecycler(MainWindow))
    
    MainWindow.show()
    sys.exit(app.exec())
