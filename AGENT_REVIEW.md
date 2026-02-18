# Agent & Skills Review

## Architecture (Generally Strong)

The modular skill architecture is well-designed. Separating platform skills from scanner skills from core skills is clean and maintainable. The two-agent approach (action-oriented Light vs. educational Guide) is a good pattern. Prerequisites as a mandatory checklist is solid.

---

## Main Issue: GitHub Copilot-Specific Tool References

This is the central problem for multi-LLM support. Several things are Copilot-specific:

**1. The `tools` frontmatter field**
```yaml
tools: ["read", "search", "edit", "execute"]
```
This is a GitHub Copilot agent format field. Claude, GPT-based agents, Gemini, etc. don't understand this. It's harmless noise for other LLMs but worth knowing.

**2. Tool names used in skill instructions**
- `project-detection.md` line 21: "Use `search` and `read` tools" — `search` is Copilot's file search tool
- `platform-github-actions.md` lines 28 and 109: "Invoke `web/fetch` TOOL" — `web/fetch` is Copilot-specific

**3. Inconsistency between agent and skill on HTTP fetching**
The agent files correctly say "Use HTTP GET requests (curl, wget, or similar)" but `platform-github-actions.md` says "Invoke `web/fetch` TOOL (NOT curl)". The skill directly contradicts the agent. For an LLM that doesn't have `web/fetch`, this instruction either causes failure or gets ignored. The other platform skills don't have this issue — only `platform-github-actions.md` still has the old reference.

---

## Agent File Issues

**SonarArchitectGuide: Name inconsistency**
- Filename: `SonarArchitectGuide.agent.md`
- Frontmatter `name`: `SonarArchitectGuide`
- H1 header: `# SonarArchitect - SonarQube Integration Expert`
- Persona: "You are **SonarArchitect**"
- Welcome message: "I'm SonarArchitect"
- Completion message: "Thank you for using SonarArchitectGuide!"

The agent calls itself "SonarArchitect" in most places but "SonarArchitectGuide" in others. This will confuse both users and the LLM.

**SonarArchitectLight: Broken interaction example**
The example in the `## Interaction Pattern` section has numbering errors — step 6 appears twice, step 8 appears twice, step 13 appears after 14, and there's a scanner-maven reference in what appears to be a Gradle scenario. LLMs that learn from in-context examples will pick up this noise.

**SonarArchitectGuide: No HTTP tool section**
SonarArchitectLight has an explicit "Available Tools" section explaining how to use HTTP clients. SonarArchitectGuide has no equivalent, yet both agents need to fetch scanner versions via HTTP. The Guide will rely on whatever the LLM infers.

---

## Skill-Level Issues

**Old agent names in `scanner-gradle.md`**
The "Usage Instructions" section at the bottom references `SonarArchitectGuideWithSkills` and `SonarArchitectLightWithSkills` — these are old names that don't match the current agent files. Any LLM following those instructions won't match on the correct agent.

**Jenkins is listed but has no skill**
`prerequisites-gathering.md` lists Jenkins as a supported platform, but there is no `platform-jenkins.md` skill. If a user says "Jenkins", the agent will gather prerequisites and then have no skill to execute.

**Server URL not in the prerequisite gathering flow**
The "Validation Mode" checklist in `prerequisites-gathering.md` mentions "If Server: Server URL" as required, but the "Order of Operations" and the interactive questions don't include collecting the Server URL as a step. It would be silently skipped in interactive mode.

**`pipeline-creation.md` has Guide-centric language**
Step 2 of the Editing Workflow says "Explain key configuration options". For the Light agent, this is wrong — Light is supposed to be action-oriented and concise. Since this skill is shared, this instruction leaks verbose behavior into Light.

**Caching typo in `platform-github-actions.md`**
Line 83: `### Caching\`` — there's a backtick at the end of the heading. Small thing but will render oddly in some environments.

---

## Summary Table

| Issue | Severity | Location |
|-------|----------|----------|
| `web/fetch` vs curl inconsistency | High | `platform-github-actions.md` L28, L109 |
| `search` tool name (Copilot-specific) | Medium | `project-detection.md` L21 |
| Agent name inconsistency | Medium | `SonarArchitectGuide.agent.md` throughout |
| Old agent names in skill | Medium | `scanner-gradle.md` Usage Instructions |
| Broken interaction example | Medium | `SonarArchitectLight.agent.md` L218-258 |
| Jenkins listed, no skill exists | Medium | `prerequisites-gathering.md` |
| Server URL missing from interactive flow | Low | `prerequisites-gathering.md` |
| Guide has no HTTP tools section | Low | `SonarArchitectGuide.agent.md` |
| "Explain key options" in shared skill | Low | `pipeline-creation.md` |
| Caching heading backtick typo | Low | `platform-github-actions.md` L83 |
