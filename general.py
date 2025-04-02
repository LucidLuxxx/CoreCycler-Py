import configparser
import os
import sys
import shutil  # Add this import
from PyQt6 import QtWidgets

def load_general_config(ui):
    """Load settings from config.ini and update the GUI elements for the [General] section."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Check if the [General] section exists
    if 'General' in config:
        general = config['General']
        
        # Stress Test Program (Radio Buttons)
        stresstestprogram = general.get('stresstestprogram', '').upper()
        if stresstestprogram == 'PRIME95':
            ui.general_stressTestProgram_radioButton_prime95.setChecked(True)
        elif stresstestprogram == 'LINPACK':
            ui.general_stressTestProgram_radioButton_linpack.setChecked(True)
        elif stresstestprogram == 'AIDA64':
            ui.general_stressTestProgram_radioButton_aida64.setChecked(True)
        elif stresstestprogram == 'YCRUNCHER':
            ui.general_stressTestProgram_radioButton_ycruncher.setChecked(True)
        elif stresstestprogram == 'YCRUNCHER_OLD':
            ui.general_stressTestProgram_radioButton_ycruncher_old.setChecked(True)
        else:
            ui.general_stressTestProgram_radioButton_prime95.setChecked(True)  # Default
        
        # Checkboxes (Boolean settings)
        ui.general_stopOnError_checkBox.setChecked(general.get('stoponerror', '0') == '1')
        ui.general_assignBothVirtualCoresForSingleThread_checkBox.setChecked(
            general.get('assignbothvirtualcoresforsinglethread', '0') == '1')
        ui.general_skipCoreOnError_checkBox.setChecked(general.get('skipcoreonerror', '0') == '1')
        ui.general_restartTestProgramForEachCore_checkBox.setChecked(
            general.get('restarttestprogramforeachcore', '0') == '1')
        ui.general_suspendPeriodically_checkBox.setChecked(general.get('suspendperiodically', '0') == '1')
        ui.general_lookForWheaErros_checkBox.setChecked(general.get('lookforwheaerrors', '0') == '1')
        ui.general_treatWheaWarningAsError_checkBox.setChecked(
            general.get('treatwheawarningaserror', '0') == '1')
        ui.general_beepOnError_checkBox.setChecked(general.get('beeponerror', '0') == '1')
        ui.general_flashOnError_checkBox.setChecked(general.get('flashonerror', '0') == '1')
        
        # Use Config File (Checkbox and Line Edit)
        useconfigfile = general.get('useconfigfile', '')
        if useconfigfile:
            ui.general_useConfigFile_checkBox.setChecked(True)
            ui.general_useConfigFile_lineEdit.setText(useconfigfile)
        else:
            ui.general_useConfigFile_checkBox.setChecked(False)
            ui.general_useConfigFile_lineEdit.clear()
        
        # Core Test Order (Combobox and Line Edit)
        coretestorder = general.get('coretestorder', 'Default')
        predefined_orders = ['Default', 'Alternate', 'Random', 'Sequential', 'Custom']  # Fixed typo: removed space in ' Default'
        if coretestorder in predefined_orders:
            ui.general_coreTestOrder_comboBox.setCurrentText(coretestorder)
            if coretestorder == 'Custom':
                ui.general_coreTestOrder_lineEdit.setText(general.get('coretestorder', ''))
            else:
                ui.general_coreTestOrder_lineEdit.clear()
        else:
            ui.general_coreTestOrder_comboBox.setCurrentText('Custom')
            ui.general_coreTestOrder_lineEdit.setText(coretestorder)
        
        # Spinboxes (Integer settings)
        try:
            ui.general_maxIterations_spinBox.setValue(int(general.get('maxiterations', '1')))
            ui.general_delayBetweenCores_spinBox.setValue(int(general.get('delaybetweencores', '15')))
            ui.general_numberOfThreads_spinBox.setValue(int(general.get('numberofthreads', '1')))
        except ValueError:
            # Set defaults if conversion fails
            ui.general_maxIterations_spinBox.setValue(1)
            ui.general_delayBetweenCores_spinBox.setValue(15)
            ui.general_numberOfThreads_spinBox.setValue(1)
        
        # Cores to Ignore (Line Edit)
        ui.general_coresToIgnore_lineEdit.setText(general.get('corestoignore', ''))
        
        # Runtime Per Core (Checkbox and Line Edit)
        runtime_per_core = general.get('runtimepercore', 'Auto')
        if runtime_per_core.strip().lower() == 'auto':
            ui.general_runtimePerCore_checkBox_auto.setChecked(True)
            ui.general_runtimePerCore_lineEdit.setText('')
        else:
            ui.general_runtimePerCore_checkBox_auto.setChecked(False)
            ui.general_runtimePerCore_lineEdit.setText(runtime_per_core)
    else:
        # If [General] section is missing, apply default GUI settings
        ui.general_stressTestProgram_radioButton_prime95.setChecked(True)
        ui.general_stopOnError_checkBox.setChecked(False)
        ui.general_runtimePerCore_checkBox_auto.setChecked(True)
        ui.general_runtimePerCore_lineEdit.setText('')

def apply_general_config(ui):
    """Update the [General] section in config.ini based on current GUI settings."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Ensure the [General] section exists
    if 'General' not in config:
        config['General'] = {}
    general = config['General']
    
    # Stress Test Program (Radio Buttons)
    if ui.general_stressTestProgram_radioButton_prime95.isChecked():
        general['stresstestprogram'] = 'PRIME95'
    elif ui.general_stressTestProgram_radioButton_linpack.isChecked():
        general['stresstestprogram'] = 'LINPACK'
    elif ui.general_stressTestProgram_radioButton_aida64.isChecked():
        general['stresstestprogram'] = 'AIDA64'
    elif ui.general_stressTestProgram_radioButton_ycruncher.isChecked():
        general['stresstestprogram'] = 'YCRUNCHER'
    elif ui.general_stressTestProgram_radioButton_ycruncher_old.isChecked():
        general['stresstestprogram'] = 'YCRUNCHER_OLD'
    
    # Checkboxes (Boolean settings)
    general['stoponerror'] = '1' if ui.general_stopOnError_checkBox.isChecked() else '0'
    general['assignbothvirtualcoresforsinglethread'] = '1' if ui.general_assignBothVirtualCoresForSingleThread_checkBox.isChecked() else '0'
    general['skipcoreonerror'] = '1' if ui.general_skipCoreOnError_checkBox.isChecked() else '0'
    general['restarttestprogramforeachcore'] = '1' if ui.general_restartTestProgramForEachCore_checkBox.isChecked() else '0'
    general['suspendperiodically'] = '1' if ui.general_suspendPeriodically_checkBox.isChecked() else '0'
    general['lookforwheaerrors'] = '1' if ui.general_lookForWheaErros_checkBox.isChecked() else '0'
    general['treatwheawarningaserror'] = '1' if ui.general_treatWheaWarningAsError_checkBox.isChecked() else '0'
    general['beeponerror'] = '1' if ui.general_beepOnError_checkBox.isChecked() else '0'
    general['flashonerror'] = '1' if ui.general_flashOnError_checkBox.isChecked() else '0'
    
    # Use Config File (Checkbox and Line Edit)
    if ui.general_useConfigFile_checkBox.isChecked():
        general['useconfigfile'] = ui.general_useConfigFile_lineEdit.text()
    else:
        general['useconfigfile'] = ''
    
    # Core Test Order (Combobox and Line Edit)
    if ui.general_coreTestOrder_comboBox.currentText() == 'Custom':
        general['coretestorder'] = ui.general_coreTestOrder_lineEdit.text()
    else:
        general['coretestorder'] = ui.general_coreTestOrder_comboBox.currentText()
    
    # Spinboxes (Integer settings)
    general['maxiterations'] = str(ui.general_maxIterations_spinBox.value())
    general['delaybetweencores'] = str(ui.general_delayBetweenCores_spinBox.value())
    general['numberofthreads'] = str(ui.general_numberOfThreads_spinBox.value())
    
    # Cores to Ignore (Line Edit)
    general['corestoignore'] = ui.general_coresToIgnore_lineEdit.text()
    
    # Runtime Per Core (Checkbox and Line Edit)
    if ui.general_runtimePerCore_checkBox_auto.isChecked():
        general['runtimepercore'] = 'Auto'
    else:
        general['runtimepercore'] = ui.general_runtimePerCore_lineEdit.text().strip()
    
    # Write the updated configuration back to config.ini
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def launch_configs_folder():
    """Open the configs folder in Windows Explorer from the base directory."""
    try:
        # Determine the base directory: script dir if uncompiled, exe dir if compiled
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)  # Compiled .exe directory
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Script directory
        
        configs_path = os.path.join(base_dir, 'configs')
        os.startfile(configs_path)
    except Exception as e:
        print(f"Error opening configs folder: {e}")

