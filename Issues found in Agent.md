**Issues found in Agent**

In .github/agents/SonarArchitect.agent.md:

> +- Build system and primary language
+- CI/CD platform from existing pipeline files
+- Existing SonarQube configuration
+
+Report findings to the user using the Detection Output fields from the skill. Ask the user to confirm the detected CI/CD platform before proceeding.
+
+**Wait for user confirmation before proceeding to Step 2.**
+
+---
+
+### Step 2 — Gather Prerequisites
+
+🔧 Using skill: prerequisites-gathering
+
+Run this skill in the appropriate mode:
+- **Validation Mode** if all 6 prerequisite fields were provided upfront
Impossible prerequisite count prevents validation mode
Medium Severity

The agent specifies "Validation Mode if all 6 prerequisite fields were provided upfront," but 6 fields can never all be present simultaneously. Fields 4–5 (Organization Key, Cloud Instance) are Cloud-only, while field 6 (Server URL) is Server-only. Cloud requires at most 5 fields; Server requires 4. This condition can never be satisfied, so the agent would never enter validation mode (used for automated testing scenarios where all info is provided upfront).

Additional Locations (1)
.github/agents/skills/prerequisites-gathering.md#L64-L76

--------------------------------------------------------------------------------------------------------

In .github/agents/skills/security-practices.md:

>  
-1. Generate a token from your SonarQube instance with analysis permissions
-2. Add the token as a secret in your CI/CD platform (NEVER commit it)
-3. Reference the secret using the appropriate syntax for your platform
-4. Use minimal privilege tokens (analysis-only)
-5. Set token expiration and rotate regularly
+**Unsafe — never do this:**
+```properties
+sonar.token=squ_1234567890abcdef
+sonar.host.url=https://sonar.mycompany.com
Security example incorrectly marks host URL as unsafe
Medium Severity

The "Unsafe — never do this" example for sonar-project.properties includes sonar.host.url=https://sonar.mycompany.com alongside a hardcoded token. But sonar.host.url is not a secret — it's a standard configuration property. The scanner-cli.md template explicitly includes sonar.host.url in its properties file template, and the validation checklist only prohibits sonar.token/sonar.password. This contradiction could cause the agent to omit sonar.host.url from properties files or flag valid configurations as insecure.

--------------------------------------------------------------------------------------------------------

In .github/agents/skills/scanner-cli.md:

> +sonar_project_key: [value from prerequisites]
+sonar_organization: [value from prerequisites, or "N/A" for Server]
+sonar_host_url: [resolved instance URL or Server URL]
+sources_path: [e.g., "src"]
+coverage_property: [language-specific property name, or "N/A" if not configured]
+coverage_report_path: [e.g., "coverage/lcov.info", or "N/A" if not configured]
+required_files:
+  - sonar-project.properties (create or update)
+  - [list of additional files modified]
+sonar_project_properties_content: |
+  sonar.projectKey=ACTUAL_VALUE
+  sonar.organization=ACTUAL_VALUE    # Cloud only
+  sonar.host.url=ACTUAL_VALUE
+  sonar.sources=ACTUAL_VALUE
+  [other properties]
+```
CLI scanner Output Contract missing working_directory field
Medium Severity

The pipeline-creation skill lists working_directory as a required field from every scanner Output Contract. The scanner-maven, scanner-gradle, and scanner-dotnet contracts all include it, but scanner-cli's Output Contract omits it entirely. When the sonar-project.properties file is in a subdirectory (e.g., frontend/), the CI/CD pipeline needs to set the working directory accordingly, but pipeline-creation has no value to use.

Additional Locations (1)
.github/agents/skills/pipeline-creation.md#L34-L41

--------------------------------------------------------------------------------------------------------

In .github/agents/skills/platform-bitbucket.md:

>  
-**Fallback Approach:**
-- If working with SonarQube Cloud, first fetch from the Cloud documentation URL
-- If the Cloud documentation lacks complete pipeline examples, also fetch from the Server documentation URL as a fallback
-- If working with SonarQube Server, first fetch from the Server documentation URL
-- If the Server documentation lacks complete pipeline examples, also fetch from the Cloud documentation URL as a fallback
-- Adapt any server-specific or cloud-specific details when using fallback documentation
+**Never use curl to access bitbucket.org.** Those pages require JavaScript rendering; only a browser-capable fetch tool can retrieve them correctly.
Bitbucket CLI scanner version unfetchable without browser tool
Medium Severity

The Bitbucket platform skill requires a "browser-capable fetch tool" (not curl) to access bitbucket.org pipe repository pages for CLI scanner version resolution. But the new agent's tool list is ["read", "edit", "execute"] — web/fetch was removed in this redesign. For Bitbucket + CLI scanner projects (JS, TS, Python, etc.), the agent cannot fetch the pipe version, causing the Processing Steps to halt at the completion condition every time.

Additional Locations (1)
.github/agents/SonarArchitect.agent.md#L3-L4