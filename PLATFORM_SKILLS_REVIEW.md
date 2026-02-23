# Platform Skills Review

## 1. Ideal Common Structure

All `platform-*` skills should follow this section order:

1. YAML frontmatter (`name`, `description`)
2. Intro paragraph (skill scope/purpose)
3. `IMPORTANT - Scope of This Skill` block
4. `## Official Documentation` (Cloud + Server subsections)
5. `## Documentation Fetching Strategy` (JS rendering warning + fallback approach)
6. `## [Platform] Implementation`
   - "Scanner selection" delegation note
   - "When to use [platform CLI tool]" subsection (CLI projects only)
   - "Build Tool Integration" subsection (Maven/Gradle/.NET)
7. `## Platform-Specific Configuration`
   - Secrets/Variables/Service connection setup
   - Checkout/Clone/Git depth config
   - Caching
   - Triggers/Branch config
8. `## Common Configurations` (PR decoration, Quality Gate)
9. `## Best Practices`
10. `## [Tool] Versions` (version-checking guidance)
11. `## Usage Instructions` (Guide + Light subsections)

---

## 2. Section-by-Section Comparison

### Frontmatter & Intro

| Skill | Notes |
|-------|-------|
| `platform-github-actions` | ✅ Consistent |
| `platform-azure-devops` | ✅ Consistent |
| `platform-bitbucket` | ✅ Consistent |
| `platform-gitlab-ci` | ✅ Consistent |

---

### Scope Block (under `IMPORTANT - Scope of This Skill`)

| Skill | 4th bullet wording |
|-------|--------------------|
| `platform-github-actions` | "Access pipeline examples from documentation..." |
| `platform-azure-devops` | ⚠️ "**Fetch** pipeline examples from documentation..." — different verb |
| `platform-bitbucket` | "Access pipeline examples from documentation..." |
| `platform-gitlab-ci` | "Access pipeline examples from documentation..." |

**Action:** Change Azure DevOps 4th bullet to "Access pipeline examples from documentation..." for consistency.

---

### Official Documentation

| Skill | Extra links |
|-------|-------------|
| `platform-github-actions` | ✅ Adds `GitHub Action Repository` link (same URL for Cloud and Server) |
| `platform-azure-devops` | ❌ No extra links |
| `platform-bitbucket` | ✅ Adds `Scan Pipe Repository` + `Quality Gate Pipe` links (different per Cloud/Server) |
| `platform-gitlab-ci` | ❌ No extra links — Docker image source is not linked |

**Action:** GitLab CI should consider linking to the `sonarsource/sonar-scanner-cli` Docker Hub image, consistent with Bitbucket linking to pipe repositories.

---

### `## Prerequisites` Section

| Skill | Has Prerequisites section |
|-------|--------------------------|
| `platform-github-actions` | ❌ Missing |
| `platform-azure-devops` | ✅ Present — documents required Marketplace extension |
| `platform-bitbucket` | ❌ Missing |
| `platform-gitlab-ci` | ❌ Missing |

**Note:** Azure DevOps genuinely requires a mandatory install step (Marketplace extension), which justifies a dedicated Prerequisites section. The other platforms may not need this section, but the structural position of this section in Azure DevOps (between Official Documentation and Documentation Fetching Strategy) is inconsistent with the ideal structure. Consider moving it after Documentation Fetching Strategy, or into Platform-Specific Configuration.

---

### Documentation Fetching Strategy

| Skill | Differences |
|-------|-------------|
| `platform-github-actions` | Standard block |
| `platform-azure-devops` | Standard block |
| `platform-bitbucket` | ⚠️ Adds "(including pipe repository pages)" to the ✅ bullet — valid and useful |
| `platform-gitlab-ci` | Standard block |

**Action:** Consider adding a similar parenthetical to GitHub Actions since it also links to external repositories (the GitHub Action repo).

---

### Implementation Section — CLI Scanner Tool guidance

