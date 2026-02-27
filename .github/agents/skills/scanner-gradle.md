---
name: scanner-gradle
description: Gradle scanner configuration for SonarQube. Use this for Java/Kotlin projects using Gradle build system. Fetches current plugin version and produces an Output Contract.
---

# Gradle Scanner Skill

## Purpose

Configure SonarQube integration for Gradle projects. This skill reads the `build.gradle` or `build.gradle.kts`, fetches the latest plugin version, verifies or adds required configuration, and produces an Output Contract for the platform skill and pipeline-creation.

## Official Documentation

| SonarQube Type | Documentation URL |
|---|---|
| Cloud | `https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/ci-based-analysis/sonarscanner-for-gradle` |
| Server | `https://docs.sonarsource.com/sonarqube-server/analyzing-source-code/scanners/sonarscanner-for-gradle` |

**Version JSON:**
`https://downloads.sonarsource.com/sonarqube/update/scannergradle.json`

## Documentation Fetching Strategy

| URL pattern | Required tool |
|---|---|
| `docs.sonarsource.com` | Use your environment's **browser-capable fetch tool** (e.g., web/fetch, WebFetch, url_context, or equivalent). **NOT curl.** |
| `downloads.sonarsource.com/sonarqube/update/scannergradle.json` | **curl or wget is acceptable** |

## Processing Steps

Execute these steps in order. Do not skip any step.

**Step 1:** Read the complete build file using the `read` tool.
- Use `build.gradle` (Groovy DSL) or `build.gradle.kts` (Kotlin DSL), whichever is present
- If both exist, use `build.gradle.kts`

**Step 2:** Check for existing SonarQube configuration:
- Look for `id("org.sonarqube")` (Kotlin DSL) or `id 'org.sonarqube'` (Groovy DSL) in the `plugins` block
- Look for a `sonarqube {}` or `sonar {}` configuration block
- Note the current plugin version if present

**Step 3:** ⛔ STOP — Fetch the latest plugin version NOW.

Run: `curl -s https://downloads.sonarsource.com/sonarqube/update/scannergradle.json`

Extract the latest version from the JSON response.

**Completion condition:** Do not proceed to Step 4 until you have the exact version string from the JSON. If the curl command fails, use the browser-capable fetch tool on the Server documentation URL as fallback to find the version in code examples.

**Step 4:** Verify the build file has the correct configuration:
- Plugin declaration uses the version from Step 3
- `sonarqube {}` block has `sonar.projectKey` set (required)
- `sonar.organization` is set (required for Cloud)
- `sonar.coverage.jacoco.xmlReportPaths` is set if JaCoCo is configured

**Step 5:** Update or add configuration as needed. Never duplicate existing properties.

**Step 6:** Populate the Output Contract below.

## Build Commands

Primary build command (with tests and coverage):
```
./gradlew test jacocoTestReport sonar
```

If no coverage is configured:
```
./gradlew sonar
```

**Always use the Gradle wrapper** (`./gradlew`), never a globally installed `gradle` binary.

**Note for multi-module projects:** Run from the root directory containing the root `build.gradle`.

## Plugin Declaration

### Kotlin DSL (`build.gradle.kts`)
```kotlin
plugins {
    id("org.sonarqube") version "X.Y.Z"  // use version from Step 3
    id("jacoco")
}

sonarqube {
    properties {
        property("sonar.projectKey", "YOUR_PROJECT_KEY")
        property("sonar.organization", "YOUR_ORG_KEY")  // Cloud only
        property("sonar.coverage.jacoco.xmlReportPaths", "build/reports/jacoco/test/jacocoTestReport.xml")
    }
}
```

### Groovy DSL (`build.gradle`)
```groovy
plugins {
    id 'org.sonarqube' version 'X.Y.Z'  // use version from Step 3
    id 'jacoco'
}

sonarqube {
    properties {
        property 'sonar.projectKey', 'YOUR_PROJECT_KEY'
        property 'sonar.organization', 'YOUR_ORG_KEY'  // Cloud only
        property 'sonar.coverage.jacoco.xmlReportPaths', 'build/reports/jacoco/test/jacocoTestReport.xml'
    }
}
```

### JaCoCo task finalization (add to test task block)

**Kotlin DSL:**
```kotlin
tasks.test {
    finalizedBy(tasks.jacocoTestReport)
}
tasks.jacocoTestReport {
    dependsOn(tasks.test)
    reports {
        xml.required.set(true)
    }
}
```

**Groovy DSL:**
```groovy
test {
    finalizedBy jacocoTestReport
}
jacocoTestReport {
    dependsOn test
    reports {
        xml.enabled true
    }
}
```

## Output Contract

This contract must be fully populated before pipeline-creation runs. No field may contain "TODO", "fetch from docs", or a placeholder.

```
scanner: gradle
tool_version: [exact version from Step 3, e.g., "5.0.0.4638"]   ← resolved in Step 3
build_commands: ["./gradlew test jacocoTestReport sonar"]
build_file: [path to build.gradle or build.gradle.kts]
dsl_type: [kotlin | groovy]
working_directory: [directory containing build.gradle]
sonar_project_key: [value from prerequisites]
sonar_organization: [value from prerequisites, or "N/A" for Server]
coverage_report_path: [path to jacocoTestReport.xml, or "N/A" if no coverage configured]
required_files: [build.gradle or build.gradle.kts — modified]
```

## Usage Instructions

**For SonarArchitectGuide:** Include documentation links and explain Gradle concepts when relevant.

**For SonarArchitectLight:** Execute all Processing Steps silently. Produce the Output Contract. Do not include links or explanations in responses.
