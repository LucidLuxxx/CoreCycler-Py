import configparser
import sys
import os
import shutil
import subprocess
import start
import menu_bar
from PyQt6 import QtWidgets, QtCore
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

# Add the new function here, after imports and before main block
def handle_config_file_checkbox(ui, state):
    if state == QtCore.Qt.CheckState.Unchecked.value:
        # Clear the line edit and refresh GUI with current config.ini
        ui.general_useConfigFile_lineEdit.clear()
        apply_all_configs(ui)  # Ensure current GUI settings are saved
        load_all_configs(ui)   # Refresh GUI with config.ini
    elif state == QtCore.Qt.CheckState.Checked.value and ui.general_useConfigFile_lineEdit.text():
        # User manually checked it with text entered
        base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, 'config.ini')
        custom_config_path = os.path.join(base_dir, ui.general_useConfigFile_lineEdit.text())
        
        if os.path.exists(custom_config_path):
            # Load default.config.ini as base
            default_config_path = os.path.join(base_dir, 'configs', 'default.config.ini')
            if os.path.exists(default_config_path):
                shutil.copyfile(default_config_path, config_path)
            else:
                QtWidgets.QMessageBox.warning(None, "Warning", f"Default config file not found at {default_config_path}.")
                return
            
            # Overlay custom config
            custom_config = configparser.ConfigParser()
            custom_config.read(custom_config_path)
            main_config = configparser.ConfigParser()
            main_config.read(config_path)
            
            for section in custom_config.sections():
                if section not in main_config:
                    main_config[section] = {}
                for key, value in custom_config[section].items():
                    main_config[section][key] = value
            
            # Do NOT set useconfigfile in config.ini
            # Removed: main_config['General']['useconfigfile'] = ui.general_useConfigFile_lineEdit.text()
            
            with open(config_path, 'w') as configfile:
                main_config.write(configfile)
            
            load_all_configs(ui)
        else:
            QtWidgets.QMessageBox.warning(None, "Warning", f"Config file not found at {custom_config_path}.")
            

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
