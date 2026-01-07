# Implementation Plan

> **Session**: `2026-01-06_browser-mcp-skill_b7k2m9`
> **Status**: Complete
> **Spec**: [./spec.md](./spec.md)
> **Created**: 2026-01-06
> **Updated**: 2026-01-07

---

## Overview

- **Checkpoints**: 4 (0 complete)
- **Total Tasks**: 17

## ⬜ Checkpoint 1: Base Skill with Cookbook Structure

**Goal**: Create the browser-mcp skill entry point (SKILL.md) with cookbook routing pattern. Establishes how to use Browser MCP tools in general, and routes to specific workflows for debugging and design critique.

### File Context

| State | File | Status | Description |
|-------|------|--------|-------------|
| Before | `.claude/skills/prompt-writing/SKILL.md` | 📄 exists | Example cookbook-style skill to follow |
| Before | `.claude/skills/git/SKILL.md` | 📄 exists | Example simple skill structure |
| After | `.claude/skills/browser-mcp/SKILL.md` | ✨ new | Browser MCP skill with tools reference, general usage, and cookbook routing |

**Projected Structure**:
```
.claude/skills/browser-mcp/
└── SKILL.md
```

### Testing Strategy

**Approach**: Structure validation

**Verification Steps**:
- [ ] `Verify SKILL.md has proper frontmatter (name, description)`
- [ ] `Verify tools reference table lists all Browser MCP tools`
- [ ] `Verify cookbook section routes to workflow files (even if not yet created)`
- [ ] `Verify general browser usage guidance is included`

### ⬜ Task Group 1.1: Create skill directory and SKILL.md file

**Objective**: Create the browser-mcp skill directory and the main SKILL.md entry point file with proper frontmatter and structure

#### ⬜ Task 1.1.1: Create SKILL.md with frontmatter and purpose section

**File**: `.claude/skills/browser-mcp/SKILL.md`

**Description**: Create the browser-mcp skill entry point file. Include YAML frontmatter with name and description (following git/SKILL.md pattern), a Purpose section explaining this skill enables browser automation via MCP, and a Variables section for SKILL_ROOT.

**Context to Load**:
- `.claude/skills/git/SKILL.md` (lines 1-20) - Example frontmatter and structure
- `.claude/skills/prompt-writing/SKILL.md` (lines 1-40) - Example cookbook-style skill with variables

**Actions**:
- ⬜ **1.1.1.1**: CREATE FILE .claude/skills/browser-mcp/SKILL.md (`.claude/skills/browser-mcp/SKILL.md`)
- ⬜ **1.1.1.2**: ADD frontmatter with name: browser-mcp, description: Browser automation via MCP for debugging and design critique (`.claude/skills/browser-mcp/SKILL.md`)
- ⬜ **1.1.1.3**: ADD Purpose section explaining browser MCP enables direct access to user's Chrome browser (`.claude/skills/browser-mcp/SKILL.md`)
- ⬜ **1.1.1.4**: ADD Variables section with SKILL_ROOT: .claude/skills/browser-mcp/ (`.claude/skills/browser-mcp/SKILL.md`)

### ⬜ Task Group 1.2: Add tools reference section

**Objective**: Document all Browser MCP tools in a reference table with their purposes

#### ⬜ Task 1.2.1: Add Browser MCP tools reference table

**File**: `.claude/skills/browser-mcp/SKILL.md`

**Description**: Add a Tools section with a markdown table listing all Browser MCP tools from the spec: browser_navigate, browser_go_back, browser_go_forward, browser_snapshot, browser_click, browser_hover, browser_type, browser_select_option, browser_press_key, browser_wait, browser_get_console_logs, browser_screenshot. Include purpose for each.

**Context to Load**:
- `agents/sessions/2026-01-06_browser-mcp-skill_b7k2m9/spec.md` (lines 275-295) - Browser MCP tools table from spec

