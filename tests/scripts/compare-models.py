#!/usr/bin/env python3
"""
compare-models.py - Compare test results across different LLM models

Usage:
    python compare-models.py --models claude-sonnet-4,gpt-4-turbo,gemini-pro-2
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
MAGENTA = '\033[0;35m'
NC = '\033[0m'


def load_model_results(results_base_dir: Path, model: str) -> Dict[str, Any]:
    """Load all results for a specific model"""
    model_dir = results_base_dir / model
    
    if not model_dir.exists():
        return {'model': model, 'results': [], 'exists': False}
    
    results = []
    for file in model_dir.glob('*.json'):
        if file.name != 'summary.md':
            with open(file, 'r') as f:
                result = json.load(f)
                result['file'] = file.name
                results.append(result)
    
    return {
        'model': model,
        'results': results,
        'exists': True
    }


def calculate_model_stats(model_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate statistics for a model"""
    results = model_data['results']
    
    if not results:
        return {
            'total_scenarios': 0,
            'passed': 0,
            'failed': 0,
            'pass_rate': 0,
            'avg_score': 0,
            'avg_accuracy': 0,
            'avg_security': 0,
            'avg_efficiency': 0,
            'avg_currency': 0,
            'avg_usability': 0,
            'total_tokens': 0,
            'avg_tokens': 0,
            'total_cost': 0.0
        }
    
    total = len(results)
    passed = sum(1 for r in results if r.get('status') == 'passed')
    failed = sum(1 for r in results if r.get('status') == 'failed')
    
    scores = [r.get('scores', {}) for r in results]
    
    return {
        'total_scenarios': total,
        'passed': passed,
        'failed': failed,
        'pass_rate': (passed / total * 100) if total > 0 else 0,
        'avg_score': sum(s.get('total', 0) for s in scores) / total if total > 0 else 0,
        'avg_accuracy': sum(s.get('accuracy', 0) for s in scores) / total if total > 0 else 0,
        'avg_security': sum(s.get('security', 0) for s in scores) / total if total > 0 else 0,
        'avg_efficiency': sum(s.get('efficiency', 0) for s in scores) / total if total > 0 else 0,
        'avg_currency': sum(s.get('currency', 0) for s in scores) / total if total > 0 else 0,
        'avg_usability': sum(s.get('usability', 0) for s in scores) / total if total > 0 else 0,
        'total_tokens': sum(r.get('execution', {}).get('total_tokens', 0) for r in results),
        'avg_tokens': sum(r.get('execution', {}).get('total_tokens', 0) for r in results) / total if total > 0 else 0,
        'total_cost': sum(r.get('execution', {}).get('cost', 0) for r in results),
        'total_doc_fetches': sum(r.get('documentation_fetches', {}).get('total_count', 0) for r in results),
        'avg_doc_fetches': sum(r.get('documentation_fetches', {}).get('total_count', 0) for r in results) / total if total > 0 else 0
    }


def generate_comparison_table(models_data: List[Dict[str, Any]]) -> str:
    """Generate comparison table"""
    lines = []
    
    lines.append("| Model | Scenarios | Passed | Failed | Pass Rate | Avg Score | Accuracy | Security | Efficiency | Currency | Usability | Avg Docs |")
    lines.append("|-------|-----------|--------|--------|-----------|-----------|----------|----------|------------|----------|-----------|----------|")
    
    for model_data in models_data:
        stats = calculate_model_stats(model_data)
        model = model_data['model']
        
        lines.append(
            f"| {model} | "
            f"{stats['total_scenarios']} | "
            f"{stats['passed']} | "
            f"{stats['failed']} | "
            f"{stats['pass_rate']:.1f}% | "
            f"{stats['avg_score']:.1f}/100 | "
            f"{stats['avg_accuracy']:.1f}/40 | "
            f"{stats['avg_security']:.1f}/20 | "
            f"{stats['avg_efficiency']:.1f}/15 | "
            f"{stats['avg_currency']:.1f}/15 | "
            f"{stats['avg_usability']:.1f}/10 | "
            f"{stats['avg_doc_fetches']:.1f} |"
        )
    
    return '\n'.join(lines)