def save_config_to_file(ui):
    """Save the current config.ini settings to a new file in the configs folder."""
    try:
        # Determine the base directory: script dir if uncompiled, exe dir if compiled
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)  # Compiled .exe directory
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))  # Script directory
        
        print(f"Base directory: {base_dir}")  # Debug output
        
        # Define the source config file path
        source_config = os.path.join(base_dir, 'config.ini')
        print(f"Source config path: {source_config}")  # Debug output
        
        # Ensure the configs folder exists
        configs_dir = os.path.join(base_dir, 'configs')
        if not os.path.exists(configs_dir):
            os.makedirs(configs_dir)
            print(f"Created configs directory: {configs_dir}")  # Debug output
        
        # Prompt the user for a file name
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            ui.centralwidget,  # Parent widget
            "Save Config File",
            configs_dir,  # Default directory
            "Config Files (*.ini);;All Files (*)"  # File filter
        )
        print(f"Selected file name: {file_name}")  # Debug output
        
        # If the user provided a file name
        if file_name:
            # Ensure the file has a .ini extension
            if not file_name.endswith('.ini'):
                file_name += '.ini'
            
            # Apply the current settings to config.ini first
            apply_general_config(ui)
            print("Applied general config to config.ini")  # Debug output
            
            # Check if source_config exists
            if not os.path.exists(source_config):
                raise FileNotFoundError(f"Source config file not found: {source_config}")
            
            # Copy the updated config.ini to the new location
            shutil.copy2(source_config, file_name)
            print(f"Config saved to: {file_name}")
        else:
            print("Save operation cancelled by user.")
            
    except Exception as e:
        print(f"Error saving config file: {str(e)}")
        # Optionally, show an error message in the GUI
        QtWidgets.QMessageBox.critical(ui.centralwidget, "Error", f"Failed to save config file: {str(e)}")