**Depends On**: Tasks 1.1.1

**Actions**:
- ⬜ **1.2.1.1**: ADD ## Tools section header (`.claude/skills/browser-mcp/SKILL.md`)
- ⬜ **1.2.1.2**: ADD markdown table with columns: Tool, Purpose (`.claude/skills/browser-mcp/SKILL.md`)
- ⬜ **1.2.1.3**: ADD all 12 Browser MCP tools with descriptions from spec (`.claude/skills/browser-mcp/SKILL.md`)

### ⬜ Task Group 1.3: Add general usage guidance

**Objective**: Explain how Browser MCP works (connects to real Chrome, auth handled) and when to use it

#### ⬜ Task 1.3.1: Add key differentiator and usage guidance

**File**: `.claude/skills/browser-mcp/SKILL.md`

**Description**: Add a section explaining the key differentiator: Browser MCP connects to user's ACTUAL Chrome browser (not Selenium/Puppeteer). Auth is already handled. Explain when to use: front-end debugging, design critique, any task needing visual reference to user's screen.

**Context to Load**:
- `agents/sessions/2026-01-06_browser-mcp-skill_b7k2m9/spec.md` (lines 275-280) - Key differentiator explanation from spec

**Depends On**: Tasks 1.2.1

**Actions**:
- ⬜ **1.3.1.1**: ADD ## Key Differentiator section explaining real Chrome connection (`.claude/skills/browser-mcp/SKILL.md`)
- ⬜ **1.3.1.2**: ADD bullet points: no infrastructure needed, auth already handled, direct visual access (`.claude/skills/browser-mcp/SKILL.md`)

### ⬜ Task Group 1.4: Add cookbook routing

**Objective**: Create IF/THEN routing to workflow files for debugging and critique (files will be created in later checkpoints)

#### ⬜ Task 1.4.1: Add cookbook section with workflow routing

**File**: `.claude/skills/browser-mcp/SKILL.md`

**Description**: Add a Cookbook section following the prompt-writing SKILL.md pattern. Include IF/THEN routing for: (1) debugging front-end issues → read workflows/debug.md, (2) design critique → read workflows/critique.md. Files don't exist yet but routing should be in place.

**Context to Load**:
- `.claude/skills/prompt-writing/SKILL.md` (lines 35-65) - Example cookbook IF/THEN pattern

**Depends On**: Tasks 1.3.1

**Actions**:
- ⬜ **1.4.1.1**: ADD ## Cookbook section header (`.claude/skills/browser-mcp/SKILL.md`)
- ⬜ **1.4.1.2**: ADD ### Front-End Debugging route: IF debugging front-end THEN read workflows/debug.md (`.claude/skills/browser-mcp/SKILL.md`)
- ⬜ **1.4.1.3**: ADD ### Design Critique route: IF design critique THEN read workflows/critique.md (`.claude/skills/browser-mcp/SKILL.md`)
- ⬜ **1.4.1.4**: ADD ## Commands section listing /browser-mcp:debug and /browser-mcp:critique (`.claude/skills/browser-mcp/SKILL.md`)

---

## ⬜ Checkpoint 2: Front-End Debugging Workflow

**Goal**: Create the debugging workflow following the multi-turn autonomous pattern from prompt-writing. Implements all 8 phases: setup, observe, analyze, instrument, refresh, iterate, propose, fix, cleanup.

**Prerequisites**: Checkpoints 1

### File Context

| State | File | Status | Description |
|-------|------|--------|-------------|
| Before | `.claude/skills/browser-mcp/SKILL.md` | 📄 exists | Base skill with cookbook routing |
| Before | `.claude/skills/prompt-writing/system_prompt/20-workflow-design/30-multi-turn/00-base.md` | 📄 exists | Multi-turn workflow pattern to follow |
| After | `.claude/skills/browser-mcp/SKILL.md` | 📝 modified | Add debug log convention [DEBUG-AGENT] |
| After | `.claude/skills/browser-mcp/workflows/debug.md` | ✨ new | Multi-turn debugging workflow with XML phases |
| After | `.claude/commands/browser-mcp/debug.md` | ✨ new | Slash command that invokes the debugging workflow |

