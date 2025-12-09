"""
Script to generate data audit report
Run: python generate_audit_report.py
"""
from data_audit import DataAuditor

if __name__ == "__main__":
    print("Generating data audit report...")
    auditor = DataAuditor()
    auditor.load_and_prepare_data()
    auditor.generate_audit_report()
    print("✓ Data audit report generated: data_audit_report.txt")