def generate_comparison_report(models_data: List[Dict[str, Any]], output_file: Path):
    """Generate detailed comparison report in markdown"""
    
    report = []
    report.append("# LLM Model Comparison for SonarArchitectLight")
    report.append("")
    report.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Models Compared:** {', '.join([m['model'] for m in models_data])}")
    report.append("")
    
    report.append("## Overall Comparison")
    report.append("")
    report.append(generate_comparison_table(models_data))
    report.append("")
    
    # Best in category
    report.append("---")
    report.append("")
    report.append("## Best in Category")
    report.append("")
    
    all_stats = [(m['model'], calculate_model_stats(m)) for m in models_data]
    
    best_pass_rate = max(all_stats, key=lambda x: x[1]['pass_rate'])
    best_score = max(all_stats, key=lambda x: x[1]['avg_score'])
    best_security = max(all_stats, key=lambda x: x[1]['avg_security'])
    best_efficiency = max(all_stats, key=lambda x: x[1]['avg_efficiency'])
    
    report.append(f"- 🏆 **Best Pass Rate:** {best_pass_rate[0]} ({best_pass_rate[1]['pass_rate']:.1f}%)")
    report.append(f"- 🏆 **Best Average Score:** {best_score[0]} ({best_score[1]['avg_score']:.1f}/100)")
    report.append(f"- 🔒 **Best Security:** {best_security[0]} ({best_security[1]['avg_security']:.1f}/20)")
    report.append(f"- ⚡ **Best Efficiency:** {best_efficiency[0]} ({best_efficiency[1]['avg_efficiency']:.1f}/15)")
    report.append("")
    
    # Performance breakdown
    report.append("---")
    report.append("")
    report.append("## Detailed Performance Breakdown")
    report.append("")
    
    for model_data in models_data:
        model = model_data['model']
        stats = calculate_model_stats(model_data)
        
        report.append(f"### {model}")
        report.append("")
        report.append(f"**Overall Performance:**")
        report.append(f"- Scenarios: {stats['total_scenarios']}")
        report.append(f"- Pass Rate: {stats['pass_rate']:.1f}%")
        report.append(f"- Average Score: {stats['avg_score']:.1f}/100")
        report.append("")
        
        report.append(f"**Score Breakdown:**")
        report.append(f"- Accuracy: {stats['avg_accuracy']:.1f}/40")
        report.append(f"- Security: {stats['avg_security']:.1f}/20")
        report.append(f"- Efficiency: {stats['avg_efficiency']:.1f}/15")
        report.append(f"- Currency: {stats['avg_currency']:.1f}/15")
        report.append(f"- Usability: {stats['avg_usability']:.1f}/10")
        report.append("")
        
        if stats['avg_tokens'] > 0:
            report.append(f"**Resource Usage:**")
            report.append(f"- Average Tokens: {stats['avg_tokens']:.0f}")
            report.append(f"- Total Cost: ${stats['total_cost']:.2f}")
            report.append("")
        
        if stats['avg_doc_fetches'] > 0:
            report.append(f"**Documentation Usage:**")
            report.append(f"- Average Doc Fetches: {stats['avg_doc_fetches']:.1f} pages/scenario")
            report.append(f"- Total Doc Fetches: {stats['total_doc_fetches']}")
            report.append("")
        
        # Identify weaknesses
        weaknesses = []
        if stats['avg_accuracy'] < 30:
            weaknesses.append("Accuracy (skill invocation & file creation)")
        if stats['avg_security'] < 15:
            weaknesses.append("Security compliance")
        if stats['avg_efficiency'] < 10:
            weaknesses.append("Efficiency (batching & web fetch)")
        if stats['avg_currency'] < 10:
            weaknesses.append("Version currency")
        
        if weaknesses:
            report.append(f"**⚠️ Areas for Improvement:**")
            for weakness in weaknesses:
                report.append(f"- {weakness}")
            report.append("")
    
    # Recommendations
    report.append("---")
    report.append("")
    report.append("## Recommendations")
    report.append("")
    
    best_overall = max(all_stats, key=lambda x: x[1]['avg_score'])
    best_cost = min([s for s in all_stats if s[1]['total_cost'] > 0], 
                    key=lambda x: x[1]['total_cost'], default=None)
    
    report.append(f"### Best Overall Model")
    report.append(f"**{best_overall[0]}**")
    report.append(f"- Average Score: {best_overall[1]['avg_score']:.1f}/100")
    report.append(f"- Pass Rate: {best_overall[1]['pass_rate']:.1f}%")
    report.append("")
    
    if best_cost:
        report.append(f"### Most Cost-Effective")
        report.append(f"**{best_cost[0]}**")
        report.append(f"- Total Cost: ${best_cost[1]['total_cost']:.2f}")
        report.append(f"- Average Score: {best_cost[1]['avg_score']:.1f}/100")
        report.append("")
    
    # Write report
    with open(output_file, 'w') as f:
        f.write('\n'.join(report))


