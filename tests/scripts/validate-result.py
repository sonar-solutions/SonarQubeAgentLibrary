#!/usr/bin/env python3
"""
validate-result.py - Validate test results against scenario expectations

Usage:
    python validate-result.py --scenario <scenario-file> --result <result-file>
"""

import argparse
import json
import yaml
import re
import sys
from pathlib import Path
from typing import Dict, List, Any

# ANSI color codes
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


class TestValidator:
    def __init__(self, scenario_file: Path, result_file: Path, assertions_dir: Path):
        self.scenario_file = scenario_file
        self.result_file = result_file
        self.assertions_dir = assertions_dir
        
        # Load files
        with open(scenario_file, 'r') as f:
            self.scenario = yaml.safe_load(f)
        
        with open(result_file, 'r') as f:
            self.result = json.load(f)
        
        # Initialize scores
        self.scores = {
            'accuracy': 0,
            'security': 0,
            'efficiency': 0,
            'currency': 0,
            'usability': 0,
            'total': 0
        }
        
        self.max_scores = {
            'accuracy': 40,
            'security': 20,
            'efficiency': 15,
            'currency': 15,
            'usability': 10
        }
        
        self.checkpoints = []
        self.failures = []
    
    def validate_all(self) -> Dict[str, Any]:
        """Run all validations"""
        print(f"\n{BLUE}Validating Test Results{NC}\n")
        
        # Run validation checks
        self.validate_skill_invocation()
        self.validate_scanner_selection()
        self.validate_files_created()
        self.validate_security_compliance()
        self.validate_version_currency()
        self.validate_documentation_fetches()
        
        # Calculate total score
        self.scores['total'] = sum(self.scores.values()) - self.scores['total']
        
        # Determine pass/fail
        pass_threshold = 80
        status = 'PASSED' if self.scores['total'] >= pass_threshold else 'FAILED'
        
        return {
            'status': status,
            'scores': self.scores,
            'max_scores': self.max_scores,
            'checkpoints': self.checkpoints,
            'failures': self.failures
        }
    
    def validate_skill_invocation(self):
        """Validate that correct skills were invoked in proper order"""
        print(f"{YELLOW}[Checkpoint]{NC} Validating skill invocation...")
        
        expected_skills = self.scenario.get('expected', {}).get('skills_invoked', [])
        actual_skills = self.result.get('skills_invoked', [])
        
        # Load skill invocation assertions
        assertion_file = self.assertions_dir / 'skill-invocation.json'
        if assertion_file.exists():
            with open(assertion_file, 'r') as f:
                skill_assertions = json.load(f)
        
        # Check if all expected skills are present
        missing_skills = set(expected_skills) - set(actual_skills)
        extra_skills = set(actual_skills) - set(expected_skills)
        
        if not missing_skills and not extra_skills:
            self.scores['accuracy'] += 10
            print(f"  {GREEN}✓{NC} All expected skills invoked")
            self.checkpoints.append({
                'name': 'skill_invocation',
                'status': 'passed',
                'message': 'All expected skills invoked correctly'
            })
        else:
            if missing_skills:
                self.failures.append(f"Missing skills: {', '.join(missing_skills)}")
                print(f"  {RED}✗{NC} Missing skills: {', '.join(missing_skills)}")
            if extra_skills:
                print(f"  {YELLOW}!{NC} Unexpected skills: {', '.join(extra_skills)}")
            
            self.checkpoints.append({
                'name': 'skill_invocation',
                'status': 'failed',
                'message': f"Missing: {missing_skills}, Extra: {extra_skills}"
            })
    
    def validate_scanner_selection(self):
        """Validate that the correct scanner was selected"""
        print(f"{YELLOW}[Checkpoint]{NC} Validating scanner selection...")
        
        language = self.scenario.get('language')
        
        # Load scanner selection assertions
        assertion_file = self.assertions_dir / 'scanner-selection.json'
        if not assertion_file.exists():
            print(f"  {YELLOW}!{NC} No scanner assertions found")
            return
        
        with open(assertion_file, 'r') as f:
            scanner_assertions = json.load(f)
        
        # Find language-specific rules
        lang_rules = None
        for rule in scanner_assertions.get('rules', []):
            if rule.get('language') == language:
                lang_rules = rule
                break
        
        if not lang_rules:
            print(f"  {YELLOW}!{NC} No rules for language: {language}")
            return
        
        # Check files created for correct scanner usage
        files_created = self.result.get('files_created', [])
        correct_scanner = False
        
        for file_info in files_created:
            content = file_info.get('content', '')
            
            # Check for correct patterns
            for pattern in lang_rules.get('correct_patterns', []):
                if re.search(pattern, content):
                    correct_scanner = True
                    break
            
            # Check for incorrect patterns
            for incorrect in lang_rules.get('incorrect_patterns', []):
                pattern = incorrect.get('pattern')
                if re.search(pattern, content):
                    reason = incorrect.get('reason')
                    self.failures.append(f"Incorrect scanner: {reason}")
                    print(f"  {RED}✗{NC} {reason}")
                    correct_scanner = False
        
        if correct_scanner:
            self.scores['accuracy'] += 10
            print(f"  {GREEN}✓{NC} Correct scanner selected")
            self.checkpoints.append({
                'name': 'scanner_selection',
                'status': 'passed',
                'message': f"Correct {lang_rules['expected_scanner']} used"
            })
        else:
            self.checkpoints.append({
                'name': 'scanner_selection',
                'status': 'failed',
                'message': 'Incorrect scanner selection'
            })
    
    def validate_files_created(self):
        """Validate that required files were created with correct content"""
        print(f"{YELLOW}[Checkpoint]{NC} Validating file creation...")
        
        expected_files = self.scenario.get('expected', {}).get('files_created', [])
        actual_files = self.result.get('files_created', [])
        
        for expected_file in expected_files:
            expected_path = expected_file.get('path')
            must_contain = expected_file.get('must_contain', [])
            must_not_contain = expected_file.get('must_not_contain', [])
            
            # Find matching file
            actual_file = None
            for af in actual_files:
                if af.get('path') == expected_path:
                    actual_file = af
                    break
            
            if not actual_file:
                self.failures.append(f"File not created: {expected_path}")
                print(f"  {RED}✗{NC} File not created: {expected_path}")
                continue
            
            content = actual_file.get('content', '')
            
            # Check must_contain
            all_present = True
            for item in must_contain:
                if item not in content:
                    self.failures.append(f"Missing content in {expected_path}: {item}")
                    print(f"  {RED}✗{NC} Missing: {item}")
                    all_present = False
            
            # Check must_not_contain
            for item in must_not_contain:
                if item in content:
                    self.failures.append(f"Forbidden content in {expected_path}: {item}")
                    print(f"  {RED}✗{NC} Contains forbidden: {item}")
                    all_present = False
            
            if all_present:
                self.scores['accuracy'] += 5
                print(f"  {GREEN}✓{NC} File {expected_path} validated")
    
    def validate_security_compliance(self):
        """Validate security best practices"""
        print(f"{YELLOW}[Checkpoint]{NC} Validating security compliance...")
        
        # Load security assertions
        assertion_file = self.assertions_dir / 'security-compliance.json'
        if not assertion_file.exists():
            print(f"  {YELLOW}!{NC} No security assertions found")
            return
        
        with open(assertion_file, 'r') as f:
            security_assertions = json.load(f)
        
        files_created = self.result.get('files_created', [])
        security_pass = True
        
        for file_info in files_created:
            content = file_info.get('content', '')
            path = file_info.get('path', '')
            
            # Check for hardcoded tokens
            for rule in security_assertions.get('rules', []):
                if rule['id'] == 'no-hardcoded-tokens':
                    for pattern_info in rule.get('patterns', []):
                        pattern = pattern_info.get('regex')
                        if re.search(pattern, content):
                            self.failures.append(pattern_info.get('failure_message'))
                            print(f"  {RED}✗{NC} {pattern_info.get('failure_message')}")
                            security_pass = False
                            self.scores['security'] -= 20
        
        if security_pass:
            self.scores['security'] += 20
            print(f"  {GREEN}✓{NC} No security violations found")
            self.checkpoints.append({
                'name': 'security_compliance',
                'status': 'passed',
                'message': 'All security checks passed'
            })
    
    def validate_version_currency(self):
        """Validate that latest versions are used"""
        print(f"{YELLOW}[Checkpoint]{NC} Validating version currency...")
        
        # Load version assertions
        assertion_file = self.assertions_dir / 'version-currency.json'
        if not assertion_file.exists():
            print(f"  {YELLOW}!{NC} No version assertions found")
            return
        
        with open(assertion_file, 'r') as f:
            version_assertions = json.load(f)
        
        platform = self.scenario.get('platform')
        files_created = self.result.get('files_created', [])
        
        current_versions_used = 0
        total_checks = 0
        
        for file_info in files_created:
            content = file_info.get('content', '')
            
            # Get platform-specific version checks
            platform_checks = version_assertions.get('platforms', {}).get(platform, {})
            
            # Check actions (GitHub Actions specific)
            for action in platform_checks.get('actions', []):
                pattern = action.get('pattern')
                matches = re.findall(pattern, content)
                
                for match in matches:
                    total_checks += 1
                    if match == action.get('current_version', '').replace('v', ''):
                        current_versions_used += 1
                    elif match in [v.replace('v', '') for v in action.get('deprecated_versions', [])]:
                        self.failures.append(f"Deprecated version: {action['name']}@v{match}")
                        print(f"  {RED}✗{NC} Deprecated: {action['name']}@v{match}")
        
        if total_checks > 0:
            currency_score = int((current_versions_used / total_checks) * 15)
            self.scores['currency'] += currency_score
            print(f"  {GREEN}✓{NC} Version currency: {current_versions_used}/{total_checks} current")
        else:
            print(f"  {YELLOW}!{NC} No version checks applicable")
    
    def validate_documentation_fetches(self):
        """Validate that proper documentation was fetched"""
        print(f"{YELLOW}[Checkpoint]{NC} Validating documentation fetches...")
        
        expected_doc_fetch = self.scenario.get('expected', {}).get('documentation_fetches', {})
        actual_doc_fetch = self.result.get('documentation_fetches', {})
        
        if not expected_doc_fetch:
            print(f"  {YELLOW}!{NC} No documentation fetch expectations defined")
            return
        
        total_fetches = actual_doc_fetch.get('total_count', 0)
        fetched_pages = actual_doc_fetch.get('pages', [])
        fetched_domains = actual_doc_fetch.get('domains', [])
        
        # Print fetch summary
        print(f"  📄 Total documentation fetches: {total_fetches}")
        if fetched_domains:
            print(f"  🌐 Domains accessed: {', '.join(set(fetched_domains))}")
        
        # Check minimum fetches
        min_fetches = expected_doc_fetch.get('min_fetches', 0)
        max_fetches = expected_doc_fetch.get('max_fetches', 100)
        
        if total_fetches < min_fetches:
            self.failures.append(f"Too few documentation fetches: {total_fetches} < {min_fetches}")
            print(f"  {RED}✗{NC} Too few fetches ({total_fetches} < {min_fetches})")
        elif total_fetches > max_fetches:
            print(f"  {YELLOW}!{NC} Many fetches ({total_fetches} > {max_fetches})")
        else:
            self.scores['efficiency'] += 3
            print(f"  {GREEN}✓{NC} Appropriate number of fetches ({total_fetches})")
        
        # Check expected domains
        expected_domains = expected_doc_fetch.get('expected_domains', [])
        fetched_domain_set = set(fetched_domains)
        
        for domain in expected_domains:
            if any(domain in fd for fd in fetched_domain_set):
                print(f"  {GREEN}✓{NC} Fetched from {domain}")
                self.scores['efficiency'] += 2
            else:
                print(f"  {YELLOW}!{NC} No fetches from {domain}")
        
        # Check expected page patterns
        expected_pages = expected_doc_fetch.get('expected_pages', [])
        for expected_page in expected_pages:
            pattern = expected_page.get('pattern')
            description = expected_page.get('description')
            
            matched = False
            for page in fetched_pages:
                if re.search(pattern, page.get('url', '')):
                    matched = True
                    print(f"  {GREEN}✓{NC} Fetched: {description}")
                    break
            
            if not matched:
                print(f"  {YELLOW}!{NC} Missing: {description}")
        
        # Log all fetched pages for review
        if fetched_pages:
            print(f"\n  📚 Documentation pages fetched:")
            for i, page in enumerate(fetched_pages[:10], 1):  # Show first 10
                url = page.get('url', 'unknown')
                title = page.get('title', '')
                if title:
                    print(f"     {i}. {url} - {title[:50]}")
                else:
                    print(f"     {i}. {url}")
            
            if len(fetched_pages) > 10:
                print(f"     ... and {len(fetched_pages) - 10} more")
        
        self.checkpoints.append({
            'name': 'documentation_fetches',
            'status': 'passed' if total_fetches >= min_fetches else 'warning',
            'message': f'{total_fetches} documentation pages fetched',
            'details': {
                'total_count': total_fetches,
                'domains': list(set(fetched_domains)),
                'pages': [p.get('url') for p in fetched_pages]
            }
        })


