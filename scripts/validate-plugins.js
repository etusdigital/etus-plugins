#!/usr/bin/env node
/**
 * Validate all plugins in the marketplace.
 * Run: node scripts/validate-plugins.js
 */
const fs = require('fs');
const path = require('path');

const pluginsDir = path.join(__dirname, '..', 'plugins');
const marketplacePath = path.join(__dirname, '..', '.claude-plugin', 'marketplace.json');

let errors = 0;

// Validate marketplace.json
try {
  const marketplace = JSON.parse(fs.readFileSync(marketplacePath, 'utf8'));
  console.log(`✓ Marketplace: ${marketplace.name} (${marketplace.plugins.length} plugins listed)`);
  
  for (const plugin of marketplace.plugins) {
    if (!plugin.name || !plugin.source) {
      console.error(`✗ Plugin entry missing name or source: ${JSON.stringify(plugin)}`);
      errors++;
    }
  }
} catch (e) {
  console.error(`✗ Invalid marketplace.json: ${e.message}`);
  errors++;
}

// Validate each plugin directory
const plugins = fs.readdirSync(pluginsDir).filter(d => 
  fs.statSync(path.join(pluginsDir, d)).isDirectory()
);

for (const pluginName of plugins) {
  const pluginDir = path.join(pluginsDir, pluginName);
  const manifestPath = path.join(pluginDir, '.claude-plugin', 'plugin.json');
  
  // Check manifest exists
  if (!fs.existsSync(manifestPath)) {
    console.error(`✗ ${pluginName}: Missing .claude-plugin/plugin.json`);
    errors++;
    continue;
  }
  
  // Parse manifest
  let manifest;
  try {
    manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  } catch (e) {
    console.error(`✗ ${pluginName}: Invalid plugin.json: ${e.message}`);
    errors++;
    continue;
  }
  
  // Check required fields
  if (!manifest.name) { console.error(`✗ ${pluginName}: Missing name`); errors++; }
  if (!manifest.version) { console.error(`✗ ${pluginName}: Missing version`); errors++; }
  
  // Check skills are flat (1 level only)
  const skillsDir = path.join(pluginDir, 'skills');
  if (fs.existsSync(skillsDir)) {
    const skills = fs.readdirSync(skillsDir).filter(d =>
      fs.statSync(path.join(skillsDir, d)).isDirectory()
    );
    
    let skillCount = 0;
    for (const skill of skills) {
      const skillMd = path.join(skillsDir, skill, 'SKILL.md');
      if (!fs.existsSync(skillMd)) {
        console.error(`✗ ${pluginName}: Missing SKILL.md in skills/${skill}/`);
        errors++;
      } else {
        skillCount++;
      }
    }
    console.log(`✓ ${pluginName} v${manifest.version}: ${skillCount} skills`);
  }
}

if (errors > 0) {
  console.error(`\n✗ ${errors} error(s) found`);
  process.exit(1);
} else {
  console.log(`\n✓ All plugins valid`);
}
