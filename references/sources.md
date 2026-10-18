# Research provenance — inspected 2026-10-18

These sources informed the design. Links do not imply endorsement. The bundled
instructions, helpers, and fixtures were newly drafted for this project; no source
code, complete skill, or transcript was copied from the researched projects.

| Source | Inspected evidence | Design implication |
|---|---|---|
| [Agent Skills specification](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx) | Pinned specification; required metadata and package layout | Small SKILL.md plus optional tools/references; folder/name agreement |
| [Anthropic skill-creator](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/skill-creator/SKILL.md) | Inspected evaluation workflow, not executed or copied | Test realistic outputs; distinguish deterministic tests from model behavior |
| [SkillsBench 1.1](https://www.skillsbench.ai/blogs/skillsbench-1-1), [code](https://github.com/benchflow-ai/skillsbench/releases/tag/v1.1) | Primary benchmark's paired conditions, invocation tracking, and negative task outcomes | Keep scope narrow and do not assume an untested skill improves an agent |
| [Don't Build Agents, Build Skills Instead](https://www.youtube.com/watch?v=CEvIs9y1uog&t=650s), Barry Zhang and Mahesh Murag | Retrieved auto-captions; inspected 03:33–04:51 (scripts and progressive disclosure), 10:49–11:45 (testing/versioning), 12:04–13:11 (distribution) | Ship reusable tools and explicit versions; connect skills through a catalog |
| [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | Primary engineering guidance on outcome/trace checks | Define observable failure signals and disclose evaluation scope |
| [OpenAI: Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | Primary guide to trace and outcome evaluation | Package checks do not demonstrate invocation or task-success improvements |
| [Common Sense v0.1.5](https://github.com/Jhurling2024/common-sense-skill/tree/945ec0456045a9f6d446a02618dce433d40b599b) | Existing release metadata, tests, and published changelog | Match attribution and package records; leave the existing skill unchanged |

The video was researched through auto-captions, not visual playback. Captions are
imperfect; the design choices are corroborated against the specification and code.
No claim of improved model performance is inferred from these sources. Research
snapshots can age; inspect current upstream versions before relying on API details.
