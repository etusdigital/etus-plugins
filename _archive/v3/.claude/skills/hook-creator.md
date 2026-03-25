# Hook Creator Skill

**Description:** Guide for creating and configuring Claude Code hooks to automate workflows, validate operations, and enhance development experience. This skill helps you create custom hooks with proper structure, matchers, and event handling.

**Use this skill when:** Users want to create hooks, automate workflows, add validation, or customize Claude Code behavior with event-driven scripts.

---

## Quick Hook Creation Process

When a user asks to create a hook, follow this structured approach:

### Step 1: Understand Requirements
Ask the user to clarify:
- **What should trigger the hook?** (Before/after tool use, on prompt submit, session start/end)
- **Which tools should it match?** (Specific tools like Write/Edit, or all tools with *)
- **What should it do?** (Log, format, validate, notify, run tests, sync, etc.)
- **Should it block operations?** (Exit code 2 for blocking, 0 for non-blocking)
- **Where should it be installed?** (Project-specific `.claude/settings.json` or global `~/.claude/settings.json`)

### Step 2: Choose Hook Event Type

```json
// Available Hook Events:
{
  "PreToolUse": "Before Claude executes a tool (can block)",
  "PostToolUse": "After tool completes successfully",
  "UserPromptSubmit": "When user submits prompt (can block)",
  "SessionStart": "Session begins or resumes",
  "SessionEnd": "Session terminates",
  "Stop": "Claude finishes responding",
  "SubagentStop": "Subagent completes",
  "Notification": "Claude sends notifications",
  "PreCompact": "Before compacting conversation history"
}
```

### Step 3: Choose Matcher Pattern

```json
// Matcher Examples:
"matcher": "Write"              // Exact match for Write tool
"matcher": "Edit|Write"         // Multiple tools (regex OR)
"matcher": "Bash"               // Shell commands only
"matcher": "Edit|MultiEdit"     // All edit operations
"matcher": "Write|Edit|MultiEdit" // All file modifications
"matcher": "*"                  // All tools (use sparingly)
"matcher": ""                   // Also matches all tools

// For SessionStart:
"matcher": "startup"            // Normal startup
"matcher": "resume"             // Resumed session
"matcher": "startup|resume"     // Both startup and resume
"matcher": "clear"              // After /clear command
```

### Step 4: Create Hook Configuration

Basic structure:
```json
{
  "description": "Clear description of what this hook does",
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "your shell command here",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Step 5: Implement Hook Logic

Choose implementation approach:

#### Option A: Simple Shell Command
```json
{
  "type": "command",
  "command": "echo 'Hook executed' && your-command-here",
  "timeout": 30
}
```

#### Option B: Inline Bash Script
```json
{
  "type": "command",
  "command": "bash -c 'input=$(cat); FILE_PATH=$(echo \"$input\" | jq -r \".tool_input.file_path // empty\"); echo \"Processing $FILE_PATH\"'",
  "timeout": 30
}
```

#### Option C: External Script Reference
```json
{
  "type": "command",
  "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/my-hook.sh",
  "timeout": 60
}
```

## Available Environment Variables

Hooks have access to these environment variables:
- `$CLAUDE_PROJECT_DIR` - Current project directory
- `$CLAUDE_TOOL_NAME` - Name of the tool being executed
- `$CLAUDE_TOOL_FILE_PATH` - File path from tool input (if applicable)

Hook input JSON structure (via stdin):
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/conversation.jsonl",
  "cwd": "/current/working/directory",
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "success": true
  }
}
```

## Exit Code Behavior

### Exit Code 0 (Success)
- For most hooks: stdout shown in transcript mode (Ctrl+R)
- For UserPromptSubmit/SessionStart: stdout added as context for Claude
- Operation continues normally

### Exit Code 2 (Blocking Error)
- **PreToolUse**: Blocks tool execution, shows stderr to Claude
- **PostToolUse**: Shows stderr to Claude (tool already executed)
- **UserPromptSubmit**: Blocks prompt, erases it, shows stderr to user
- **Stop/SubagentStop**: Blocks stopping, shows stderr to Claude
- **Others**: Shows stderr to user only

### Other Exit Codes (Non-blocking Error)
- Shows stderr to user
- Continues execution
- Use for warnings or non-critical errors

## Advanced JSON Output

For sophisticated control, return JSON to stdout:

```json
{
  "continue": true,
  "stopReason": "Optional message when continue is false",
  "suppressOutput": false,
  "systemMessage": "Optional warning for user",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Auto-approved safe operation",
    "additionalContext": "Extra context for Claude"
  }
}
```

