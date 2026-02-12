#!/usr/bin/env python3
"""
generate-summary.py - Generate summary report from test results

Usage:
    python generate-summary.py --model <model-name>
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# ANSI color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'


def load_results(results_dir: Path) -> List[Dict[str, Any]]:
    """Load all JSON result files from results directory"""
    results = []
    for file in results_dir.glob('*.json'):
        with open(file, 'r') as f:
            result = json.load(f)
            result['file'] = file.name
            results.append(result)
    return results


def categorize_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Categorize results by language and status"""
    categorized = {
        'by_language': {},
        'by_status': {'passed': 0, 'failed': 0, 'pending': 0},
        'all_results': results
    }
    
    for result in results:
        language = result.get('language', 'unknown')
        status = result.get('status', 'pending')
        
        # By language
        if language not in categorized['by_language']:
            categorized['by_language'][language] = {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'pending': 0,
                'scenarios': []
            }
        
        categorized['by_language'][language]['total'] += 1
        categorized['by_language'][language][status] += 1
        categorized['by_language'][language]['scenarios'].append(result)
        
        # By status
        categorized['by_status'][status] += 1
    
    return categorized


def _calculate_summary_stats(categorized: Dict[str, Any]) -> Dict[str, Any]:
    """Helper to calculate summary statistics"""
    total_scenarios = len(categorized['all_results'])
    passed = categorized['by_status']['passed']
    failed = categorized['by_status']['failed']
    pending = categorized['by_status']['pending']
    pass_rate = (passed / total_scenarios * 100) if total_scenarios > 0 else 0
    
    total_score = 0
    score_count = 0
    total_doc_fetches = 0
    doc_fetch_count = 0
    
    for result in categorized['all_results']:
        if 'scores' in result and 'total' in result['scores']:
            total_score += result['scores']['total']
            score_count += 1
        
        if 'documentation_fetches' in result:
            doc_fetches = result['documentation_fetches'].get('total_count', 0)
            if doc_fetches > 0:
                total_doc_fetches += doc_fetches
                doc_fetch_count += 1
    
    avg_score = (total_score / score_count) if score_count > 0 else 0
    avg_doc_fetches = (total_doc_fetches / doc_fetch_count) if doc_fetch_count > 0 else 0
    
    return {
        'total_scenarios': total_scenarios,
        'passed': passed,
        'failed': failed,
        'pending': pending,
        'pass_rate': pass_rate,
        'avg_score': avg_score,
        'avg_doc_fetches': avg_doc_fetches
    }


def _generate_failed_scenarios_section(model: str, categorized: Dict[str, Any]) -> List[str]:
    """Helper to generate failed scenarios section"""
    section = []
    section.append("## Failed Scenarios")
    section.append("")
    
    for result in categorized['all_results']:
        if result.get('status') == 'failed':
            scenario_name = result.get('scenario', 'Unknown')
            language = result.get('language', 'unknown')
            score = result.get('scores', {}).get('total', 0)
            
            section.append(f"### {language}/{scenario_name}")
            section.append(f"**Score:** {score}/100")
            section.append("")
            
            # List failures
            validation = result.get('validation', {})
            failures = validation.get('failures', [])
            if failures:
                section.append("**Issues:**")
                for failure in failures:
                    section.append(f"- {failure}")
                section.append("")
            
            section.append(f"**Details:** `results/{model}/{result['file']}`")
            section.append("")
    
    return section


def generate_markdown_report(model: str, categorized: Dict[str, Any], output_file: Path):
    """Generate markdown summary report"""
    
    stats = _calculate_summary_stats(categorized)
    
    # Start building report
    report = []
    report.append("# SonarArchitectLight Test Suite Summary")
    report.append("")
    report.append(f"**Model:** {model}")
    report.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Total Scenarios:** {stats['total_scenarios']}")
    report.append("")
    
    report.append("## Overall Results")
    report.append("")
    report.append(f"- ✅ **Passed:** {stats['passed']} ({stats['pass_rate']:.1f}%)")
    report.append(f"- ❌ **Failed:** {stats['failed']} ({(stats['failed']/stats['total_scenarios']*100) if stats['total_scenarios'] > 0 else 0:.1f}%)")
    if stats['pending'] > 0:
        report.append(f"- ⏳ **Pending:** {stats['pending']}")
    report.append(f"- 📊 **Average Score:** {stats['avg_score']:.1f}/100")
    if stats['avg_doc_fetches'] > 0:
        report.append(f"- 📚 **Avg Documentation Fetches:** {stats['avg_doc_fetches']:.1f} pages/scenario")
    report.append("")
    
    report.append("---")
    report.append("")
    report.append("## Results by Language")
    report.append("")
    
    # Table header
    report.append("| Language | Total | Passed | Failed | Pass Rate |")
    report.append("|----------|-------|--------|--------|-----------|")
    
    for language, data in sorted(categorized['by_language'].items()):
        lang_pass_rate = (data['passed'] / data['total'] * 100) if data['total'] > 0 else 0
        status_icon = "✓" if data['failed'] == 0 else "✗"
        report.append(f"| {language.capitalize()} | {data['total']} | {data['passed']} | {data['failed']} | {lang_pass_rate:.1f}% {status_icon} |")
    
    report.append("")
    report.append("---")
    report.append("")
    
    # Failed scenarios detail
    if stats['failed'] > 0:
        report.extend(_generate_failed_scenarios_section(model, categorized))
    
    report.append("---")
    report.append("")
    
    # Score breakdown
    report.append("## Score Breakdown")
    report.append("")
    report.append("| Scenario | Accuracy | Security | Efficiency | Currency | Usability | Total | Doc Fetches |")
    report.append("|---------|---------|---------|-----------|---------|-----------|------|-------------|")
    
    for result in sorted(categorized['all_results'], key=lambda x: x.get('scores', {}).get('total', 0), reverse=True):
        scenario = f"{result.get('language', 'unknown')}/{result.get('scenario', 'unknown')}"
        scores = result.get('scores', {})
        doc_fetches = result.get('documentation_fetches', {}).get('total_count', 0)
        
        report.append(
            f"| {scenario} | "
            f"{scores.get('accuracy', 0)}/40 | "
            f"{scores.get('security', 0)}/20 | "
            f"{scores.get('efficiency', 0)}/15 | "
            f"{scores.get('currency', 0)}/15 | "
            f"{scores.get('usability', 0)}/10 | "
            f"{scores.get('total', 0)}/100 | "
            f"{doc_fetches} |"
        )
    
    report.append("")
    
    # Recommendations
    report.append("---")
    report.append("")
    report.append("## Recommendations")
    report.append("")
    
    if stats['pass_rate'] >= 95:
        report.append("✅ **Excellent:** Model performs very well across all scenarios.")
    elif stats['pass_rate'] >= 80:
        report.append("⚠️ **Good:** Model performs well but has some areas for improvement.")
    elif stats['pass_rate'] >= 60:
        report.append("⚠️ **Fair:** Model needs improvement in several areas.")
    else:
        report.append("❌ **Poor:** Model requires significant improvements.")
    
    report.append("")
    
    # Write report
    with open(output_file, 'w') as f:
        f.write('\n'.join(report))