def print_console_comparison(models_data: List[Dict[str, Any]]):
    """Print comparison summary to console"""
    
    print("\n" + "=" * 100)
    print(f"{BLUE}LLM Model Comparison{NC}")
    print("=" * 100)
    print("")
    
    print(f"{BLUE}Models:{NC} {', '.join([m['model'] for m in models_data])}")
    print("")
    
    # Summary table
    print(f"{'Model':<20} {'Scenarios':<10} {'Passed':<8} {'Pass Rate':<12} {'Avg Score':<12} {'Doc Fetches':<12}")
    print("-" * 110)
    
    for model_data in models_data:
        model = model_data['model']
        stats = calculate_model_stats(model_data)
        
        status_color = GREEN if stats['pass_rate'] >= 80 else YELLOW if stats['pass_rate'] >= 60 else RED
        
        print(
            f"{model:<20} "
            f"{stats['total_scenarios']:<10} "
            f"{stats['passed']:<8} "
            f"{status_color}{stats['pass_rate']:>6.1f}%{NC}    "
            f"{stats['avg_score']:>6.1f}/100   "
            f"{stats['avg_doc_fetches']:>6.1f}"
        )
    
    print("")
    
    # Best model
    all_stats = [(m['model'], calculate_model_stats(m)) for m in models_data]
    best = max(all_stats, key=lambda x: x[1]['avg_score'])
    
    print(f"{GREEN}🏆 Best Overall:{NC} {best[0]} (Score: {best[1]['avg_score']:.1f}/100)")
    print("")
    print("=" * 100)
    print("")


def main():
    parser = argparse.ArgumentParser(description='Compare LLM model test results')
    parser.add_argument('--models', required=True, help='Comma-separated list of model names')
    parser.add_argument('--results-dir', help='Base results directory')
    parser.add_argument('--output', help='Output comparison report file')
    
    args = parser.parse_args()
    
    models = [m.strip() for m in args.models.split(',')]
    
    # Determine results directory
    if args.results_dir:
        results_base_dir = Path(args.results_dir)
    else:
        script_dir = Path(__file__).parent
        tests_dir = script_dir.parent
        results_base_dir = tests_dir / 'results'
    
    # Load results for each model
    models_data = []
    for model in models:
        model_data = load_model_results(results_base_dir, model)
        if not model_data['exists']:
            print(f"{YELLOW}Warning: No results found for model '{model}'{NC}")
        else:
            models_data.append(model_data)
    
    if not models_data:
        print(f"{RED}Error: No model results found{NC}")
        sys.exit(1)
    
    # Print console comparison
    print_console_comparison(models_data)
    
    # Generate markdown report
    output_file = Path(args.output) if args.output else results_base_dir / 'model-comparison.md'
    generate_comparison_report(models_data, output_file)
    
    print(f"{GREEN}✓{NC} Comparison report generated: {output_file}\n")


if __name__ == '__main__':
    main()
