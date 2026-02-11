---
name: prerequisites-gathering
description: Defines critical prerequisites required before creating SonarQube configurations. Use this to gather SonarQube type, CI/CD platform, branch info, project key, organization, and Cloud instance.
---

# Prerequisites Gathering Skill

This skill defines the critical information needed before creating any SonarQube configuration files.

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

### 3. Current Branch (REQUIRED)
- Use `execute` tool to run: `git branch --show-current`
- If the current branch is NOT `main` or `master`:
  - Add that branch to workflow triggers/pipeline configuration
  - Ensure analysis runs on the current branch
- DO NOT create pipeline files without branch information

### 4. SonarQube Cloud Specific Information (REQUIRED if using Cloud)

**If the user is using SonarQube Cloud, collect:**

**4a. Organization Key (REQUIRED for Cloud)**
- Ask user: "What is your SonarQube Cloud organization key?"
- This is the organization identifier in SonarCloud
- Format: lowercase organization name (e.g., `my-org`, `company-name`)
- DO NOT proceed without this for Cloud users

**4b. SonarQube Cloud Instance (REQUIRED for Cloud)**
- Ask user: "Which SonarQube Cloud instance are you using?"
  - **US**: `sonarcloud.us`
  - **EU**: `sonarcloud.io`
- Default is EU (`sonarcloud.io`) if user is unsure
- This determines the SONAR_HOST_URL value

### 5. Project Key (REQUIRED)
- Ask user for their SonarQube project key
- This uniquely identifies the project in SonarQube
- Format varies by platform:
  - Cloud: Often matches project name or custom format
  - Server: `projectname` or custom format

### 6. Project Type/Build System (REQUIRED)
- Identified through project detection skill
- Determines which scanner to use:
  - Maven projects → Maven plugin
  - Gradle projects → Gradle plugin
  - Other projects → SonarScanner CLI

## Validation Rules

**Efficient Question Asking:**
- ✅ ASK multiple related questions in a single interaction when possible
- ✅ Group SonarQube-related questions together (type, project key, organization)
- ❌ DON'T ask questions one at a time when they can be batched

**If ANY prerequisite is missing:**
- ❌ STOP immediately
- ❌ DO NOT create files with placeholder values
- ❌ DO NOT assume or guess values
- ✅ ASK the user for the missing information
- ✅ WAIT for their response before proceeding

## Order of Operations

1. Analyze project structure (use project-detection skill)
2. Confirm detected CI/CD platform with user
3. **Ask all remaining prerequisites in a single interaction when possible:**
   - SonarQube type (Cloud or Server)?
   - SonarQube project key?
   - If Cloud: Organization key and instance (US/EU)?
4. Detect current branch using `execute` tool
3. **If SonarQube Cloud:**
   - Ask for organization key
   - Ask for Cloud instance (US or EU)
4. Confirm CI/CD platform (if not detected)
5. Detect current branch (use execute tool)
6. Ask for project key
7. Proceed to file creation only when all prerequisites are confirmed
