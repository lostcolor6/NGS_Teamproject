"""
SettingsManager class for managing application settings.

This class provides a way to save and load application settings to and from a configuration file.
"""

from PyQt5.QtCore import QSettings
import os


class SettingsManager:
    """
    A manager for application settings.

    Attributes:
        settings (QSettings): The QSettings instance for storing and retrieving settings.
    """
    def __init__(self, settings_file="gui.ini"):
        # Get the absolute path to the project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))

        # Construct the full path to the ini file
        settings_path = os.path.join(project_root, "config", settings_file)

        self.settings = QSettings(settings_path, QSettings.IniFormat)

        api_settings_file="API.ini"
        api_settings_path = os.path.join(project_root, "config", api_settings_file)
        self.api_settings = QSettings(api_settings_path, QSettings.IniFormat)

    def save_setting(self, key, value):
        """
        Saves a setting to the configuration file.

        Args:
            key (str): The key for the setting.
            value: The value to be saved.
        """
        self.settings.setValue("gui/" + key, value)

    def load_setting(self, key, default_value=None, value_type=None):
        """
        Loads a setting from the configuration file.

        Args:
            key (str): The key for the setting.
            default_value: The default value to return if the setting is not found.
            value_type: The type of the value to be loaded.

        Returns:
            The loaded value or the default value if not found.
        """
        if value_type:
            return self.settings.value("gui/" + key, default_value, type=value_type)
        return self.settings.value("gui/" + key, default_value)


    def load_infoAPI(self, key, default_value=None, value_type=None):
        if value_type:
            return self.api_settings.value("api/" + key, default_value, type=value_type)
        return self.api_settings.value("api/" + key, default_value)
