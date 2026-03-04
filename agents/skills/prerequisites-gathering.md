---
name: prerequisites-gathering
description: Validates or collects all required inputs before any file creation. ALWAYS run this skill after project-detection and before any platform or scanner skill.
---

# Prerequisites Gathering Skill

## Purpose

Validate or collect all required inputs before creating any SonarQube configuration files. This skill runs in two modes:

- **Validation Mode** — all prerequisites were provided upfront (e.g., automated testing); verify they are all present and correct
- **Interactive Mode** — some prerequisites are missing; ask for all missing values in a single interaction

Never skip this skill. Never create files before this skill has confirmed every required field.

## CRITICAL: Always Run

Run this skill after project-detection in every scenario, regardless of how much information was already provided. In validation mode it serves as a checklist; in interactive mode it drives the question sequence.

## Required Prerequisites

### 1. SonarQube Type (REQUIRED)
- **Cloud** or **Server**
- This is critical: documentation links, configuration properties, and required fields differ between Cloud and Server
- Do not proceed without this value

### 2. CI/CD Platform (REQUIRED)
- Detected by project-detection skill, then confirmed by the user
- Supported values: GitHub Actions, GitLab CI, Azure DevOps, Bitbucket Pipelines
- Jenkins is not supported — if the user requests Jenkins, explain it is out of scope and ask them to choose a supported platform

### 3. Project Key (REQUIRED)
- The unique identifier for the project in SonarQube
- Cloud format: often `organization_repository` or custom
- Server format: custom string, typically the project name

### 4. Organization Key (REQUIRED for Cloud only)
- The organization identifier in SonarQube Cloud
- Format: lowercase slug (e.g., `my-org`, `company-name`)
- Not applicable for Server

### 5. Cloud Instance (REQUIRED for Cloud only)
- Which SonarQube Cloud instance the user is on
- **Only two valid values — present these exactly:**
  - **US:** `sonarqube.us` (full URL: `https://sonarqube.us`)
  - **EU:** `sonarcloud.io` (full URL: `https://sonarcloud.io`)
- Default if user is unsure: EU (`sonarcloud.io`)
- This value determines the `SONAR_HOST_URL`

### 6. Server URL (REQUIRED for Server only)
- The full URL of the SonarQube Server instance
- Example: `https://sonar.yourcompany.com`
- Must include the scheme (`https://`)
- This value is used as `SONAR_HOST_URL` in all configuration files

## Order of Operations

1. **Check what is already provided** — review the conversation context for any of the required fields above
2. **Confirm the CI/CD platform** — based on project-detection output, ask the user to confirm (or correct) the detected platform
3. **Batch all remaining questions in ONE interaction** — do not ask field by field; compose a single message listing all missing values needed
4. **Validate all confirmed values** — verify formats are correct (e.g., URL starts with `https://`, project key is not empty)
5. **Block until complete** — do not proceed to any platform or scanner skill until all required fields for the detected SonarQube type are confirmed

## Validation Mode Checklist

When all information is provided upfront, verify each field is present:

- [ ] SonarQube type: Cloud or Server
- [ ] CI/CD platform: github-actions | gitlab-ci | azure-devops | bitbucket
- [ ] Project key: non-empty string
- [ ] Organization key: non-empty string *(Cloud only)*
- [ ] Cloud instance: `sonarqube.us` or `sonarcloud.io` *(Cloud only)*
- [ ] Server URL: starts with `https://` *(Server only)*

If any required field is missing, switch to Interactive Mode immediately.

## Interactive Mode Question Template

When prerequisites are missing, ask all questions in a single message. Example for a Gradle + GitHub Actions project where SonarQube type is unknown:

```
To set up your SonarQube analysis, I need a few details:

1. Are you using **SonarQube Cloud** or **SonarQube Server**?
2. What is your **SonarQube project key**?
3. *(If Cloud)* What is your **organization key**?
4. *(If Cloud)* Which instance are you on — **US: sonarqube.us** or **EU: sonarcloud.io**?
5. *(If Server)* What is your **SonarQube Server URL**? (e.g., https://sonar.yourcompany.com)
```

Adjust which questions appear based on what is already known. Never ask a question that has already been answered.