| Skill | Approach |
|-------|----------|
| `platform-github-actions` | Documents `sonarsource/sonarqube-scan-action` with version-finding instructions embedded inline |
| `platform-azure-devops` | Extension tasks for ALL types — no separate CLI tool subsection needed; uses `## Extension Task Pattern` instead |
| `platform-bitbucket` | Documents named pipes with a YAML example |
| `platform-gitlab-ci` | Documents `sonarsource/sonar-scanner-cli` Docker image with a YAML example |

GitHub Actions is the only one that embeds version-finding instructions inline in this section instead of a dedicated `## [Tool] Versions` section. Azure DevOps has the best pattern for version guidance — a dedicated `## Task Versions` section at the end.

---

### Implementation Section — Build Tool Integration

| Skill | Approach |
|-------|----------|
| `platform-github-actions` | References specific doc section names + hardcodes a Server doc URL inline |
| `platform-azure-devops` | Numbered list per build type with scanner mode specified |
| `platform-bitbucket` | Run commands directly, brief |
| `platform-gitlab-ci` | Run commands directly + specifies Docker images |

**Action:** The hardcoded Server URL in `platform-github-actions` Build Tool Integration is inconsistent with how other skills handle doc references (they rely on the Official Documentation section). Consider removing the inline URL and pointing to the Official Documentation section instead.

---

### Platform-Specific Configuration — Secrets/Variables

| Skill | Section title | Notes |
|-------|--------------|-------|
| `platform-github-actions` | "Secrets Configuration" | Lists `SONAR_TOKEN` + `SONAR_HOST_URL`; cross-references two skills |
| `platform-azure-devops` | "Service Connection Setup" + "Variable Configuration (Alternative)" | Two subsections — Service connection is preferred, variables are fallback |
| `platform-bitbucket` | "Repository Variables" | Lists `SONAR_TOKEN`, `SONAR_HOST_URL`, `SONAR_PROJECT_KEY` (optional); cross-references two skills |
| `platform-gitlab-ci` | "Variables Configuration" | Lists `SONAR_TOKEN` + `SONAR_HOST_URL`; cross-references two skills |

**Note:** Bitbucket is the only one that mentions `SONAR_PROJECT_KEY` as an optional variable. Consider whether this is relevant for the other platforms too.

---

### Platform-Specific Configuration — Checkout/Git Depth

| Skill | Setting name | Notes |
|-------|-------------|-------|
| `platform-github-actions` | `fetch-depth: 0` | Also specifies `actions/checkout@v4` |
| `platform-azure-devops` | `fetchDepth: 0` | Azure YAML syntax difference — correct |
| `platform-bitbucket` | `depth: full` | Different concept — `clone.depth: full` |
| `platform-gitlab-ci` | `GIT_DEPTH: "0"` | GitLab variable syntax — correct |

These differences are platform-correct; no change needed. They should all explain *why* (full git history for accurate blame) consistently. GitHub Actions is the only one with the parenthetical "(accurate blame information)" — add this to the other three.

---

### Platform-Specific Configuration — Caching

| Skill | Cache path | Notes |
|-------|-----------|-------|
| `platform-github-actions` | `~/.sonar/cache` | Specifies `actions/cache@v4` |
| `platform-azure-devops` | ❌ Not mentioned | Missing section |
| `platform-bitbucket` | `.sonar/cache` | Also mentions build dependency caching; uses `definitions.caches` |
| `platform-gitlab-ci` | `.sonar/cache` | Basic mention |

**Action:** Add a Caching subsection to `platform-azure-devops` covering `~/.sonar/cache`.

---

### Common Configurations — Order

| Skill | Order |
|-------|-------|
| `platform-github-actions` | PR Decoration → Quality Gate |
| `platform-azure-devops` | ⚠️ Quality Gate → PR Decoration (reversed) |
| `platform-bitbucket` | PR Decoration → Quality Gate |
| `platform-gitlab-ci` | PR Decoration → Quality Gate |

**Action:** Reorder Azure DevOps Common Configurations to PR Decoration first, Quality Gate second.

---

### Best Practices — Count & Coverage

| Skill | Count | Notable items |
|-------|-------|---------------|
| `platform-github-actions` | 4 | Matrix builds, branch protection, permissions |
| `platform-azure-devops` | 5 | Service connection, separate jobs |
| `platform-bitbucket` | 6 | Pipes vs direct scanner, quality gate step |
| `platform-gitlab-ci` | 5 | Pinned Docker image versions |

