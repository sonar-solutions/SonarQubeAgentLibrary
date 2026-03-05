---
name: scanner-maven
description: Maven scanner configuration for SonarQube. Use this for Java/Kotlin projects using Maven build system. Fetches current plugin version and produces an Output Contract.
---

# Maven Scanner Skill

## Purpose

Configure SonarQube integration for Maven projects. This skill reads `pom.xml`, fetches the latest scanner version, verifies or adds required configuration, and produces an Output Contract for the platform skill and pipeline-creation.

## Official Documentation

| SonarQube Type | Documentation URL |
|---|---|
| Cloud | `https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/sonarscanner-for-maven` |
| Server | `https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonarscanner-for-maven` |

**Version JSON:**
`https://downloads.sonarsource.com/sonarqube/update/scannermaven.json`

## Documentation Fetching Strategy

| URL pattern | Required tool |
|---|---|
| `docs.sonarsource.com` | Append `.md` to the URL and fetch with **curl** (e.g., `curl "https://docs.sonarsource.com/...page.md"`) — returns the full page content as Markdown |
| `downloads.sonarsource.com/sonarqube/update/scannermaven.json` | **curl or wget is acceptable** |

## Processing Steps

Execute these steps in order. Do not skip any step.

**Step 1:** Read the complete `pom.xml` file using the `read` tool.

**Step 2:** Check for existing SonarQube configuration:
- Look for `sonar-maven-plugin` in `<plugins>` or `<pluginManagement>`
- Look for `<sonar.*>` properties in the `<properties>` section
- Note the current plugin version if present

**Step 3:** ⛔ STOP — Fetch the latest plugin version NOW.

Run: `curl -s https://downloads.sonarsource.com/sonarqube/update/scannermaven.json`

Extract the latest version from the JSON response.

**Completion condition:** Do not proceed to Step 4 until you have the exact version string from the JSON. If the curl command fails, fetch the Server documentation URL with `.md` appended and extract the version from code examples as fallback.

**Step 4:** Verify `pom.xml` has the correct configuration:
- `sonar.projectKey` is set (required)
- `sonar.organization` is set (required for Cloud)
- `sonar.coverage.jacoco.xmlReportPaths` is set if JaCoCo is configured
- Plugin version matches the latest version from Step 3

**Step 5:** Update or add configuration as needed. Never duplicate existing properties.

**Step 6:** Populate the Output Contract below.

## Build Commands

Primary build command (with tests and coverage):
```
mvn clean verify sonar:sonar
```

If a Maven wrapper is present (`mvnw`), use:
```
./mvnw clean verify sonar:sonar
```

**Note for multi-module projects:** Run from the parent directory containing the root `pom.xml`.

## Configuration Requirements

### pom.xml plugin declaration (add if not present)
```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.sonarsource.scanner.maven</groupId>
      <artifactId>sonar-maven-plugin</artifactId>
      <version>X.Y.Z</version>  <!-- use version from Step 3 -->
    </plugin>
  </plugins>
</build>
```

### pom.xml properties (in `<properties>` section)
```xml
<sonar.projectKey>YOUR_PROJECT_KEY</sonar.projectKey>
<sonar.organization>YOUR_ORG_KEY</sonar.organization>  <!-- Cloud only -->
<sonar.coverage.jacoco.xmlReportPaths>
  ${project.build.directory}/site/jacoco/jacoco.xml
</sonar.coverage.jacoco.xmlReportPaths>
```

### Coverage (JaCoCo)
Add JaCoCo plugin to `pom.xml` if test coverage is needed:
```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <executions>
    <execution>
      <id>prepare-agent</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <id>report</id>
      <phase>test</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

## Output Contract

This contract must be fully populated before pipeline-creation runs. No field may contain "TODO", "fetch from docs", or a placeholder.

```
scanner: maven
tool_version: [exact version from Step 3, e.g., "4.0.0.4121"]   ← resolved in Step 3
build_commands: ["mvn clean verify sonar:sonar"]
build_file: [path to pom.xml, e.g., "pom.xml" or "backend/pom.xml"]
working_directory: [directory containing pom.xml]
sonar_project_key: [value from prerequisites]
sonar_organization: [value from prerequisites, or "N/A" for Server]
coverage_report_path: [path to jacoco.xml, or "N/A" if no coverage configured]
required_files: [pom.xml — modified]
```

## Usage Instructions

**For SonarArchitect:** Execute all Processing Steps silently. Produce the Output Contract. Do not include links or explanations in responses.
