"""
Common Utilities Module
Contains common helper functions used across the framework
"""
import os
import json
import yaml
from datetime import datetime
from typing import Dict, Any
from util.logger import Logger


class CommonUtils:
    """Common utility functions"""
    
    logger = Logger.get_logger(__name__)
    
    @staticmethod
    def read_json_file(file_path: str) -> Dict[str, Any]:
        """
        Read JSON file
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            dict: JSON data
        """
        CommonUtils.logger.info(f"Reading JSON file: {file_path}")
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            CommonUtils.logger.error(f"Error reading JSON file: {str(e)}")
            raise
    
    @staticmethod
    def read_yaml_file(file_path: str) -> Dict[str, Any]:
        """
        Read YAML file
        
        Args:
            file_path: Path to YAML file
            
        Returns:
            dict: YAML data
        """
        CommonUtils.logger.info(f"Reading YAML file: {file_path}")
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            CommonUtils.logger.error(f"Error reading YAML file: {str(e)}")
            raise
    
    @staticmethod
    def write_json_file(file_path: str, data: Dict[str, Any]):
        """
        Write data to JSON file
        
        Args:
            file_path: Path to JSON file
            data: Data to write
        """
        CommonUtils.logger.info(f"Writing JSON file: {file_path}")
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            CommonUtils.logger.error(f"Error writing JSON file: {str(e)}")
            raise
    
    @staticmethod
    def get_timestamp() -> str:
        """
        Get current timestamp
        
        Returns:
            str: Formatted timestamp
        """
        return datetime.now().strftime('%Y%m%d_%H%M%S')
    
    @staticmethod
    def create_directory(directory_path: str):
        """
        Create directory if it doesn't exist
        
        Args:
            directory_path: Path to directory
        """
        if not os.path.exists(directory_path):
            CommonUtils.logger.info(f"Creating directory: {directory_path}")
            os.makedirs(directory_path)
    
    @staticmethod
    def get_project_root() -> str:
        """
        Get project root directory
        
        Returns:
            str: Project root path
        """
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    @staticmethod
    def wait_for_condition(condition_func, timeout: int = 30, poll_interval: float = 0.5) -> bool:
        """
        Wait for a condition to be true
        
        Args:
            condition_func: Function that returns boolean
            timeout: Maximum wait time in seconds
            poll_interval: Time between checks in seconds
            
        Returns:
            bool: True if condition met, False if timeout
        """
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if condition_func():
                return True
            time.sleep(poll_interval)
        
        return False

