#!/usr/bin/env python3
"""Fetch SonarQube configuration versions and YAML templates from official sources.

Returns compact JSON with extracted versions and workflow templates,
reducing ~120KB of raw documentation to ~5KB of structured data.

Zero external dependencies — uses only Python stdlib.
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# URL lookup tables
# ---------------------------------------------------------------------------

PLATFORM_DOCS = {
    "github-actions": {
        "cloud": [
            "https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/ci-based-analysis/github-actions-for-sonarcloud",
            "https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/github-actions-for-sonarcloud",
        ],
        "server": [
            "https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/github-integration/adding-analysis-to-github-actions-workflow",
        ],
    },
    "gitlab-ci": {
        "cloud": [
            "https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/ci-based-analysis/gitlab-ci",
            "https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/gitlab-ci",
        ],
        "server": [
            "https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/gitlab-integration/adding-analysis-to-gitlab-ci-cd",
        ],
    },
    "azure-devops": {
        "cloud": [
            "https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/ci-based-analysis/azure-pipelines/adding-analysis-to-build-pipeline",
            "https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/azure-pipelines/adding-analysis-to-build-pipeline",
        ],
        "server": [
            "https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/azure-devops-integration/adding-analysis-to-pipeline",
        ],
    },
    "bitbucket": {
        "cloud": [
            "https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/ci-based-analysis/bitbucket-pipelines-for-sonarcloud",
            "https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/bitbucket-pipelines-for-sonarcloud",
        ],
        "server": [
            "https://docs.sonarsource.com/sonarqube-server/devops-platform-integration/bitbucket-integration/bitbucket-cloud-integration/bitbucket-pipelines",
        ],
    },
}

SCANNER_VERSION_URLS = {
    "maven": "https://downloads.sonarsource.com/sonarqube/update/scannermaven.json",
    "gradle": "https://downloads.sonarsource.com/sonarqube/update/scannergradle.json",
    "dotnet": "https://downloads.sonarsource.com/sonarqube/update/scannermsbuild.json",
}

BITBUCKET_PIPE_URLS = {
    "cloud": {
        "scan": "https://api.bitbucket.org/2.0/repositories/sonarsource/sonarcloud-scan/refs/tags?sort=-name&pagelen=1",
        "quality_gate": "https://api.bitbucket.org/2.0/repositories/sonarsource/sonarcloud-quality-gate/refs/tags?sort=-name&pagelen=1",
    },
    "server": {
        "scan": "https://api.bitbucket.org/2.0/repositories/sonarsource/sonarqube-scan/refs/tags?sort=-name&pagelen=1",
        "quality_gate": "https://api.bitbucket.org/2.0/repositories/sonarsource/sonarqube-quality-gate/refs/tags?sort=-name&pagelen=1",
    },
}

# Keywords used to classify YAML blocks by scanner approach
# More specific keywords come first and are weighted higher
SCANNER_KEYWORDS = {
    "maven": ["mvn ", "maven:", "sonar:sonar", "sonar-maven-plugin"],
    "gradle": ["gradlew", "gradle ", "gradle:", "org.sonarqube"],
    "dotnet": ["dotnet ", "sonarscanner begin", "sonarscanner end", "msbuild", ".csproj"],
    "cli": ["sonarqube-scan-action", "sonar-scanner-cli", "sonarcloud-scan"],
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def fetch_url(url, timeout=15):
    """Fetch a URL and return (content, None) or (None, error_message)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SonarArchitect/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            if "not found" in content.lower()[:200] and len(content) < 200:
                return None, f"Page not found: {url}"
            return content, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {url}"
    except urllib.error.URLError as e:
        return None, f"URL error: {e.reason} — {url}"
    except Exception as e:
        return None, f"Fetch error: {e} — {url}"


def fetch_with_fallbacks(urls, timeout=15):
    """Try each URL in order, return first successful (content, url) or (None, errors)."""
    errors = []
    for url in urls:
        md_url = url + ".md"
        content, err = fetch_url(md_url, timeout)
        if content is not None:
            return content, md_url, []
        errors.append(err)
    return None, None, errors


def extract_yaml_blocks(markdown):
    """Extract fenced YAML code blocks from markdown content."""
    pattern = r"```(?:yaml|yml)\s*\n(.*?)```"
    return re.findall(pattern, markdown, re.DOTALL)


def classify_yaml_block(block):
    """Classify a YAML block by scanner approach based on keywords."""
    block_lower = block.lower()
    scores = {}
    for approach, keywords in SCANNER_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in block_lower)
        if score > 0:
            scores[approach] = score
    if not scores:
        return "unknown"
    return max(scores, key=scores.get)


