---
name: devops-setup-instructions
description: Platform-specific instructions for configuring secrets and variables in CI/CD platforms after pipeline files have been created.
---

# DevOps Setup Instructions Skill

Use `security-practices` as the canonical reference for variable syntax in pipeline files.
This skill focuses on UI navigation, required variable names, and flags.

## GitHub Actions

**Location:** Repository → Settings → Secrets and variables → Actions → New repository secret

**Required secrets:**

| Secret name | Value | When required |
|---|---|---|
| `SONAR_TOKEN` | SonarQube analysis token | Always |
| `SONAR_HOST_URL` | `https://sonarcloud.io` (EU) or `https://sonarqube.us` (US) or your Server URL | Cloud (use the instance URL) and Server |

**Notes:**
- The organization key goes in your configuration files (`sonar.organization`), **not** in secrets
- Ensure GitHub Actions is enabled: Settings → Actions → General → Allow all actions
- If you provide YAML examples, read `security-practices.md` first and use that syntax

---

## GitLab CI

**Location:** Project → Settings → CI/CD → Variables → Add variable

**Required variables:**

| Variable name | Value | Flags | When required |
|---|---|---|---|
| `SONAR_TOKEN` | SonarQube analysis token | Masked, Protected | Always |
| `SONAR_HOST_URL` | Cloud instance URL or Server URL | Protected | Always |

**Notes:**
- Mark `SONAR_TOKEN` as **Masked** so it never appears in job logs
- Mark both variables as **Protected** so they are available on protected branches only
- For merge request pipelines, ensure variables are available on unprotected branches if needed
- If you provide `.gitlab-ci.yml` examples, read `security-practices.md` first and use that syntax

---

## Azure DevOps

**Option A — Variable Group (recommended):**

**Location:** Pipelines → Library → + Variable group

Create a group named `SonarQube` with:

| Variable name | Value | Flags | When required |
|---|---|---|---|
| `SONAR_TOKEN` | SonarQube analysis token | Secret (lock icon) | Always |
| `SONAR_HOST_URL` | Cloud instance URL or Server URL | — | Always |

Then link the group to your pipeline: Pipeline → Edit → Variables → Variable groups → Link variable group.

**Option B — Pipeline Variables:**

Pipeline → Edit → Variables → add `SONAR_TOKEN` (mark as secret) and `SONAR_HOST_URL`.
- If you provide YAML examples, read `security-practices.md` first and use Azure syntax from that skill

**Additional setup for Server:**
- Project Settings → Service connections → New service connection → SonarQube
- Enter your Server URL and token; name the connection (e.g., `SonarQube-Connection`)
- Reference this connection name in `SonarQubePrepare@6` task configuration

**Extension required:**
- Install the **SonarQube** extension from Azure DevOps Marketplace before running the pipeline

---

## Bitbucket Pipelines

**Location:** Repository settings → Pipelines → Repository variables

**Required variables:**

| Variable name | Value | Flags | When required |
|---|---|---|---|
| `SONAR_TOKEN` | SonarQube analysis token | Secured | Always |
| `SONAR_HOST_URL` | Cloud instance URL or Server URL | Secured | Always |

**Notes:**
- Mark all variables as **Secured** so they are masked in logs
- For workspace-level variables: Workspace settings → Pipelines → Workspace variables
- If you provide `bitbucket-pipelines.yml` examples, read `security-practices.md` first and use that syntax

---

## Token Generation

### SonarQube Cloud — Scoped Organization Token

1. Log in to your SonarQube Cloud instance (sonarcloud.io or sonarqube.us)
2. Go to your organization → Administration → Scoped Organization Tokens
3. Click **Create token**
4. Enter a descriptive name (e.g., `GitHub Actions CI — my-project`)
5. Set an expiration date
6. Under "Projects this token can access," select **All current and future projects** (for shared CI) or a custom selection
7. Click **Generate token**
8. Copy the token immediately — it will not be shown again

*Scoped Organization Tokens are prefixed with `sqco_` and require Team or Enterprise plan.*

### SonarQube Server

1. Log in to your SonarQube Server instance
2. Go to My Account → Security → Generate Tokens
3. Enter a descriptive token name (e.g., `CI Pipeline — my-project`)
4. Select token type: **Global Analysis Token** or **Project Analysis Token**
5. Set an expiration date
6. Click **Generate**
7. Copy the token immediately — it will not be shown again

---

## Post-Setup Checklist

- [ ] `SONAR_TOKEN` is stored as a secret/masked variable — never visible in logs
- [ ] `SONAR_HOST_URL` is set correctly (Cloud instance URL or Server URL)
- [ ] Token has analysis-only permissions
- [ ] Pipeline has access to the secrets (variable group linked, branch policies allow it)
