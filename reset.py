import os
import shutil
import subprocess
import sys
from PyQt6 import QtWidgets

def reset_config():
    reply = QtWidgets.QMessageBox.question(
        None,
        "Confirm Reset",
        "Are you sure you want to reset to default settings?",
        QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
        QtWidgets.QMessageBox.StandardButton.No
    )
    if reply == QtWidgets.QMessageBox.StandardButton.Yes:
        working_dir = os.getcwd()
        default_config_path = os.path.join(working_dir, 'configs', 'default.config.ini')
        config_path = os.path.join(working_dir, 'config.ini')
        
        if not os.path.exists(default_config_path):
            QtWidgets.QMessageBox.warning(
                None,
                "Warning",
                f"Default config file not found at {default_config_path}."
            )
            return
        
        try:
            shutil.copyfile(default_config_path, config_path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                None,
                "Error",
                f"Failed to copy default config: {e}"
            )
            return
        
        try:
            # Restart the application based on whether it's frozen or a script
            if getattr(sys, 'frozen', False):
                # Frozen executable: run the executable
                subprocess.Popen([sys.executable], cwd=working_dir)
            else:
                # Python script: run the interpreter with the current script
                subprocess.Popen([sys.executable, sys.argv[0]], cwd=working_dir)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                None,
                "Error",
                f"Failed to restart application: {e}"
            )
            return
        
        QtWidgets.QApplication.quit()