### PreToolUse Permission Control
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",  // "allow", "deny", or "ask"
    "permissionDecisionReason": "Reason for decision"
  }
}
```

### PostToolUse Feedback
```json
{
  "decision": "block",  // "block" or undefined
  "reason": "Why operation is blocked",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional info for Claude"
  }
}
```

## Common Hook Patterns

### 1. Logging Pattern
```json
{
  "description": "Log all tool usage for audit trail",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"[$(date)] $CLAUDE_TOOL_NAME\" >> ~/.claude/activity.log"
          }
        ]
      }
    ]
  }
}
```

### 2. Backup Pattern
```json
{
  "description": "Backup files before editing",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "[[ -f \"$CLAUDE_TOOL_FILE_PATH\" ]] && cp \"$CLAUDE_TOOL_FILE_PATH\" \"$CLAUDE_TOOL_FILE_PATH.$(date +%s).bak\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### 3. Auto-Format Pattern
```json
{
  "description": "Auto-format code files after editing",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" =~ \\.(js|ts)$ ]]; then npx prettier --write \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; elif [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.py ]]; then black \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

### 4. Git Auto-Add Pattern
```json
{
  "description": "Automatically git add modified files",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "git rev-parse --git-dir >/dev/null 2>&1 && git add \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### 5. Test Runner Pattern
```json
{
  "description": "Run tests after code changes",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ -f package.json ]]; then npm test 2>/dev/null || yarn test 2>/dev/null || true; elif [[ -f pytest.ini ]]; then pytest 2>/dev/null || true; fi",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

### 6. File Protection Pattern
```json
{
  "description": "Prevent editing protected files",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "for p in '/etc/*' '/usr/bin/*' '*.production.*' '*prod*config*'; do [[ \"$CLAUDE_TOOL_FILE_PATH\" == $p ]] && echo \"Error: Protected file\" >&2 && exit 1; done"
          }
        ]
      }
    ]
  }
}
```

### 7. Security Scanner Pattern
```json
{
  "description": "Scan for security issues after modifications",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if command -v semgrep >/dev/null 2>&1; then semgrep --config=auto \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi; if grep -qE '(password|secret|key|token)\\s*=\\s*[\"\\'][^\"\\'\n]{8,}' \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null; then echo \"Warning: Potential hardcoded secrets\" >&2; fi",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 8. Session Context Loading Pattern
```json
{
  "description": "Load project context at session start",
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"## Project Status\"; echo \"Branch: $(git branch --show-current 2>/dev/null || echo 'N/A')\"; echo \"Last commit: $(git log -1 --oneline 2>/dev/null || echo 'N/A')\""
          }
        ]
      }
    ]
  }
}
```

### 9. Notification Pattern
```json
{
  "description": "Send desktop notifications on completion",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "if command -v osascript >/dev/null; then osascript -e 'display notification \"$CLAUDE_TOOL_NAME completed\" with title \"Claude Code\"'; elif command -v notify-send >/dev/null; then notify-send \"Claude Code\" \"$CLAUDE_TOOL_NAME completed\"; fi"
          }
        ]
      }
    ]
  }
}
```

### 10. Build Trigger Pattern
```json
{
  "description": "Trigger build after file changes",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ -f package.json ]] && grep -q '\"build\"' package.json; then npm run build 2>/dev/null || true; elif [[ -f Makefile ]]; then make 2>/dev/null || true; fi",
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

## Complex Hook Example: Input Validation with JSON Processing

```json
{
  "description": "Validate code changes with detailed analysis",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'input=$(cat); FILE_PATH=$(echo \"$input\" | jq -r \".tool_input.file_path // empty\"); SUCCESS=$(echo \"$input\" | jq -r \".tool_response.success // false\"); if [ \"$SUCCESS\" = \"true\" ] && [[ \"$FILE_PATH\" =~ \\.(js|jsx|ts|tsx)$ ]]; then echo \"🔍 Validating $FILE_PATH...\"; ISSUES=0; if ! grep -q \"export\" \"$FILE_PATH\" 2>/dev/null; then echo \"⚠️ No exports found\"; ((ISSUES++)); fi; if [ $ISSUES -eq 0 ]; then echo \"✅ Validation passed\"; else echo \"❌ Found $ISSUES issues\" >&2; exit 2; fi; fi'",
            "timeout": 20
          }
        ]
      }
    ]
  }
}
```

## Best Practices

### 1. Hook Design
- **Single Responsibility**: Each hook should do one thing well
- **Fail Gracefully**: Use `|| true` for non-critical operations
- **Be Fast**: Keep execution time under 30 seconds when possible
- **Idempotent**: Safe to run multiple times with same input

### 2. Error Handling
```bash
# Suppress non-critical errors
command 2>/dev/null || true

# Check command existence
if command -v prettier >/dev/null 2>&1; then
  prettier --write "$FILE_PATH"
fi

# Check file existence
[[ -f "$FILE_PATH" ]] && process_file || echo "File not found"
```

### 3. Performance
- Set appropriate timeouts (default: 60s)
- Use background processes for long operations: `command &`
- Cache results when possible
- Avoid expensive operations in hot paths

### 4. Security
- Always validate file paths: check for `..` patterns
- Never expose secrets in output
- Use exit code 2 to block dangerous operations
- Validate user inputs thoroughly
- Use minimal required permissions

### 5. Testing
Test hooks independently:
```bash
# Test with mock input
echo '{"session_id":"test","hook_event_name":"PreToolUse","tool_name":"Write","tool_input":{"file_path":"test.txt"}}' | bash -c 'your-hook-command'

