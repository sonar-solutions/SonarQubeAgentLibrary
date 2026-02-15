---
name: devops-setup-instructions
description: Platform-specific instructions for configuring secrets and variables in CI/CD platforms. Use this to guide users in setting up SONAR_TOKEN and SONAR_HOST_URL.
---

# DevOps Setup Instructions Skill

This skill provides concise, platform-specific instructions for configuring secrets and variables in CI/CD platforms.

## GitHub Actions Setup

### Secret Configuration

**Location:** Repository → Settings → Secrets and variables → Actions

**Required Secrets:**

**For SonarQube Cloud:**
```
SONAR_TOKEN: [your SonarQube Cloud token with analysis permissions]
SONAR_HOST_URL: [https://sonarcloud.io for EU or https://sonarqube.us for US instance]
SONAR_ORGANIZATION: [your organization key]
```

**For SonarQube Server:**
```
SONAR_TOKEN: [your SonarQube Server token with analysis permissions]
SONAR_HOST_URL: [your SonarQube Server URL, e.g., https://sonar.yourcompany.com]
```

### Additional Setup
- Ensure GitHub Actions is enabled for the repository
- Check workflow permissions: Settings → Actions → General → Workflow permissions
- For PR decoration: Configure SonarQube GitHub App integration

---

## GitLab CI Setup

### Variable Configuration

**Location:** Project → Settings → CI/CD → Variables

**Required Variables:**

**For SonarQube Cloud:**
```
SONAR_TOKEN: [your SonarQube Cloud token] - Mark as "Masked" and "Protected"
SONAR_HOST_URL: [https://sonarcloud.io for EU or https://sonarqube.us for US] - Mark as "Protected"
```

**For SonarQube Server:**
```
SONAR_TOKEN: [your SonarQube Server token] - Mark as "Masked" and "Protected"
SONAR_HOST_URL: [your SonarQube Server URL] - Mark as "Protected"
```

### Additional Setup
- Ensure CI/CD pipelines are enabled
- For protected branches, mark variables as "Protected"
- For PR decoration: Configure SonarQube GitLab integration

---

## Azure DevOps Setup

### Variable Configuration

**Location:** Pipelines → Library → Variable groups

**Create a Variable Group named "SonarQube" with:**

**For SonarQube Cloud:**
```
SONAR_TOKEN: [your SonarQube Cloud token] - Mark as "Secret" (lock icon)
(SONAR_HOST_URL is not needed for Cloud)
```

**For SonarQube Server:**
```
SONAR_TOKEN: [your SonarQube Server token] - Mark as "Secret"
SONAR_HOST_URL: [your SonarQube Server URL]
```

**Alternative: Pipeline Variables**
Configure in Pipeline → Edit → Variables

### Additional Setup
- Install SonarQube extension from Azure DevOps Marketplace
- Link variable group to your pipeline
- For SonarQube Server: Create a Service Connection (Project Settings → Service connections → SonarQube)
- For PR decoration: Configure SonarQube Azure DevOps integration

---

## Bitbucket Pipelines Setup

### Variable Configuration

**Location:** Repository settings → Pipelines → Repository variables

**Required Variables:**

**For SonarQube Cloud:**
```
SONAR_TOKEN: [your SonarQube Cloud token] - Mark as "Secured"
```

**For SonarQube Server:**
```
SONAR_TOKEN: [your SonarQube Server token] - Mark as "Secured"
SONAR_HOST_URL: [your SonarQube Server URL]
```

### Additional Setup
- Ensure Pipelines are enabled for the repository
- For workspace-level variables: Settings → Pipelines → Workspace variables
- For PR decoration: Configure SonarQube Bitbucket integration

---

## Jenkins Setup

### Credentials Configuration

**Location:** Manage Jenkins → Manage Credentials

**Required Credentials:**

**For SonarQube Cloud or Server:**
```
Kind: Secret text
ID: sonarqube-token
Secret: [your SonarQube token]
```

### SonarQube Server Configuration

**Location:** Manage Jenkins → Configure System → SonarQube servers

**Add SonarQube Server:**
```
Name: SonarQube (or SonarCloud)
Server URL: [your SonarQube URL or https://sonarcloud.io (EU) / https://sonarqube.us (US)]
Server authentication token: Select the credential created above
```

### Additional Setup
- Install SonarQube Scanner plugin from Jenkins Plugin Manager
- Configure SonarQube Scanner: Manage Jenkins → Global Tool Configuration
- For PR decoration: Install SonarQube Quality Gates plugin

---

## Token Generation Instructions

### SonarQube Cloud (Scoped Organization Tokens)
1. Log in to SonarCloud
2. Retrieve your organization
3. Go to Administration → Scoped Organization Tokens
4. Click the "Create token" button in the top right corner
5. Enter the token name and description (e.g., "GitHub Actions CI")
6. Select "Expires in" duration or "No expiration"
7. Choose "Projects this token can access":
   - **All current and future projects** - Recommended for CI/CD pipelines
   - **Custom selection of projects** - Select specific projects using the "Select projects" button
8. Click "Generate token"
9. Copy the token immediately from the notification (it won't be shown again)

**Note:** Scoped Organization Tokens are identified by the `sqco_` prefix and are available in Team and Enterprise plans.

### SonarQube Server
1. Log in to your SonarQube Server
2. Go to My Account → Security → Generate Tokens
3. Enter token name (e.g., "CI Pipeline")
4. Select token type: "Global Analysis Token" or "Project Analysis Token"
5. Click "Generate"
6. Copy the token immediately (it won't be shown again)

---

## Post-Setup Validation

After configuring secrets/variables, verify:
- [ ] Secrets/variables are marked as protected/secured
- [ ] Token has analysis permissions only (minimal privilege)
- [ ] SONAR_HOST_URL is correct (Server only)
- [ ] Pipeline has access to secrets/variables
- [ ] Run a test pipeline to verify authentication

---

## Instructions Format for Users

When providing setup instructions to users, use this concise format:

```
✅ Configuration files created successfully!

🔐 Next Steps - Configure Secrets in [Platform]:

1. Go to: [exact path in UI]
2. Add the following secrets/variables:
   - SONAR_TOKEN: [description] - [special settings]
   - SONAR_HOST_URL: [description] - [special settings if Server]
3. [Any additional setup steps]

📝 Push your changes and the pipeline will run automatically.
```