def extract_github_action_versions(markdown):
    """Extract action versions from GitHub Actions workflow examples."""
    versions = {}
    for match in re.finditer(r"uses:\s+([\w.-]+/[\w.-]+)@(v?\d[\w.]*)", markdown):
        action, version = match.group(1), match.group(2)
        # Keep the latest version found for each action
        if action not in versions or version > versions[action]:
            versions[action] = version
    return versions


def extract_gitlab_image_versions(markdown):
    """Extract Docker image versions from GitLab CI examples."""
    versions = {}
    for match in re.finditer(
        r"(?:image:\s*(?:name:\s*)?)(sonarsource/[\w.-]+):([\w.]+)", markdown
    ):
        image, version = match.group(1), match.group(2)
        versions[image] = version
    # Also extract non-sonarsource images used in examples
    for match in re.finditer(
        r"image:\s*((?:gradle|maven|mcr\.microsoft\.com)[\w./-]*?):([\w.-]+)", markdown
    ):
        image, version = match.group(1), match.group(2)
        versions[image] = version
    return versions


def extract_azure_task_versions(markdown):
    """Extract Azure DevOps task versions from pipeline examples."""
    versions = {}
    for match in re.finditer(r"task:\s+(SonarQube\w+)@(\d+)", markdown):
        task, version = match.group(1), match.group(2)
        versions[task] = version
    for match in re.finditer(r"task:\s+(Cache)@(\d+)", markdown):
        task, version = match.group(1), match.group(2)
        versions[task] = version
    return versions


def extract_bitbucket_pipe_versions(markdown):
    """Extract Bitbucket pipe references from pipeline examples."""
    versions = {}
    for match in re.finditer(
        r"pipe:\s+(sonarsource/[\w.-]+):([\w.]+)", markdown
    ):
        pipe, version = match.group(1), match.group(2)
        versions[pipe] = version
    return versions


# ---------------------------------------------------------------------------
# Phase 1: Platform documentation
# ---------------------------------------------------------------------------


def fetch_platform_docs(platform, scanner_approach, sonarqube_type, timeout=15):
    """Fetch platform documentation and extract versions + YAML templates."""
    result = {
        "name": platform,
        "doc_url_fetched": None,
        "fetch_status": "error",
        "action_versions": {},
        "task_versions": {},
        "image_versions": {},
        "pipe_versions": {},
        "yaml_templates": {},
    }
    errors = []
    warnings = []

    urls = PLATFORM_DOCS.get(platform, {}).get(sonarqube_type, [])
    if not urls:
        errors.append(f"No documentation URL configured for {platform}/{sonarqube_type}")
        return result, errors, warnings

    # Try primary type first, then fallback to the other type
    content, fetched_url, fetch_errors = fetch_with_fallbacks(urls, timeout)

    # If primary type failed, try the other type as fallback
    if content is None:
        other_type = "server" if sonarqube_type == "cloud" else "cloud"
        other_urls = PLATFORM_DOCS.get(platform, {}).get(other_type, [])
        if other_urls:
            warnings.append(
                f"{sonarqube_type} docs unavailable, falling back to {other_type} docs"
            )
            content, fetched_url, more_errors = fetch_with_fallbacks(other_urls, timeout)
            fetch_errors.extend(more_errors)

    if content is None:
        errors.extend(fetch_errors)
        return result, errors, warnings

    result["doc_url_fetched"] = fetched_url
    result["fetch_status"] = "ok"

    # Extract versions based on platform
    if platform == "github-actions":
        result["action_versions"] = extract_github_action_versions(content)
    elif platform == "gitlab-ci":
        result["image_versions"] = extract_gitlab_image_versions(content)
    elif platform == "azure-devops":
        result["task_versions"] = extract_azure_task_versions(content)
    elif platform == "bitbucket":
        result["pipe_versions"] = extract_bitbucket_pipe_versions(content)

    # Extract and classify YAML templates
    yaml_blocks = extract_yaml_blocks(content)
    templates = {}
    for block in yaml_blocks:
        approach = classify_yaml_block(block)
        block_stripped = block.strip()
        # Keep the first (usually simplest) template per approach
        if approach not in templates:
            templates[approach] = block_stripped
        # Also store as "monorepo" if it contains monorepo keywords
        if "monorepo" in block.lower() or "paths:" in block.lower():
            if "monorepo" not in templates:
                templates["monorepo"] = block_stripped

    # Filter to only include the requested scanner approach + monorepo
    filtered = {}
    if scanner_approach in templates:
        filtered[scanner_approach] = templates[scanner_approach]
    if "monorepo" in templates:
        filtered["monorepo"] = templates["monorepo"]
    # If no match for the specific approach, include all classified templates
    if not filtered and templates:
        filtered = templates
        warnings.append(
            f"No YAML template matched scanner approach '{scanner_approach}'; returning all found templates"
        )

    result["yaml_templates"] = filtered

    return result, errors, warnings


