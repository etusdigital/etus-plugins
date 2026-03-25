# Etus Plugins — Claude Code Marketplace

Plugin marketplace for [Claude Code](https://claude.ai/code) by [Etus Digital](https://github.com/etusdigital).

## Installation

```bash
/plugin marketplace add etusdigital/etus-plugins
/plugin install pm@etus
```

## Available Plugins

| Plugin | Commands | Description |
|--------|----------|-------------|
| **pm** | `/pm:prd`, `/pm:stories`, `/pm:disc-ideate`, `/pm:val-elicit`, ... | Product documentation with story-based elicitation and developer handoff |

## Plugin: pm

48 skills across discovery, planning, architecture, data, UX, API, implementation, validation, and retrospective.

### Key commands

```
/pm:disc-ideate        # Story-based ideation with SNAP-# snapshots
/pm:prd                # Product Requirements Document
/pm:stories            # User stories with Given/When/Then
/pm:brief              # Feature brief with NG-# non-goals
/pm:val-elicit         # Semantic stress-test (ambiguities, contradictions, gaps)
/pm:impl-packet        # Developer handoff packet (SST-compliant)
/pm:orchestrator       # Full workflow orchestration
/pm:retro-feedback     # Post-implementation feedback loop
```

### Skill categories

| Prefix | Category | Skills |
|--------|----------|--------|
| `disc-` | Discovery | ideate, project-context, product-vision, baseline, report, jtbd, journeys, edges, cases, assumptions, spike |
| *(none)* | Planning | prd, stories, brief, feature-spec, ost, prioritization, solution, correct-course |
| `arch-` | Architecture | diagram, tech-spec, delta |
| `data-` | Data Design | requirements, erd, db-spec, dictionary, flow, catalog |
| `ux-` | UX Design | journey, sitemap, wireframes, style-guide |
| `api-` | API | spec |
| `impl-` | Implementation | plan, packet, quality, release, sprint, tech-spec |
| `val-` | Validation | gate, traceability, sst, quick, elicit |
| `retro-` | Retrospective | project, feedback |

## Future Plugins

| Plugin | Status | Description |
|--------|--------|-------------|
| **data** | Planned | Data pipelines, dashboards, KPIs, data quality |
| **ads** | Planned | Ad ops, campaign specs, budget allocation, creative briefs |
| **ops** | Planned | Infrastructure, deploys, monitoring, runbooks |
| **hub** | Planned | CMS, content ops, editorial workflow |

## License

MIT
