# Start Project

Initialize a new product documentation project and begin the orchestrator.

## What It Does

1. Check for existing structure:
   - If docs/ets/ exists -> ask user: start fresh or continue existing?
   - If ids.yml exists -> ask user: reset or keep?

2. Create the output directory structure:
   ```
   docs/ets/
   ├── catalog/
   ├── projects/
   │   └── {project-slug}/
   │       ├── discovery/
   │       ├── planning/
   │       │   └── feature-specs/
   │       ├── architecture/
   │       ├── data/
   │       ├── ux/
   │       ├── implementation/
   │       ├── features/
   │       ├── bugs/
   │       ├── spikes/
   │       ├── adrs/
   │       ├── learnings/
   │       └── state/
   └── schemas/
   ```

3. Copy ids.yml template to project root (if not exists):
   - Source: .claude/skills/orchestrator/knowledge/ids.yml
   - Target: ids.yml (project root)

4. Ask user for initial project metadata:
   - Product name -> update ids.yml registry.product
   - Namespace -> update ids.yml registry.namespace
   - Owner -> update ids.yml registry.owner

5. Confirm project structure was created successfully

6. Initialize workflow metadata for new projects:
   - Run `python3 .claude/hooks/state-manager.py init-project {project-slug} none product`
   - Create `docs/ets/projects/{project-slug}/state/project-status.yaml`
   - Create `docs/ets/projects/{project-slug}/state/workflow-state.yaml`
   - Create `docs/ets/projects/{project-slug}/state/feature-index.yaml`
   - Save `execution_adapter: none` into `project-status.yaml`
   - Do not create execution adapter files by default

7. Recommend the opening flow:
   - `/ideate` to create opportunity-pack.md + coverage-matrix.yaml
   - `/discover` to derive project-context.md + product-vision.md from ideation

8. Hand off to orchestrator (Phase 1: Discovery):
   - Read .claude/commands/orchestrator.md
   - Begin the full workflow starting from Phase 1

$ARGUMENTS
