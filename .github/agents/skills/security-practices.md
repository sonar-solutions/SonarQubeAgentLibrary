---
name: security-practices
description: Security requirements and best practices for SonarQube integration. Apply this skill when creating or validating any configuration file to ensure credentials are never hardcoded.
---

# Security Practices Skill

## Critical Rules

- **Never hardcode credentials** in any file, including pipeline YAML, properties files, or build scripts
- **Never commit tokens** to version control under any circumstances
- **Always use platform secret management** — reference secrets via platform-specific variable syntax
- **Use analysis-only token scope** — never use admin or broader-scoped tokens for CI/CD pipelines
- **Set token expiration** — tokens should not be permanent; set appropriate expiration dates
- **Rotate tokens regularly** — rotate and revoke tokens on a schedule

## Platform Secret Patterns

Use the exact syntax for the target platform. Using the wrong syntax silently breaks pipelines.

| Platform | SONAR_TOKEN syntax | SONAR_HOST_URL syntax |
|---|---|---|
| GitHub Actions | `${{ secrets.SONAR_TOKEN }}` | `${{ secrets.SONAR_HOST_URL }}` |
| GitLab CI | `$SONAR_TOKEN` | `$SONAR_HOST_URL` |
| Azure DevOps | `$(SONAR_TOKEN)` | `$(SONAR_HOST_URL)` |
| Bitbucket Pipelines | `$SONAR_TOKEN` | `$SONAR_HOST_URL` |

## Safe vs Unsafe Examples

### GitHub Actions

**Safe:**
```yaml
env:
  SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
  SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

**Unsafe — never do this:**
```yaml
env:
  SONAR_TOKEN: "squ_1234567890abcdef"
  SONAR_HOST_URL: "https://sonar.mycompany.com"
```

---

### GitLab CI

**Safe:**
```yaml
variables:
  SONAR_TOKEN: $SONAR_TOKEN
  SONAR_HOST_URL: $SONAR_HOST_URL
```

**Unsafe — never do this:**
```yaml
variables:
  SONAR_TOKEN: "squ_1234567890abcdef"
```

---

### Azure DevOps

**Safe:**
```yaml
env:
  SONAR_TOKEN: $(SONAR_TOKEN)
  SONAR_HOST_URL: $(SONAR_HOST_URL)
```

**Unsafe — never do this:**
```yaml
env:
  SONAR_TOKEN: "squ_1234567890abcdef"
```

---

### Bitbucket Pipelines

**Safe:**
```yaml
- pipe: sonarsource/sonarcloud-scan:2.0.0
  variables:
    SONAR_TOKEN: $SONAR_TOKEN
```

**Unsafe — never do this:**
```yaml
- pipe: sonarsource/sonarcloud-scan:2.0.0
  variables:
    SONAR_TOKEN: "squ_1234567890abcdef"
```

---

### sonar-project.properties

**Safe:**
```properties
sonar.projectKey=my-project
sonar.organization=my-org
sonar.sources=src
```

**Unsafe — never do this:**
```properties
sonar.token=squ_1234567890abcdef
sonar.host.url=https://sonar.mycompany.com
```

## Token Best Practices

- **Scope:** Use analysis-only tokens (Global Analysis Token or Project Analysis Token); never use user credentials
- **Expiration:** Set an expiration date appropriate to your rotation schedule
- **Rotation:** Revoke and regenerate tokens on a regular schedule
- **Naming:** Use descriptive token names (e.g., "GitHub Actions CI — my-project") so you can identify and revoke specific tokens
- **Service accounts:** Use a dedicated CI service account, not a personal user account, for CI/CD pipelines

## Validation Checklist

Before finalizing any configuration file, verify:

- [ ] No hardcoded tokens or passwords in any file
- [ ] Secrets are referenced using the correct platform syntax (see table above)
- [ ] `sonar-project.properties` does not contain `sonar.token` or `sonar.password`
- [ ] Pipeline files do not echo or log token values
- [ ] Token scope is analysis-only (not admin)
