---
description: Handle mid-sprint requirement changes with a structured Sprint Change Proposal.
---

# Correct Course

Handle mid-sprint requirement changes with a structured Sprint Change Proposal.

## Usage
```
/correct-course                    -> Start change proposal
/correct-course [change description] -> Start with change context
```

## Workflow

1. Understand the change (interview)
2. Analyze impact across all existing documents
3. Generate Sprint Change Proposal
4. Present for approval
5. If approved, update affected documents + Linear (if connected)

## Reconciliation

After the change-proposal is approved, correct-course automatically:
1. Finds all documents referencing affected IDs
2. Generates proposed diffs for each
3. Presents changes for approval
4. Applies approved changes and updates state files

This ensures scope changes propagate to ALL connected documents instead of requiring manual updates.

$ARGUMENTS
