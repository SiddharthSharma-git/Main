"""
Report Generator Module
Handles test report generation and management
"""
import os
from datetime import datetime
from typing import Dict, List
from util.logger import Logger
from util.common_utils import CommonUtils


class ReportGenerator:
    """Generate and manage test reports"""
    
    logger = Logger.get_logger(__name__)
    
    def __init__(self):
        """Initialize Report Generator"""
        self.project_root = CommonUtils.get_project_root()
        self.reports_dir = os.path.join(self.project_root, "test_reports")
        CommonUtils.create_directory(self.reports_dir)
    
    def get_html_report_path(self) -> str:
        """
        Get path for HTML report
        
        Returns:
            str: HTML report path
        """
        timestamp = CommonUtils.get_timestamp()
        report_path = os.path.join(
            self.reports_dir, 
            f"test_report_{timestamp}.html"
        )
        self.logger.info(f"HTML report will be saved to: {report_path}")
        return report_path
    
    def get_allure_report_dir(self) -> str:
        """
        Get directory for Allure report results
        
        Returns:
            str: Allure report directory
        """
        allure_dir = os.path.join(self.reports_dir, "allure_results")
        CommonUtils.create_directory(allure_dir)
        self.logger.info(f"Allure results directory: {allure_dir}")
        return allure_dir
    
    def generate_summary_report(self, test_results: Dict) -> str:
        """
        Generate summary report
        
        Args:
            test_results: Dictionary containing test results
            
        Returns:
            str: Path to generated report
        """
        self.logger.info("Generating summary report")
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total_tests = test_results.get('total', 0)
        passed = test_results.get('passed', 0)
        failed = test_results.get('failed', 0)
        skipped = test_results.get('skipped', 0)
        
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        summary = f"""
        ================================================
        TEST EXECUTION SUMMARY
        ================================================
        Execution Time: {timestamp}
        ------------------------------------------------
        Total Tests:    {total_tests}
        Passed:         {passed}
        Failed:         {failed}
        Skipped:        {skipped}
        Pass Rate:      {pass_rate:.2f}%
        ================================================
        """
        
        print(summary)
        
        # Save summary to file
        summary_file = os.path.join(
            self.reports_dir, 
            f"summary_{CommonUtils.get_timestamp()}.txt"
        )
        
        with open(summary_file, 'w') as f:
            f.write(summary)
        
        self.logger.info(f"Summary report saved to: {summary_file}")
        return summary_file
    
    def cleanup_old_reports(self, days: int = 7):
        """
        Clean up old report files
        
        Args:
            days: Number of days to keep reports
        """
        self.logger.info(f"Cleaning up reports older than {days} days")
        current_time = datetime.now().timestamp()
        
        for filename in os.listdir(self.reports_dir):
            file_path = os.path.join(self.reports_dir, filename)
            if os.path.isfile(file_path):
                file_modified_time = os.path.getmtime(file_path)
                days_old = (current_time - file_modified_time) / (24 * 3600)
                
                if days_old > days:
                    os.remove(file_path)
                    self.logger.info(f"Removed old report: {filename}")