def main():
    parser = argparse.ArgumentParser(description='Validate test results against scenarios')
    parser.add_argument('--scenario', required=True, help='Path to scenario YAML file')
    parser.add_argument('--result', required=True, help='Path to result JSON file')
    parser.add_argument('--assertions-dir', help='Path to assertions directory')
    
    args = parser.parse_args()
    
    scenario_file = Path(args.scenario)
    result_file = Path(args.result)
    
    if not scenario_file.exists():
        print(f"{RED}Error: Scenario file not found: {scenario_file}{NC}")
        sys.exit(1)
    
    if not result_file.exists():
        print(f"{RED}Error: Result file not found: {result_file}{NC}")
        sys.exit(1)
    
    # Determine assertions directory
    if args.assertions_dir:
        assertions_dir = Path(args.assertions_dir)
    else:
        # Default to tests/assertions
        tests_dir = scenario_file.parent.parent if 'scenarios' in str(scenario_file) else scenario_file.parent
        assertions_dir = tests_dir / 'assertions'
    
    # Run validation
    validator = TestValidator(scenario_file, result_file, assertions_dir)
    validation_result = validator.validate_all()
    
    # Print summary
    print(f"\n{'=' * 44}")
    status = validation_result['status']
    if status == 'PASSED':
        print(f"{GREEN}TEST {status} ✓{NC}")
    else:
        print(f"{RED}TEST {status} ✗{NC}")
    print(f"{'=' * 44}")
    
    print(f"Score: {validation_result['scores']['total']}/100")
    print(f"  Accuracy:   {validation_result['scores']['accuracy']}/{validator.max_scores['accuracy']}")
    print(f"  Security:   {validation_result['scores']['security']}/{validator.max_scores['security']}")
    print(f"  Efficiency: {validation_result['scores']['efficiency']}/{validator.max_scores['efficiency']}")
    print(f"  Currency:   {validation_result['scores']['currency']}/{validator.max_scores['currency']}")
    print(f"  Usability:  {validation_result['scores']['usability']}/{validator.max_scores['usability']}")
    print(f"{'=' * 44}\n")
    
    # Update result file with validation
    with open(result_file, 'r+') as f:
        result_data = json.load(f)
        result_data['validation'] = validation_result
        result_data['scores'] = validation_result['scores']
        result_data['status'] = status.lower()
        f.seek(0)
        json.dump(result_data, f, indent=2)
        f.truncate()
    
    sys.exit(0 if status == 'PASSED' else 1)


if __name__ == '__main__':
    main()
