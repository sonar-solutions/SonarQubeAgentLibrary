---
name: security-practices
description: Security requirements and best practices for SonarQube integration. Use this to ensure credentials are never hardcoded and secrets are properly managed.
---

# Security Best Practices Skill

This skill defines security requirements and best practices for SonarQube integration.

## ⚠️ Critical Security Rules

### Never Hardcode Credentials

**FORBIDDEN:**
- ❌ Hardcoding `SONAR_TOKEN` in workflow files
- ❌ Hardcoding `SONAR_HOST_URL` in configuration files
- ❌ Committing tokens to version control
- ❌ Storing credentials in plain text files
- ❌ Using personal tokens for production pipelines

### Always Use Secrets/Variables

**REQUIRED:**
- ✅ Use platform-specific secret management
- ✅ Store `SONAR_TOKEN` as a secret/variable
- ✅ Store `SONAR_HOST_URL` as a secret/variable (Server only)
- ✅ Use minimal privilege tokens (analysis-only permissions)
- ✅ Rotate tokens regularly

## Platform-Specific Secret Management

### GitHub Actions

**Secret Reference Syntax:**
```yaml
env:
  SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
  SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

**Always remind users:**
- Secrets are configured in: Settings → Secrets and variables → Actions
- Repository secrets vs Organization secrets
- Secrets are not visible in logs

### GitLab CI

**Variable Reference Syntax:**
```yaml
variables:
  SONAR_TOKEN: $SONAR_TOKEN
  SONAR_HOST_URL: $SONAR_HOST_URL
```

**Always remind users:**
- Variables are configured in: Settings → CI/CD → Variables
- Mark variables as "Masked" and "Protected"
- Use project variables or group variables

### Azure DevOps

**Variable Reference Syntax:**
```yaml
env:
  SONAR_TOKEN: $(SONAR_TOKEN)
  SONAR_HOST_URL: $(SONAR_HOST_URL)
```

**Always remind users:**
- Variables are configured in: Pipelines → Library → Variable groups
- Mark variables as "Secret"
- Link variable group to pipeline

### Bitbucket Pipelines

**Variable Reference Syntax:**
```yaml
- pipe: sonarsource/sonarcloud-scan:1.0.0
  variables:
    SONAR_TOKEN: $SONAR_TOKEN
```

**Always remind users:**
- Variables are configured in: Repository settings → Pipelines → Repository variables
- Mark variables as "Secured"
- Repository variables vs Workspace variables

## Token Best Practices

### Token Generation

**For SonarQube Cloud:**
- Generate at: Account → Security → Tokens
- Scope: Analysis permissions only
- Expiration: Set appropriate expiration date

**For SonarQube Server:**
- Generate at: My Account → Security → Tokens
- Permissions: Execute Analysis
- User tokens vs Project tokens

### Token Management

**Best practices:**
- 🔐 Use analysis-only scope (minimal privilege)
- ⏰ Set token expiration dates
- 🔄 Rotate tokens regularly
- 📝 Document which token is used where
- 🗑️ Revoke unused tokens immediately
- 👥 Use service accounts for CI/CD (not personal accounts)

## Configuration File Security

### sonar-project.properties

**SAFE:**
```properties
sonar.projectKey=my-project-key
sonar.organization=my-org
sonar.sources=src
```

**UNSAFE:**
```properties
# ❌ NEVER DO THIS
sonar.login=TOKEN_VALUE_HERE
sonar.password=PASSWORD_HERE
```

### Workflow Files

**SAFE:**
```yaml
env:
  SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

**UNSAFE:**
```yaml
# ❌ NEVER DO THIS
env:
  SONAR_TOKEN: "squ_1234567890abcdef"
```

## Security Reminders for Users

Always include these reminders when creating configurations:

```
🔐 Security Setup Required:

1. Generate a token from your SonarQube instance with analysis permissions
2. Add the token as a secret in your CI/CD platform (NEVER commit it)
3. Reference the secret using the appropriate syntax for your platform
4. Use minimal privilege tokens (analysis-only)
5. Set token expiration and rotate regularly
```

## Validation Checklist

Before finalizing any configuration, verify:
- [ ] No hardcoded credentials in any file
- [ ] Secrets are referenced using platform syntax
- [ ] Comments explain how to configure secrets
- [ ] User has been reminded about secret management
- [ ] Token scope is minimal (analysis-only)