**Projected Structure**:
```
.claude/skills/browser-mcp/
├── SKILL.md
└── workflows/
    └── debug.md
.claude/commands/browser-mcp/
└── debug.md
```

### Testing Strategy

**Approach**: Manual debugging session

**Verification Steps**:
- [ ] `Run /browser-mcp:debug command`
- [ ] `Verify URL confirmation phase works`
- [ ] `Verify console log capture works`
- [ ] `Verify [DEBUG-AGENT] instrumentation convention documented`
- [ ] `Verify cleanup phase removes all markers`

### ⬜ Task Group 2.1: Add debug log convention to SKILL.md

**Objective**: Document the [DEBUG-AGENT] marker convention and cleanup strategy in the base skill

#### ⬜ Task 2.1.1: Add debug log convention section

**File**: `.claude/skills/browser-mcp/SKILL.md`

**Description**: Add a section documenting the debug log convention: console.log('[DEBUG-AGENT]', '[Context.location]', { data }). Explain the format (single call for browser grouping), marker for cleanup, and common placement patterns.

**Context to Load**:
- `agents/sessions/2026-01-06_browser-mcp-skill_b7k2m9/spec.md` (lines 103-142) - Debug log convention from spec

**Actions**:
- ⬜ **2.1.1.1**: ADD ## Debug Log Convention section to SKILL.md (`.claude/skills/browser-mcp/SKILL.md`)
- ⬜ **2.1.1.2**: ADD code example: console.log('[DEBUG-AGENT]', '[ComponentName.functionName]', { data }) (`.claude/skills/browser-mcp/SKILL.md`)
- ⬜ **2.1.1.3**: ADD cleanup strategy: grep for marker, git diff as fallback (`.claude/skills/browser-mcp/SKILL.md`)

### ⬜ Task Group 2.2: Create debugging workflow file

**Objective**: Create the multi-turn debugging workflow with XML phases following prompt-writing pattern

#### ⬜ Task 2.2.1: Create workflows/debug.md with frontmatter

**File**: `.claude/skills/browser-mcp/workflows/debug.md`

**Description**: Create the debugging workflow file. Add frontmatter covering what this workflow does. Add overview section explaining collaborative debugging approach.

**Context to Load**:
- `.claude/skills/prompt-writing/system_prompt/20-workflow-design/30-multi-turn/00-base.md` (lines 1-100) - Multi-turn workflow pattern structure
- `agents/sessions/2026-01-06_browser-mcp-skill_b7k2m9/spec.md` (lines 55-101) - Debugging workflow phases from spec

**Actions**:
- ⬜ **2.2.1.1**: CREATE FILE .claude/skills/browser-mcp/workflows/debug.md (`.claude/skills/browser-mcp/workflows/debug.md`)
- ⬜ **2.2.1.2**: ADD frontmatter with covers, type, concepts (`.claude/skills/browser-mcp/workflows/debug.md`)
- ⬜ **2.2.1.3**: ADD overview section explaining collaborative debugging approach (`.claude/skills/browser-mcp/workflows/debug.md`)

#### ⬜ Task 2.2.2: Add XML workflow with all 8 phases

**File**: `.claude/skills/browser-mcp/workflows/debug.md`

**Description**: Add the XML workflow element with all 8 debugging phases: Setup (confirm URL), Observe (screenshot + logs), Analyze (determine if more visibility needed), Instrument (add [DEBUG-AGENT] logs), Refresh (browser_navigate), Iterate (repeat until understood), Propose (explain root cause), Fix & Cleanup (implement fix, remove markers).