def generate_console_summary(model: str, categorized: Dict[str, Any]):
    """Print summary to console"""
    
    total_scenarios = len(categorized['all_results'])
    passed = categorized['by_status']['passed']
    failed = categorized['by_status']['failed']
    pending = categorized['by_status']['pending']
    
    pass_rate = (passed / total_scenarios * 100) if total_scenarios > 0 else 0
    
    print("\n" + "=" * 77)
    print(f"{BLUE}Test Suite Summary Report{NC}")
    print("=" * 77)
    print(f"\n{BLUE}Model:{NC} {model}")
    print(f"{BLUE}Date:{NC} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{BLUE}Total Scenarios:{NC} {total_scenarios}")
    print(f"{GREEN}Passed:{NC} {passed} ({pass_rate:.1f}%)")
    print(f"{RED}Failed:{NC} {failed} ({(failed/total_scenarios*100) if total_scenarios > 0 else 0:.1f}%)")
    
    if pending > 0:
        print(f"{YELLOW}Pending:{NC} {pending}")
    
    print("\n" + "=" * 77)
    print("Results by Category")
    print("=" * 77 + "\n")
    
    for language, data in sorted(categorized['by_language'].items()):
        lang_pass_rate = (data['passed'] / data['total'] * 100) if data['total'] > 0 else 0
        status = f"{GREEN}✓ {lang_pass_rate:.1f}%{NC}" if data['failed'] == 0 else f"{RED}✗ {lang_pass_rate:.1f}%{NC}"
        print(f"{language.capitalize():15} {data['passed']}/{data['total']:2}   {status}")
    
    if failed > 0:
        print("\n" + "=" * 77)
        print("Failed Scenarios")
        print("=" * 77 + "\n")
        
        for result in categorized['all_results']:
            if result.get('status') == 'failed':
                scenario = f"{result.get('language')}/{result.get('scenario')}"
                score = result.get('scores', {}).get('total', 0)
                print(f"{RED}✗{NC} {scenario:45} Score: {score}/100")
        
        print(f"\n{YELLOW}View details:{NC} tests/results/{model}/")
    
    print("\n" + "=" * 77 + "\n")


def main():
    parser = argparse.ArgumentParser(description='Generate test summary report')
    parser.add_argument('--model', required=True, help='Model name')
    parser.add_argument('--results-dir', help='Path to results directory')
    parser.add_argument('--output', help='Output markdown file path')
    
    args = parser.parse_args()
    
    # Determine results directory
    if args.results_dir:
        results_dir = Path(args.results_dir)
    else:
        script_dir = Path(__file__).parent
        tests_dir = script_dir.parent
        results_dir = tests_dir / 'results' / args.model
    
    if not results_dir.exists():
        print(f"{RED}Error: Results directory not found: {results_dir}{NC}")
        sys.exit(1)
    
    # Load results
    results = load_results(results_dir)
    
    if not results:
        print(f"{YELLOW}Warning: No results found in {results_dir}{NC}")
        sys.exit(0)
    
    # Categorize results
    categorized = categorize_results(results)
    
    # Generate console summary
    generate_console_summary(args.model, categorized)
    
    # Generate markdown report
    output_file = Path(args.output) if args.output else results_dir / 'summary.md'
    generate_markdown_report(args.model, categorized, output_file)
    
    print(f"{GREEN}✓{NC} Summary report generated: {output_file}\n")


if __name__ == '__main__':
    main()
