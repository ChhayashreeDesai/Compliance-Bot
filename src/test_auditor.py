"""
ADVANCED TESTING AND BATCH AUDIT SCRIPT
DPDP Act 2025 Compliance Auditor

This script allows you to:
1. Test multiple URLs in batch
2. Generate comprehensive reports
3. Export results to CSV
4. Schedule audits
"""

import csv
from datetime import datetime
from dpdp_auditor import DPDP_Auditor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BatchAuditor:
    """Run audits on multiple URLs and generate reports"""
    
    def __init__(self):
        self.results = []
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    def audit_single_url(self, url: str) -> dict:
        """Audit a single URL"""
        print(f"\n{'='*70}")
        print(f"Auditing: {url}")
        print(f"{'='*70}")
        
        try:
            auditor = DPDP_Auditor(url)
            report = auditor.run_audit()
            
            # Extract summary
            summary = {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'module_1': self._get_status(report, 'module_1'),
                'module_2': self._get_status(report, 'module_2'),
                'module_3': self._get_status(report, 'module_3'),
                'module_4': self._get_status(report, 'module_4'),
                'violations': self._count_status(report, 'VIOLATION'),
                'risks': self._count_status(report, 'RISK'),
                'passed': self._count_status(report, 'PASS'),
            }
            
            self.results.append(summary)
            return summary
            
        except Exception as e:
            logger.error(f"Error auditing {url}: {str(e)}")
            summary = {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
            self.results.append(summary)
            return summary
    
    def audit_batch(self, urls: list) -> list:
        """Audit multiple URLs"""
        for url in urls:
            self.audit_single_url(url)
        return self.results
    
    def export_to_csv(self, filename: str = None) -> str:
        """Export results to CSV file"""
        if filename is None:
            filename = f"audit_report_{self.timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                if not self.results:
                    logger.warning("No results to export")
                    return filename
                
                fieldnames = self.results[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(self.results)
                
                logger.info(f"Report exported to: {filename}")
                return filename
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            return None
    
    def _get_status(self, report: dict, module: str) -> str:
        """Get primary status for a module"""
        findings = report.get(module, [])
        if findings:
            return findings[0].get('status', 'UNKNOWN')
        return 'UNKNOWN'
    
    def _count_status(self, report: dict, status: str) -> int:
        """Count occurrences of a status across all modules"""
        count = 0
        for module_findings in report.values():
            for finding in module_findings:
                if finding.get('status') == status:
                    count += 1
        return count
    
    def print_summary(self) -> None:
        """Print summary of all audits"""
        print(f"\n{'='*70}")
        print(f"BATCH AUDIT SUMMARY")
        print(f"{'='*70}")
        print(f"Total URLs Audited: {len(self.results)}")
        print(f"Timestamp: {self.timestamp}")
        print(f"\n{'URL':<40} {'Violations':<15} {'Risks':<15} {'Passed':<10}")
        print("-" * 70)
        
        for result in self.results:
            if 'error' not in result:
                print(f"{result['url']:<40} {result['violations']:<15} {result['risks']:<15} {result['passed']:<10}")
            else:
                print(f"{result['url']:<40} {'ERROR':<15}")
        
        print("=" * 70)


def test_urls_list():
    """Test with a predefined list of URLs"""
    test_urls = [
        "https://google.com",
        "https://example.com",
        # Add more URLs here
    ]
    
    batch_auditor = BatchAuditor()
    print("Starting batch audit...")
    batch_auditor.audit_batch(test_urls)
    batch_auditor.print_summary()
    batch_auditor.export_to_csv()


def interactive_batch_audit():
    """Interactive batch audit"""
    print("\n" + "="*70)
    print("BATCH AUDIT MODE")
    print("="*70)
    
    urls = []
    print("Enter URLs to audit (one per line, empty line to finish):")
    
    while True:
        url = input("> ").strip()
        if not url:
            if urls:
                break
            else:
                print("Please enter at least one URL")
                continue
        urls.append(url)
    
    batch_auditor = BatchAuditor()
    print(f"\nAuditing {len(urls)} URLs...")
    batch_auditor.audit_batch(urls)
    batch_auditor.print_summary()
    
    # Export option
    export = input("\nExport results to CSV? (y/n): ").lower()
    if export == 'y':
        filename = batch_auditor.export_to_csv()
        print(f"✓ Results saved to: {filename}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--batch':
            interactive_batch_audit()
        else:
            print("Usage: python test_auditor.py [--batch]")
    else:
        test_urls_list()
