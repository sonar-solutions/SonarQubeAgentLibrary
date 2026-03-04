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
            'currency': 0,
            'usability': 0,
            'total': 0
        }

        self.max_scores = {
            'accuracy': 40,
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
        self.validate_version_currency()
        self.validate_usability()
        self.validate_output_contracts()

        # Calculate total score
        self.scores['total'] = sum(self.scores.values()) - self.scores['total']

        # Status is informational: show failures if any hard failures occurred
        status = 'FAILED' if self.failures else 'PASSED'

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
        
        # Check if all expected skills are present
        missing_skills = set(expected_skills) - set(actual_skills)
        extra_skills = set(actual_skills) - set(expected_skills)
        
        if not missing_skills:
            self.scores['accuracy'] += 10
            if not extra_skills:
                print(f"  {GREEN}✓{NC} All expected skills invoked")
            else:
                print(f"  {GREEN}✓{NC} All expected skills invoked")
                print(f"  {YELLOW}!{NC} Extra skills (informational): {', '.join(sorted(extra_skills))}")
            self.checkpoints.append({
                'name': 'skill_invocation',
                'status': 'passed',
                'message': f"All required skills invoked. Extra: {sorted(extra_skills)}" if extra_skills else 'All expected skills invoked correctly'
            })
        else:
            self.failures.append(f"Missing skills: {', '.join(missing_skills)}")
            print(f"  {RED}✗{NC} Missing skills: {', '.join(missing_skills)}")
            if extra_skills:
                print(f"  {YELLOW}!{NC} Extra skills (informational): {', '.join(sorted(extra_skills))}")
            self.checkpoints.append({
                'name': 'skill_invocation',
                'status': 'failed',
                'message': f"Missing: {missing_skills}, Extra: {extra_skills}"
            })
    
    def _check_scanner_patterns(self, files_created, lang_rules):
        """Helper to check scanner patterns in files"""
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
        
        return correct_scanner
    
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
        correct_scanner = self._check_scanner_patterns(files_created, lang_rules)
        
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
    
    def _validate_single_file(self, expected_file, actual_files):
        """Helper to validate a single file's content"""
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
            return False
        
        content = actual_file.get('content', '')
        all_present = True
        
        # Check must_contain
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
            print(f"  {GREEN}✓{NC} File {expected_path} validated")
        
        return all_present
    
    def validate_files_created(self):
        """Validate that required files were created with correct content"""
        print(f"{YELLOW}[Checkpoint]{NC} Validating file creation...")
        
        expected_files = self.scenario.get('expected', {}).get('files_created', [])
        actual_files = self.result.get('files_created', [])
        
        for expected_file in expected_files:
            if self._validate_single_file(expected_file, actual_files):
                self.scores['accuracy'] += 5

        # Cap accuracy at maximum to prevent overflow from many files
        self.scores['accuracy'] = min(self.scores['accuracy'], self.max_scores['accuracy'])
    
    def _check_security_violations(self, files_created, security_rules):
        """Helper to check for security violations in files"""
        security_pass = True
        
        for file_info in files_created:
            content = file_info.get('content', '')
            
            # Check for hardcoded tokens
            for rule in security_rules:
                if rule['id'] == 'no-hardcoded-tokens':
                    for pattern_info in rule.get('patterns', []):
                        pattern = pattern_info.get('regex')
                        if re.search(pattern, content):
                            self.failures.append(pattern_info.get('failure_message'))
                            print(f"  {RED}✗{NC} {pattern_info.get('failure_message')}")
                            security_pass = False
                            self.scores['security'] -= 20
        
        return security_pass
    
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
        security_pass = self._check_security_violations(files_created, security_assertions.get('rules', []))
        
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

        # Warn if version data may be stale
        from datetime import datetime, timedelta
        last_updated = version_assertions.get('last_updated', '')
        staleness_days = version_assertions.get('staleness_warning_days', 90)
        if last_updated:
            try:
                updated_date = datetime.strptime(last_updated, '%Y-%m-%d')
                if datetime.now() - updated_date > timedelta(days=staleness_days):
                    print(f"  {YELLOW}!{NC} Warning: version-currency.json may be stale (last updated: {last_updated})")
            except ValueError:
                pass

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
    
    def _check_min_fetches(self, doc_assertions, total_fetches):
        """Check minimum fetch count rule and return score"""
        min_fetches_rule = next((r for r in doc_assertions['rules'] if r['id'] == 'minimum-fetches'), None)
        if not min_fetches_rule:
            return 0
        
        min_fetches = min_fetches_rule.get('default_min', 2)
        scenario_doc_fetch = self.scenario.get('expected', {}).get('documentation_fetches', {})
        if 'min_fetches' in scenario_doc_fetch:
            min_fetches = scenario_doc_fetch['min_fetches']
        
        if total_fetches < min_fetches:
            self.failures.append(f"Too few documentation fetches: {total_fetches} < {min_fetches}")
            print(f"  {RED}✗{NC} Too few fetches ({total_fetches} < {min_fetches})")
            return min_fetches_rule.get('score_if_not_met', -5)
        else:
            print(f"  {GREEN}✓{NC} Sufficient fetches ({total_fetches})")
            return min_fetches_rule.get('score_if_met', 3)
    
    def _check_max_fetches(self, doc_assertions, total_fetches):
        """Check maximum fetch count rule and return score"""
        max_fetches_rule = next((r for r in doc_assertions['rules'] if r['id'] == 'maximum-fetches'), None)
        if not max_fetches_rule:
            return 0
        
        max_fetches = max_fetches_rule.get('default_max', 10)
        scenario_doc_fetch = self.scenario.get('expected', {}).get('documentation_fetches', {})
        if 'max_fetches' in scenario_doc_fetch:
            max_fetches = scenario_doc_fetch['max_fetches']
        
        if total_fetches > max_fetches:
            print(f"  {YELLOW}!{NC} Many fetches ({total_fetches} > {max_fetches})")
            return max_fetches_rule.get('score_if_exceeded', -2)
        return 0
    
    def _check_official_sources(self, doc_assertions, fetched_domains, platform):
        """Check official sources rule and return score"""
        official_sources_rule = next((r for r in doc_assertions['rules'] if r['id'] == 'official-sources'), None)
        if not official_sources_rule:
            return 0
        
        required_domains = list(official_sources_rule['required_domains']['all_scenarios'])
        if platform in official_sources_rule['required_domains']:
            required_domains.extend(official_sources_rule['required_domains'][platform])
        
        scenario_doc_fetch = self.scenario.get('expected', {}).get('documentation_fetches', {})
        if 'expected_domains' in scenario_doc_fetch:
            required_domains.extend(scenario_doc_fetch['expected_domains'])
        
        required_domains = list(set(required_domains))
        score = 0
        
        for domain in required_domains:
            if any(domain in fd for fd in fetched_domains):
                print(f"  {GREEN}✓{NC} Fetched from {domain}")
                score += official_sources_rule.get('score_per_domain', 2)
            else:
                print(f"  {YELLOW}!{NC} No fetches from {domain}")
        return score
    
    def _check_relevant_pages(self, doc_assertions, fetched_pages, language):
        """Check relevant pages rule and return score"""
        relevant_pages_rule = next((r for r in doc_assertions['rules'] if r['id'] == 'relevant-pages'), None)
        if not relevant_pages_rule:
            return 0
        
        expected_patterns = relevant_pages_rule['expected_patterns_by_language'].get(language, [])
        scenario_doc_fetch = self.scenario.get('expected', {}).get('documentation_fetches', {})
        if 'expected_pages' in scenario_doc_fetch:
            for page in scenario_doc_fetch['expected_pages']:
                expected_patterns.append(page)
        
        score = 0
        for expected in expected_patterns:
            pattern = expected.get('pattern')
            description = expected.get('description')
            score_value = expected.get('score', 1)
            
            matched = False
            for page in fetched_pages:
                if re.search(pattern, page.get('url', '')):
                    matched = True
                    print(f"  {GREEN}✓{NC} Fetched: {description}")
                    score += score_value
                    break
            
            if not matched:
                print(f"  {YELLOW}!{NC} Missing: {description}")
        return score
    
    def _check_duplicate_fetches(self, doc_assertions, fetched_pages, total_fetches):
        """Check duplicate fetches rule and return score"""
        if total_fetches == 0:
            return 0
        
        unique_urls = len({p.get('url') for p in fetched_pages})
        duplicate_ratio = 1 - (unique_urls / total_fetches)
        
        no_dup_rule = next((r for r in doc_assertions['rules'] if r['id'] == 'no-duplicate-fetches'), None)
        if not no_dup_rule:
            return 0
        
        max_dup_ratio = no_dup_rule.get('max_duplicate_ratio', 0.3)
        if duplicate_ratio <= max_dup_ratio:
            return no_dup_rule.get('score_if_met', 1)
        else:
            print(f"  {YELLOW}!{NC} {no_dup_rule.get('warning_message')}")
            return 0
    
    def _check_curl_md_pattern(self, doc_assertions, fetched_pages):
        """Check that docs.sonarsource.com URLs use .md extension, warn if not"""
        curl_md_rule = next((r for r in doc_assertions['rules'] if r['id'] == 'curl-md-pattern'), None)
        if not curl_md_rule:
            return 0

        sonar_pages = [p for p in fetched_pages if 'docs.sonarsource.com' in p.get('url', '')]
        if not sonar_pages:
            return 0

        md_pages = [p for p in sonar_pages if p.get('url', '').endswith('.md')]
        if md_pages:
            print(f"  {GREEN}✓{NC} docs.sonarsource.com fetched with .md extension")
            return curl_md_rule.get('score_if_met', 1)
        else:
            print(f"  {YELLOW}!{NC} {curl_md_rule.get('warning_message', 'Not using .md URL pattern')}")
            return curl_md_rule.get('score_if_not_met', 0)

    def _print_fetched_pages(self, fetched_pages):
        """Print the fetched pages for review"""
        if not fetched_pages:
            return
        
        print("\n  📚 Documentation pages fetched:")
        for i, page in enumerate(fetched_pages[:10], 1):
            url = page.get('url', 'unknown')
            title = page.get('title', '')
            if title:
                print(f"     {i}. {url} - {title[:50]}")
            else:
                print(f"     {i}. {url}")
        
        if len(fetched_pages) > 10:
            print(f"     ... and {len(fetched_pages) - 10} more")

    def validate_documentation_fetches(self):
        """Validate that proper documentation was fetched"""
        print(f"{YELLOW}[Checkpoint]{NC} Validating documentation fetches...")
        
        assertion_file = self.assertions_dir / 'documentation-fetches.json'
        if not assertion_file.exists():
            print(f"  {YELLOW}!{NC} No documentation fetch assertions found")
            return
        
        with open(assertion_file, 'r') as f:
            doc_assertions = json.load(f)
        
        actual_doc_fetch = self.result.get('documentation_fetches', {})
        total_fetches = actual_doc_fetch.get('total_count', 0)
        fetched_pages = actual_doc_fetch.get('pages', [])
        fetched_domains = actual_doc_fetch.get('domains', [])
        
        language = self.scenario.get('language')
        platform = self.scenario.get('platform')
        
        print(f"  📄 Total documentation fetches: {total_fetches}")
        if fetched_domains:
            print(f"  🌐 Domains accessed: {', '.join(set(fetched_domains))}")
        
        max_doc_score = doc_assertions.get('scoring', {}).get('max_points', 15)
        doc_score = 0
        
        doc_score += self._check_min_fetches(doc_assertions, total_fetches)
        doc_score += self._check_max_fetches(doc_assertions, total_fetches)
        doc_score += self._check_official_sources(doc_assertions, fetched_domains, platform)
        doc_score += self._check_relevant_pages(doc_assertions, fetched_pages, language)
        doc_score += self._check_duplicate_fetches(doc_assertions, fetched_pages, total_fetches)
        doc_score += self._check_curl_md_pattern(doc_assertions, fetched_pages)
        
        actual_doc_score = min(max(doc_score, 0), max_doc_score)
        self.scores['efficiency'] += actual_doc_score
        
        self._print_fetched_pages(fetched_pages)
        
        print(f"  📊 Documentation score: {actual_doc_score}/{max_doc_score}")
        
        self.checkpoints.append({
            'name': 'documentation_fetches',
            'status': 'passed' if total_fetches >= 2 else 'warning',
            'message': f'{total_fetches} documentation pages fetched',
            'score': actual_doc_score,
            'max_score': max_doc_score,
            'details': {
                'total_count': total_fetches,
                'unique_count': len({p.get('url') for p in fetched_pages}),
                'domains': list(set(fetched_domains)),
                'pages': [p.get('url') for p in fetched_pages]
            }
        })


    def validate_usability(self):
        """Validate usability - clear setup instructions provided to user"""
        print(f"{YELLOW}[Checkpoint]{NC} Validating usability...")

        skills_invoked = self.result.get('skills_invoked', [])
        files_created = self.result.get('files_created', [])
        usability_score = 0

        # Check 1: Setup instructions skill was invoked
        if 'devops-setup-instructions' in skills_invoked:
            usability_score += 5
            print(f"  {GREEN}✓{NC} Setup instructions skill invoked")
        else:
            print(f"  {YELLOW}!{NC} Setup instructions skill not invoked")

        # Check 2: Files contain references to required secrets/variables
        setup_keywords = ['SONAR_TOKEN', 'secrets.', 'environment variable',
                          'repository variable', 'CI/CD variable', 'pipeline variable']
        has_setup_content = False
        for file_info in files_created:
            content = file_info.get('content', '')
            if any(kw in content for kw in setup_keywords):
                has_setup_content = True
                break

        if has_setup_content:
            usability_score += 5
            print(f"  {GREEN}✓{NC} Setup guidance present in created files")
        else:
            print(f"  {YELLOW}!{NC} No setup guidance found in created files")

        self.scores['usability'] = min(usability_score, self.max_scores['usability'])
        self.checkpoints.append({
            'name': 'usability',
            'status': 'passed' if usability_score >= 5 else 'failed',
            'message': f'Usability score: {usability_score}/{self.max_scores["usability"]}'
        })

    def validate_efficiency_batching(self):
        """Validate that prerequisite questions were batched efficiently"""
        print(f"{YELLOW}[Checkpoint]{NC} Validating question batching efficiency...")

        agent_output_path = self.result.get('execution', {}).get('agent_output', '')
        if not agent_output_path or not Path(agent_output_path).exists():
            print(f"  {YELLOW}!{NC} Agent output not available for batching check")
            return

        with open(agent_output_path, 'r', errors='replace') as f:
            output = f.read()

        # Heuristic: multiple question marks in close proximity indicates batched questions
        question_blocks = re.findall(r'[^\n]*\?[^\n]*\n[^\n]*\?', output)

        if question_blocks:
            batching_score = 5
            print(f"  {GREEN}✓{NC} Questions appear to be batched efficiently")
        else:
            batching_score = 2
            print(f"  {YELLOW}!{NC} Questions may be sequential (partial credit)")

        self.scores['efficiency'] = min(
            self.scores['efficiency'] + batching_score,
            self.max_scores['efficiency']
        )
        self.checkpoints.append({
            'name': 'efficiency_batching',
            'status': 'passed' if batching_score == 5 else 'warning',
            'message': f'Batching score: {batching_score}/5'
        })

    def validate_output_contracts(self):
        """Validate that Output Contracts were produced by platform and scanner skills"""
        print(f"{YELLOW}[Checkpoint]{NC} Validating Output Contracts...")

        agent_output_path = self.result.get('execution', {}).get('agent_output', '')
        agent_output = ''
        if agent_output_path and Path(agent_output_path).exists():
            with open(agent_output_path, 'r', errors='replace') as f:
                agent_output = f.read()

        if not agent_output:
            print(f"  {YELLOW}!{NC} Agent output not available for Output Contract check")
            return

        platform_contract = bool(re.search(r'Platform Output Contract', agent_output, re.IGNORECASE))
        scanner_contract = bool(re.search(r'Scanner Output Contract', agent_output, re.IGNORECASE))

        if platform_contract:
            self.scores['accuracy'] = min(self.scores['accuracy'] + 5, self.max_scores['accuracy'])
            print(f"  {GREEN}✓{NC} Platform Output Contract found")
        else:
            print(f"  {YELLOW}!{NC} Platform Output Contract not found in agent output")

        if scanner_contract:
            self.scores['accuracy'] = min(self.scores['accuracy'] + 5, self.max_scores['accuracy'])
            print(f"  {GREEN}✓{NC} Scanner Output Contract found")
        else:
            print(f"  {YELLOW}!{NC} Scanner Output Contract not found in agent output")

        self.checkpoints.append({
            'name': 'output_contracts',
            'status': 'passed' if (platform_contract and scanner_contract) else 'warning',
            'message': f'Platform: {platform_contract}, Scanner: {scanner_contract}'
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
        # Path structure: .../tests/scenarios/<language>/<name>.yaml
        # Go up 3 levels from the file to reach tests/
        tests_dir = scenario_file.parent.parent.parent if 'scenarios' in str(scenario_file) else scenario_file.parent
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
    
    max_total = sum(validator.max_scores.values())
    print(f"Score: {validation_result['scores']['total']}/{max_total}")
    print(f"  Accuracy:   {validation_result['scores']['accuracy']}/{validator.max_scores['accuracy']}")
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
    
    sys.exit(0)


if __name__ == '__main__':
    main()