**Context to Load**:
- `.claude/skills/prompt-writing/system_prompt/20-workflow-design/10-base.md` (lines 40-90) - Phase and action syntax
- `agents/sessions/2026-01-06_browser-mcp-skill_b7k2m9/spec.md` (lines 55-101) - Debugging workflow phases from spec

**Depends On**: Tasks 2.2.1

**Actions**:
- ⬜ **2.2.2.1**: ADD <workflow> element with global_constraints for collaborative debugging (`.claude/skills/browser-mcp/workflows/debug.md`)
- ⬜ **2.2.2.2**: ADD <phase id=0 name=Setup>: browser_snapshot, confirm URL with user (`.claude/skills/browser-mcp/workflows/debug.md`)
- ⬜ **2.2.2.3**: ADD <phase id=1 name=Observe>: browser_screenshot, browser_get_console_logs (`.claude/skills/browser-mcp/workflows/debug.md`)
- ⬜ **2.2.2.4**: ADD <phase id=2 name=Analyze>: examine state, determine if instrumentation needed (`.claude/skills/browser-mcp/workflows/debug.md`)
- ⬜ **2.2.2.5**: ADD <phase id=3 name=Instrument>: add console.log with [DEBUG-AGENT] markers (`.claude/skills/browser-mcp/workflows/debug.md`)
- ⬜ **2.2.2.6**: ADD <phase id=4 name=Refresh>: browser_navigate to same URL for clean slate (`.claude/skills/browser-mcp/workflows/debug.md`)
- ⬜ **2.2.2.7**: ADD <phase id=5 name=Iterate>: repeat phases 1-4 until root cause identified (`.claude/skills/browser-mcp/workflows/debug.md`)
- ⬜ **2.2.2.8**: ADD <phase id=6 name=Propose>: explain root cause, propose fix, get user approval (`.claude/skills/browser-mcp/workflows/debug.md`)
- ⬜ **2.2.2.9**: ADD <phase id=7 name=Fix_and_Cleanup>: implement fix, remove all [DEBUG-AGENT] markers, verify (`.claude/skills/browser-mcp/workflows/debug.md`)

### ⬜ Task Group 2.3: Create slash command

**Objective**: Create the /browser-mcp:debug command that invokes the workflow

#### ⬜ Task 2.3.1: Create debug.md slash command

**File**: `.claude/commands/browser-mcp/debug.md`

**Description**: Create the slash command file for debugging. Add frontmatter with allowed-tools (browser MCP tools, Read, Edit), description, and arguments. Add instruction to read and execute workflows/debug.md from the skill.

**Context to Load**:
- `.claude/commands/git/commit.md` (lines 1-30) - Example command frontmatter and structure

**Depends On**: Tasks 2.2.2

**Actions**:
- ⬜ **2.3.1.1**: CREATE FILE .claude/commands/browser-mcp/debug.md (`.claude/commands/browser-mcp/debug.md`)
- ⬜ **2.3.1.2**: ADD frontmatter: allowed-tools (browser_*, Read, Edit, Bash), description, arguments (`.claude/commands/browser-mcp/debug.md`)
- ⬜ **2.3.1.3**: ADD instruction: Read and execute .claude/skills/browser-mcp/workflows/debug.md (`.claude/commands/browser-mcp/debug.md`)

---

## ⬜ Checkpoint 3: Design Critique Workflow

**Goal**: Create the design critique workflow following multi-turn pattern. Implements context gathering, Jony Ive analysis, principles check, report generation, and session storage.

**Prerequisites**: Checkpoints 1

### File Context