**Action:** GitHub Actions is missing a best practice about not running analysis in matrix builds — this is already mentioned in the section but should be confirmed in Best Practices. Consider aligning count and coverage across all skills.

---

### Version Guidance Section

| Skill | Has dedicated section | Approach |
|-------|----------------------|---------|
| `platform-github-actions` | ❌ Inline in "When to Use" | References specific doc section |
| `platform-azure-devops` | ✅ `## Task Versions` | Explains format + browser fetch |
| `platform-bitbucket` | ❌ Only in Best Practices | One-liner |
| `platform-gitlab-ci` | ❌ Missing entirely | Uses `:latest` anti-pattern in examples |

**Action:**
- Add `## Action Version` section to `platform-github-actions`
- Add `## Pipe Versions` section to `platform-bitbucket`  
- Add `## Image Versions` section to `platform-gitlab-ci` and stop using `:latest` in examples

---

### Usage Instructions — Format

| Skill | Format |
|-------|--------|
| `platform-github-actions` | ⚠️ Mixed: ⚠️ callout at top + a single combined block (not clearly split) |
| `platform-azure-devops` | ✅ Two clearly labeled subsections (Guide / Light) |
| `platform-bitbucket` | ✅ Two clearly labeled subsections (Guide / Light) |
| `platform-gitlab-ci` | ✅ Two clearly labeled subsections (Guide / Light) |

**Action:** Refactor `platform-github-actions` Usage Instructions to match the two-subsection format. Move the ⚠️ reminder into the Light subsection (or remove it — the agent config already handles this reminder).

---

### Usage Instructions — Output File Action (Light section)

| Skill | Explicit filename in Light section |
|-------|------------------------------------|
| `platform-github-actions` | ✅ `.github/workflows/sonarqube.yml` mentioned — but in main body, not Light section |
| `platform-azure-devops` | ✅ `azure-pipelines.yml` in Light section |
| `platform-bitbucket` | ✅ `bitbucket-pipelines.yml` in Light section |
| `platform-gitlab-ci` | ✅ `.gitlab-ci.yml` in Light section |

**Action:** Move the filename reference in `platform-github-actions` from the main body into the Light section (consistent with others).

---

## 3. Summary of Actionable Changes

### `platform-github-actions.md`
- [ ] Refactor `## Usage Instructions` into two clear subsections (Guide / Light)
- [ ] Move output filename (`.github/workflows/sonarqube.yml`) into the Light subsection
- [ ] Remove inline hardcoded Server doc URL from Build Tool Integration; replace with reference to Official Documentation section
- [ ] Add dedicated `## Action Version` section (following Azure DevOps `## Task Versions` pattern)
- [ ] Add "(accurate blame information)" to checkout `fetch-depth: 0` note

### `platform-azure-devops.md`
- [ ] Change 4th Scope bullet verb from "Fetch" to "Access"
- [ ] Add `## Caching` subsection to Platform-Specific Configuration
- [ ] Reorder Common Configurations: PR Decoration first, Quality Gate second
- [ ] Move `## Prerequisites` section to after `## Documentation Fetching Strategy`

### `platform-bitbucket.md`
- [ ] Add dedicated `## Pipe Versions` section (following Azure DevOps `## Task Versions` pattern)
- [ ] Add "(accurate blame information)" to clone depth note
- [ ] Review Best Practices for consolidation (6 items vs 4-5 in others)

### `platform-gitlab-ci.md`
- [ ] Add dedicated `## Image Versions` section and stop using `:latest` in examples
- [ ] Replace deprecated `only` keyword references with `rules` (current GitLab best practice)
- [ ] Add "(accurate blame information)" to `GIT_DEPTH: "0"` note
- [ ] Consider linking to the `sonarsource/sonar-scanner-cli` Docker Hub image in Official Documentation

### All skills
- [ ] Standardize "why" explanation for full git history setting (blame information)
- [ ] Confirm whether `SONAR_PROJECT_KEY` as optional variable is relevant across all platforms (currently only Bitbucket)