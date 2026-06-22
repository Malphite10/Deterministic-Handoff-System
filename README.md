# Multi-Agent Deterministic Handoff System

**Owner**: @Malphite10
**Status**: Production Agent Operating System 🟢

A production-grade multi-agent orchestration framework with deterministic handoffs, a critical supply-chain gatekeeper, and a full-featured runtime execution engine.

## 2-Layer Architecture

### 1. Private Core (Engine)
- **Runtime Engine**: Python-based orchestrator, state manager, and execution graph.
- **Agent Factory**: Machine-readable agent definitions (`agent.json`) and skills (`skill.md`).
- **Deterministic State**: Resumable execution via `state.json` and structured artifacts.

### 2. Public Layer (Products)
- **Templates**: High-converting template DNA for SaaS, Agency, and AI Startups.
- **Design System**: Registry of high-performance components and tokens.
- **Marketplace Assets**: Ready-to-publish marketplace submission artifacts.

## Quick Start

```bash
git clone https://github.com/@Malphite10/multi-agent-system.git
cd multi-agent-system
npm install
PYTHONPATH=. python3 runtime/orchestrator.py --dry-run
```

## Core Components

### Runtime State Machine
The `runtime/` engine manages execution flow and artifact generation.
- `orchestrator.py`: Coordinates the workflow.
- `state.py`: Manages global state persistence.
- `graph.py`: Defines the execution sequence.
- `registry.py`: Loads agent metadata.

### Supply Chain Gatekeeper
Critical security gate in `.github/workflows/` enforcing:
- ✅ Dependency license scans
- ✅ SBOM generation (CycloneDX)
- ✅ SLSA provenance
- ✅ Signed releases

## Repository Structure

- `runtime/`: Execution engine and state management.
- `agents/`: Agent specifications, skills, and central registry.
- `schemas/`: Global state and handoff definitions.
- `artifacts/`: Structured store for runs, snapshots, and security reports.
- `design-system/`: Registry and design tokens.
- `memory/`: Knowledge graph and marketplace intelligence.

---

Built with ❤️ by @Malphite10

![Octocats High Five](https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png) 🙌 🐱
