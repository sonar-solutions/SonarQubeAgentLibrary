---
name: prerequisites-gathering
description: Defines critical prerequisites required before creating SonarQube configurations. Use this to gather SonarQube type, CI/CD platform, branch info, project key, organization, and Cloud instance.
---

# Prerequisites Gathering Skill

This skill defines the critical information needed before creating any SonarQube configuration files.

## ⚠️ CRITICAL: ALWAYS USE THIS SKILL

**This skill MUST be used in EVERY scenario, whether information needs to be gathered OR validated:**

- **Interactive Mode** (can ask questions): Use this skill to ASK for missing prerequisites
- **Validation Mode** (automated/testing with all info provided): Use this skill to VALIDATE all prerequisites are present

**DO NOT skip this skill even if all information appears to be provided upfront. Always validate prerequisites before proceeding.**

## ⚠️ CRITICAL PREREQUISITES

**You MUST collect ALL of the following before creating ANY pipeline configuration files:**

### 1. SonarQube Type (REQUIRED)
- **If not specified by the user**, STOP and ask:
  - "Are you connecting to **SonarQube Cloud** or **SonarQube Server**?"
- This is critical as documentation links and configuration differ between Cloud and Server
- DO NOT proceed until you have this information

### 2. CI/CD Platform (REQUIRED)
- Detect from project structure OR ask the user if unclear
- Supported platforms:
  - GitHub Actions
  - GitLab CI
  - Azure DevOps
  - Bitbucket Pipelines
  - Jenkins
- DO NOT proceed without confirming the platform

### 3. SonarQube Cloud Specific Information (REQUIRED if using Cloud)

**If the user is using SonarQube Cloud, collect:**

**3a. Organization Key (REQUIRED for Cloud)**
- Ask user: "What is your SonarQube Cloud organization key?"
- This is the organization identifier in SonarCloud
- Format: lowercase organization name (e.g., `my-org`, `company-name`)
- DO NOT proceed without this for Cloud users

**3b. SonarQube Cloud Instance (REQUIRED for Cloud)**
- **CRITICAL**: Ask user: "Which SonarQube Cloud instance are you using?"
- **ONLY these two options exist - use them exactly as shown**:
  - **US**: `sonarqube.us` (full URL: https://sonarqube.us)
  - **EU**: `sonarcloud.io` (full URL: https://sonarcloud.io)
- When asking the user, you MUST present these exact values: "US: sonarqube.us or EU: sonarcloud.io"
- Default is EU (`sonarcloud.io`) if user is unsure
- This determines the SONAR_HOST_URL value
- **DO NOT** use any other URLs or variations

### 4. Project Key (REQUIRED)
- Ask user for their SonarQube project key
- This uniquely identifies the project in SonarQube
- Format varies by platform:
  - Cloud: Often matches project name or custom format
  - Server: `projectname` or custom format

### 5. Project Type/Build System (REQUIRED)
- Identified through project detection skill
- Determines which scanner to use:
  - Maven projects → Maven plugin
  - Gradle projects → Gradle plugin
  - Other projects → SonarScanner CLI

## Validation Rules

**Two Modes of Operation:**

1. **Interactive Mode** (when you can ask questions):
   - ✅ ASK multiple related questions in a single interaction when possible
   - ✅ Group SonarQube-related questions together (type, project key, organization)
   - ❌ DON'T ask questions one at a time when they can be batched
   - **If ANY prerequisite is missing:**
     - ❌ STOP immediately
     - ❌ DO NOT create files with placeholder values
     - ❌ DO NOT assume or guess values
     - ✅ ASK the user for the missing information
     - ✅ WAIT for their response before proceeding

2. **Validation Mode** (when all info is provided upfront, e.g., automated testing):
   - ✅ Use this skill to VALIDATE (not skip it)
   - ✅ Check that the initial prompt contains ALL required prerequisites:
     - SonarQube type (Cloud or Server)
     - CI/CD platform
     - Project key
     - If Cloud: Organization key and instance (US/EU)
     - If Server: Server URL
   - ❌ If ANY prerequisite is missing from the prompt, you cannot proceed
   - ✅ Once validated, extract the values and proceed with file creation

**In BOTH modes, this skill serves as your checklist - DO NOT skip it.**

## Order of Operations

1. Analyze project structure (use project-detection skill)
2. Confirm detected CI/CD platform with user
3. **Ask all remaining prerequisites in a single interaction when possible:**
   - SonarQube type (Cloud or Server)?
   - SonarQube project key?
   - If Cloud: Organization key and instance (US/EU)?
4. Proceed to file creation only when all prerequisites are confirmed