| State | File | Status | Description |
|-------|------|--------|-------------|
| Before | `.claude/skills/browser-mcp/SKILL.md` | 📄 exists | Base skill with cookbook routing |
| Before | `.claude/skills/prompt-writing/system_prompt/20-workflow-design/30-multi-turn/00-base.md` | 📄 exists | Multi-turn workflow pattern to follow |
| After | `.claude/skills/browser-mcp/SKILL.md` | 📝 modified | Add design principles summary |
| After | `.claude/skills/browser-mcp/workflows/critique.md` | ✨ new | Multi-turn critique workflow with XML phases |
| After | `.claude/skills/browser-mcp/references/design-principles.md` | ✨ new | Jony Ive aesthetic guidelines |
| After | `.claude/commands/browser-mcp/critique.md` | ✨ new | Slash command that invokes the critique workflow |

**Projected Structure**:
```
.claude/skills/browser-mcp/
├── SKILL.md
├── workflows/
│   ├── debug.md
│   └── critique.md
└── references/
    └── design-principles.md
.claude/commands/browser-mcp/
├── debug.md
└── critique.md
```

### Testing Strategy

**Approach**: Manual critique session

**Verification Steps**:
- [ ] `Run /browser-mcp:critique command`
- [ ] `Verify context inference and confirmation works`
- [ ] `Verify Jony Ive principles are applied`
- [ ] `Verify output saved to agents/design-sessions/{id}/`

### ⬜ Task Group 3.1: Create design principles reference

**Objective**: Create a reference document with Jony Ive aesthetic guidelines and design principles

#### ⬜ Task 3.1.1: Create design-principles.md reference file

**File**: `.claude/skills/browser-mcp/references/design-principles.md`

**Description**: Create the design principles reference file. Include the Jony Ive lens ('Really think. Really, really think.'), target aesthetic (sleek, premium, minimalist, like a spa in Switzerland), and specific guidelines (icons over emojis, perfect padding, cohesive colors, responsive design).

**Context to Load**:
- `agents/sessions/2026-01-06_browser-mcp-skill_b7k2m9/spec.md` (lines 208-227) - Design principles from spec

**Actions**:
- ⬜ **3.1.1.1**: CREATE FILE .claude/skills/browser-mcp/references/design-principles.md (`.claude/skills/browser-mcp/references/design-principles.md`)
- ⬜ **3.1.1.2**: ADD frontmatter with covers, type (`.claude/skills/browser-mcp/references/design-principles.md`)
- ⬜ **3.1.1.3**: ADD Jony Ive Lens section with key quote and mindset (`.claude/skills/browser-mcp/references/design-principles.md`)
- ⬜ **3.1.1.4**: ADD Target Aesthetic section (sleek, premium, minimalist) (`.claude/skills/browser-mcp/references/design-principles.md`)
- ⬜ **3.1.1.5**: ADD Specific Guidelines (icons, padding, colors, responsive) (`.claude/skills/browser-mcp/references/design-principles.md`)

### ⬜ Task Group 3.2: Create critique workflow file

**Objective**: Create the multi-turn critique workflow with XML phases following prompt-writing pattern

#### ⬜ Task 3.2.1: Create workflows/critique.md with frontmatter

**File**: `.claude/skills/browser-mcp/workflows/critique.md`

**Description**: Create the critique workflow file. Add frontmatter covering what this workflow does. Add overview section explaining the design critique approach and that it produces analysis, not implementation.

**Context to Load**:
- `.claude/skills/prompt-writing/system_prompt/20-workflow-design/30-multi-turn/00-base.md` (lines 1-100) - Multi-turn workflow pattern structure
- `agents/sessions/2026-01-06_browser-mcp-skill_b7k2m9/spec.md` (lines 145-206) - Critique workflow from spec

**Depends On**: Tasks 3.1.1

**Actions**:
- ⬜ **3.2.1.1**: CREATE FILE .claude/skills/browser-mcp/workflows/critique.md (`.claude/skills/browser-mcp/workflows/critique.md`)
- ⬜ **3.2.1.2**: ADD frontmatter with covers, type, concepts (`.claude/skills/browser-mcp/workflows/critique.md`)
- ⬜ **3.2.1.3**: ADD overview section explaining analysis-focused (not implementation) approach (`.claude/skills/browser-mcp/workflows/critique.md`)