# Test exit codes
bash -c 'your-hook-command'; echo "Exit code: $?"

# Test JSON output
echo '{"session_id":"test"}' | bash -c 'your-hook-command' | jq .
```

## Installation Methods

### Method 1: Direct Settings File Edit
Add hook to `.claude/settings.json` or `~/.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'File written'"
          }
        ]
      }
    ]
  }
}
```

### Method 2: Using claude-code-templates CLI
```bash
# Install pre-built hook
npx claude-code-templates@latest --hook security-scanner

# Browse available hooks
npx claude-code-templates@latest
```

### Method 3: External Script
1. Create hook configuration in settings.json
2. Create executable script:
```bash
# Create hook script
cat > .claude/hooks/my-hook.sh << 'EOF'
#!/bin/bash
input=$(cat)
# Hook logic here
EOF

# Make executable
chmod +x .claude/hooks/my-hook.sh
```

3. Reference in configuration:
```json
{
  "type": "command",
  "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/my-hook.sh"
}
```

## Debugging Hooks

### Check Hook Registration
```bash
# View active hooks
claude --debug

# Or check settings file
cat ~/.claude/settings.json
cat .claude/settings.json
```

### Enable Debug Mode
```bash
# Run Claude Code with debug output
claude --debug
```

Debug output shows:
- Hook discovery and matching
- Command execution
- Exit codes
- stdout/stderr output
- Execution time

### Common Issues

1. **Hook not executing**
   - Check JSON syntax in settings.json
   - Verify matcher pattern (case-sensitive)
   - Ensure script is executable: `chmod +x script.sh`
   - Check hook event name spelling

2. **Permission errors**
   - Verify script permissions
   - Check file paths are absolute or use `$CLAUDE_PROJECT_DIR`
   - Ensure required tools are installed

3. **Timeout issues**
   - Increase timeout value
   - Optimize hook performance
   - Use background processes: `command &`

## Hook Creation Workflow

When creating a hook, follow this process:

1. **Clarify Requirements**
   - What triggers the hook?
   - What should it do?
   - Should it block operations?
   - Where should it be installed?

2. **Choose Pattern**
   - Simple command
   - Inline bash script
   - External script reference
   - Complex with JSON parsing

3. **Implement Logic**
   - Start simple
   - Add error handling
   - Test thoroughly
   - Optimize for performance

4. **Test Hook**
   - Test with mock data
   - Verify exit codes
   - Check error handling
   - Test edge cases

5. **Install and Validate**
   - Add to settings.json
   - Verify JSON syntax
   - Test in real workflow
   - Monitor with debug mode

6. **Document**
   - Add clear description
   - Document requirements
   - Note any dependencies
   - Explain configuration

## Template for Creating New Hooks

Use this template when creating hooks:

```json
{
  "description": "[Clear description of what this hook does and when it runs]",
  "hooks": {
    "[EventName]": [
      {
        "matcher": "[ToolPattern]",
        "hooks": [
          {
            "type": "command",
            "command": "[Your command here]",
            "timeout": [Timeout in seconds]
          }
        ]
      }
    ]
  }
}
```

## Resources

- **Official Documentation**: https://docs.claude.com/en/docs/claude-code/hooks-guide
- **Hook Examples**: `/Users/albertoandre/Dropbox/aa-projects/ia-setup/claude-code-templates/cli-tool/components/hooks/`
- **Pre-built Hooks**: https://github.com/anthropics/claude-code (community)
- **CLI Tool**: `npx claude-code-templates@latest --hook [name]`

## Common Commands for Hooks

### File Checks
```bash
[[ -f "$FILE_PATH" ]]              # File exists
[[ -d "$DIR_PATH" ]]               # Directory exists
[[ "$FILE" =~ \.js$ ]]             # File extension match
```

### Git Operations
```bash
git rev-parse --git-dir >/dev/null 2>&1  # In git repo
git branch --show-current                # Current branch
git diff --name-only HEAD                # Modified files
git add "$FILE_PATH"                     # Stage file
```

### Tool Checks
```bash
command -v prettier >/dev/null 2>&1      # Tool exists
```

### Conditional Execution
```bash
[[ condition ]] && command || true       # Safe execution
command 2>/dev/null || true              # Suppress errors
```

### JSON Processing
```bash
input=$(cat)                             # Read stdin
echo "$input" | jq -r '.tool_input.file_path'  # Parse JSON
```

---

## When User Asks to Create a Hook

1. **Gather Requirements** using the questions in Step 1
2. **Propose Hook Structure** with appropriate event and matcher
3. **Implement Hook Logic** using patterns from this guide
4. **Create Configuration File** in proper JSON format
5. **Provide Installation Instructions** for settings.json
6. **Offer Testing Guidance** with mock data examples
7. **Document the Hook** with clear description and usage notes

Always prioritize:
- Clear, understandable code
- Proper error handling
- Security best practices
- Performance optimization
- Comprehensive testing

Remember: Hooks execute with full environment access - always validate and sanitize inputs!