# ---------------------------------------------------------------------------
# Phase 2: Scanner version JSON
# ---------------------------------------------------------------------------


def fetch_scanner_version(scanner_approach, timeout=15):
    """Fetch the latest scanner plugin/tool version from downloads.sonarsource.com."""
    result = {
        "name": scanner_approach,
        "version": None,
        "version_source": None,
        "fetch_status": "skipped",
    }
    errors = []

    url = SCANNER_VERSION_URLS.get(scanner_approach)
    if url is None:
        # CLI scanner version comes from platform docs, not a separate JSON
        result["fetch_status"] = "not_applicable"
        return result, errors

    content, err = fetch_url(url, timeout)
    if content is None:
        result["fetch_status"] = "error"
        errors.append(f"Scanner version fetch failed: {err}")
        return result, errors

    try:
        data = json.loads(content)
        versions = data.get("versions", [])
        # Find latest non-archived version
        for v in versions:
            if not v.get("archived", False):
                result["version"] = v["version"]
                break
        if result["version"] is None and versions:
            # All archived — use the first one anyway
            result["version"] = versions[0]["version"]
        result["version_source"] = url
        result["fetch_status"] = "ok"
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        result["fetch_status"] = "error"
        errors.append(f"Scanner version parse error: {e}")

    return result, errors


# ---------------------------------------------------------------------------
# Phase 3: Bitbucket pipe versions
# ---------------------------------------------------------------------------


def fetch_bitbucket_pipe_versions(sonarqube_type, timeout=15):
    """Fetch latest Bitbucket pipe versions from the Bitbucket API."""
    pipe_versions = {}
    errors = []

    pipe_urls = BITBUCKET_PIPE_URLS.get(sonarqube_type, {})
    for pipe_name, url in pipe_urls.items():
        content, err = fetch_url(url, timeout)
        if content is None:
            errors.append(f"Bitbucket pipe version fetch failed ({pipe_name}): {err}")
            continue
        try:
            data = json.loads(content)
            values = data.get("values", [])
            if values:
                pipe_versions[pipe_name] = values[0].get("name", "unknown")
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            errors.append(f"Bitbucket pipe version parse error ({pipe_name}): {e}")

    return pipe_versions, errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Fetch SonarQube configuration versions and YAML templates."
    )
    parser.add_argument(
        "--platform",
        required=True,
        choices=["github-actions", "gitlab-ci", "azure-devops", "bitbucket"],
        help="CI/CD platform",
    )
    parser.add_argument(
        "--scanner-approach",
        required=True,
        choices=["maven", "gradle", "dotnet", "cli"],
        help="Scanner approach based on build system",
    )
    parser.add_argument(
        "--sonarqube-type",
        required=True,
        choices=["cloud", "server"],
        help="SonarQube deployment type",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="HTTP timeout in seconds (default: 15)",
    )

    args = parser.parse_args()

    all_errors = []
    all_warnings = []

    # Phase 1: Platform documentation
    platform_result, p_errors, p_warnings = fetch_platform_docs(
        args.platform, args.scanner_approach, args.sonarqube_type, args.timeout
    )
    all_errors.extend(p_errors)
    all_warnings.extend(p_warnings)

    # Phase 2: Scanner version
    scanner_result, s_errors = fetch_scanner_version(args.scanner_approach, args.timeout)
    all_errors.extend(s_errors)

    # Phase 3: Bitbucket pipe versions (only for bitbucket + cli)
    if args.platform == "bitbucket" and args.scanner_approach == "cli":
        pipe_versions, bb_errors = fetch_bitbucket_pipe_versions(
            args.sonarqube_type, args.timeout
        )
        all_errors.extend(bb_errors)
        platform_result["pipe_versions"] = pipe_versions

    output = {
        "platform": platform_result,
        "scanner": scanner_result,
        "errors": all_errors,
        "warnings": all_warnings,
    }

    json.dump(output, sys.stdout, indent=2)
    print()  # trailing newline


if __name__ == "__main__":
    main()