#### ⬜ Task 3.2.2: Add XML workflow with 7 critique phases

**File**: `.claude/skills/browser-mcp/workflows/critique.md`

**Description**: Add the XML workflow element with 7 critique phases: Context Gathering (infer + confirm), Visual Capture (screenshots), Analysis (Jony Ive lens), Principles Check (guidelines), Report (structured output), Refinement (iterate with user), Save (agents/design-sessions/{id}/).

**Context to Load**:
- `.claude/skills/prompt-writing/system_prompt/20-workflow-design/10-base.md` (lines 40-90) - Phase and action syntax
- `agents/sessions/2026-01-06_browser-mcp-skill_b7k2m9/spec.md` (lines 145-206) - Critique workflow phases from spec
- `.claude/skills/browser-mcp/references/design-principles.md` - Reference design principles in workflow

**Depends On**: Tasks 3.2.1

**Actions**:
- ⬜ **3.2.2.1**: ADD <workflow> element with global_constraints for critique approach (`.claude/skills/browser-mcp/workflows/critique.md`)
- ⬜ **3.2.2.2**: ADD <phase id=1 name=Context_Gathering>: infer app/page purpose, present to user, require confirmation (`.claude/skills/browser-mcp/workflows/critique.md`)
- ⬜ **3.2.2.3**: ADD <phase id=2 name=Visual_Capture>: screenshots across states/viewports (`.claude/skills/browser-mcp/workflows/critique.md`)
- ⬜ **3.2.2.4**: ADD <phase id=3 name=Analysis>: apply Jony Ive lens (what works, what doesn't, confusing, redundant) (`.claude/skills/browser-mcp/workflows/critique.md`)
- ⬜ **3.2.2.5**: ADD <phase id=4 name=Principles_Check>: evaluate against design principles from references/design-principles.md (`.claude/skills/browser-mcp/workflows/critique.md`)
- ⬜ **3.2.2.6**: ADD <phase id=5 name=Report>: structured output with summary, issues, recommendations, priorities (`.claude/skills/browser-mcp/workflows/critique.md`)
- ⬜ **3.2.2.7**: ADD <phase id=6 name=Refinement>: iterate with user questions until satisfied (`.claude/skills/browser-mcp/workflows/critique.md`)
- ⬜ **3.2.2.8**: ADD <phase id=7 name=Save>: write to agents/design-sessions/{id}/ (critique.md, context.md, screenshots/) (`.claude/skills/browser-mcp/workflows/critique.md`)

### ⬜ Task Group 3.3: Create slash command

**Objective**: Create the /browser-mcp:critique command that invokes the workflow

#### ⬜ Task 3.3.1: Create critique.md slash command

**File**: `.claude/commands/browser-mcp/critique.md`

**Description**: Create the slash command file for design critique. Add frontmatter with allowed-tools (browser MCP tools, Read, Write), description, and arguments. Add instruction to read and execute workflows/critique.md from the skill.

**Context to Load**:
- `.claude/commands/browser-mcp/debug.md` - Example command structure from checkpoint 2

**Depends On**: Tasks 3.2.2

**Actions**:
- ⬜ **3.3.1.1**: CREATE FILE .claude/commands/browser-mcp/critique.md (`.claude/commands/browser-mcp/critique.md`)
- ⬜ **3.3.1.2**: ADD frontmatter: allowed-tools (browser_*, Read, Write), description, arguments (`.claude/commands/browser-mcp/critique.md`)
- ⬜ **3.3.1.3**: ADD instruction: Read and execute .claude/skills/browser-mcp/workflows/critique.md (`.claude/commands/browser-mcp/critique.md`)

### ⬜ Task Group 3.4: Update SKILL.md with design principles reference

**Objective**: Add a brief design principles section to SKILL.md that references the detailed principles file

#### ⬜ Task 3.4.1: Add design principles summary to SKILL.md

**File**: `.claude/skills/browser-mcp/SKILL.md`

**Description**: Add a brief Design Principles section to SKILL.md that summarizes the Jony Ive approach and links to the full references/design-principles.md file.

**Context to Load**:
- `.claude/skills/browser-mcp/references/design-principles.md` - Reference the detailed principles file

**Depends On**: Tasks 3.1.1

**Actions**:
- ⬜ **3.4.1.1**: ADD ## Design Principles section with brief Jony Ive summary (`.claude/skills/browser-mcp/SKILL.md`)
- ⬜ **3.4.1.2**: ADD link to references/design-principles.md for full guidelines (`.claude/skills/browser-mcp/SKILL.md`)

---

## ⬜ Checkpoint 4: Polish and Spec Validation

**Goal**: Refine cookbook routing, add tools quick reference, ensure cross-workflow consistency, validate all spec success criteria are met.

**Prerequisites**: Checkpoints 2, 3

### File Context

| State | File | Status | Description |
|-------|------|--------|-------------|
| Before | `.claude/skills/browser-mcp/SKILL.md` | 📄 exists | Skill with both workflows referenced |
| After | `.claude/skills/browser-mcp/SKILL.md` | 📝 modified | Polished skill with complete cookbook and commands section |
| After | `.claude/skills/browser-mcp/references/tools.md` | ✨ new | Browser MCP tools quick reference |

**Projected Structure**:
```
.claude/skills/browser-mcp/
├── SKILL.md
├── workflows/
│   ├── debug.md
│   └── critique.md
└── references/
    ├── design-principles.md
    └── tools.md
```

### Testing Strategy

**Approach**: Spec success criteria validation

**Verification Steps**:
- [ ] `Check all debugging workflow success criteria from spec`
- [ ] `Check all design critique success criteria from spec`
- [ ] `Verify cookbook routing works correctly`
- [ ] `Verify skill structure matches project conventions`

### ⬜ Task Group 4.1: Create tools quick reference

**Objective**: Create a standalone tools reference file with detailed Browser MCP tools documentation

#### ⬜ Task 4.1.1: Create tools.md reference file

**File**: `.claude/skills/browser-mcp/references/tools.md`

**Description**: Create a comprehensive tools reference file. Include all 12 Browser MCP tools with detailed usage examples, parameters, and when to use each. This is more detailed than the summary table in SKILL.md.

**Context to Load**:
- `agents/sessions/2026-01-06_browser-mcp-skill_b7k2m9/spec.md` (lines 275-295) - Browser MCP tools from spec
- `.claude/skills/browser-mcp/SKILL.md` - Reference existing tools table

**Actions**:
- ⬜ **4.1.1.1**: CREATE FILE .claude/skills/browser-mcp/references/tools.md (`.claude/skills/browser-mcp/references/tools.md`)
- ⬜ **4.1.1.2**: ADD frontmatter with covers, type (`.claude/skills/browser-mcp/references/tools.md`)
- ⬜ **4.1.1.3**: ADD navigation tools section (browser_navigate, browser_go_back, browser_go_forward) (`.claude/skills/browser-mcp/references/tools.md`)
- ⬜ **4.1.1.4**: ADD state capture tools section (browser_snapshot, browser_screenshot, browser_get_console_logs) (`.claude/skills/browser-mcp/references/tools.md`)
- ⬜ **4.1.1.5**: ADD interaction tools section (browser_click, browser_hover, browser_type, browser_select_option, browser_press_key) (`.claude/skills/browser-mcp/references/tools.md`)
- ⬜ **4.1.1.6**: ADD utility tools section (browser_wait) (`.claude/skills/browser-mcp/references/tools.md`)

### ⬜ Task Group 4.2: Polish SKILL.md

**Objective**: Review and polish SKILL.md for completeness, cross-links, and consistency

#### ⬜ Task 4.2.1: Add References section to SKILL.md

**File**: `.claude/skills/browser-mcp/SKILL.md`

**Description**: Add a References section that links to all reference files: tools.md and design-principles.md. This creates a clear navigation structure.

**Context to Load**:
- `.claude/skills/browser-mcp/SKILL.md` - Review current structure
- `.claude/skills/git/SKILL.md` (lines 50-62) - Example References section

**Depends On**: Tasks 4.1.1

**Actions**:
- ⬜ **4.2.1.1**: ADD ## References section to SKILL.md (`.claude/skills/browser-mcp/SKILL.md`)
- ⬜ **4.2.1.2**: ADD link to references/tools.md (Browser MCP tools quick reference) (`.claude/skills/browser-mcp/SKILL.md`)
- ⬜ **4.2.1.3**: ADD link to references/design-principles.md (Jony Ive design guidelines) (`.claude/skills/browser-mcp/SKILL.md`)

### ⬜ Task Group 4.3: Validate spec success criteria

**Objective**: Review all files against spec success criteria and make any needed adjustments

#### ⬜ Task 4.3.1: Validate debugging workflow criteria

**File**: `.claude/skills/browser-mcp/workflows/debug.md`

**Description**: Review debugging workflow against spec success criteria: browser_snapshot for URL confirm, console logs + screenshots without copy/paste, [DEBUG-AGENT] instrumentation, browser_navigate refresh, cleanup of markers, user confirmations at key points.

**Context to Load**:
- `agents/sessions/2026-01-06_browser-mcp-skill_b7k2m9/spec.md` (lines 255-262) - Debugging workflow success criteria
- `.claude/skills/browser-mcp/workflows/debug.md` - Verify workflow meets criteria

**Actions**:
- ⬜ **4.3.1.1**: VERIFY debug workflow has browser_snapshot for URL confirmation (`.claude/skills/browser-mcp/workflows/debug.md`)
- ⬜ **4.3.1.2**: VERIFY debug workflow has console log + screenshot capture without manual copy/paste (`.claude/skills/browser-mcp/workflows/debug.md`)
- ⬜ **4.3.1.3**: VERIFY debug workflow uses [DEBUG-AGENT] marker convention (`.claude/skills/browser-mcp/workflows/debug.md`)
- ⬜ **4.3.1.4**: VERIFY debug workflow has cleanup phase for marker removal (`.claude/skills/browser-mcp/workflows/debug.md`)

#### ⬜ Task 4.3.2: Validate critique workflow criteria

**File**: `.claude/skills/browser-mcp/workflows/critique.md`

**Description**: Review critique workflow against spec success criteria: context inference + user confirmation, screenshot capture across states/viewports, Jony Ive lens applied, output saved to agents/design-sessions/{id}/.

**Context to Load**:
- `agents/sessions/2026-01-06_browser-mcp-skill_b7k2m9/spec.md` (lines 264-270) - Critique workflow success criteria
- `.claude/skills/browser-mcp/workflows/critique.md` - Verify workflow meets criteria

**Actions**:
- ⬜ **4.3.2.1**: VERIFY critique workflow has context inference + user confirmation (`.claude/skills/browser-mcp/workflows/critique.md`)
- ⬜ **4.3.2.2**: VERIFY critique workflow captures screenshots across states/viewports (`.claude/skills/browser-mcp/workflows/critique.md`)
- ⬜ **4.3.2.3**: VERIFY critique workflow applies Jony Ive lens and design principles (`.claude/skills/browser-mcp/workflows/critique.md`)
- ⬜ **4.3.2.4**: VERIFY critique workflow saves to agents/design-sessions/{id}/ (`.claude/skills/browser-mcp/workflows/critique.md`)

---

---
*Auto-generated from plan.json on 2026-01-07 09:08*