# Quality Checklist Template

## Responsaveis

- **Owner:** PM + Tech Lead
- **Contribuem:** Dev team, QA
- **Aprovacao:** PM + Tech Lead

Use this template as a guide to structure quality-checklist.md.

```markdown
# Quality Checklist — Pre-Release Validation

**Release:** MVP v1.0
**Release Date:** 2026-04-30
**Target Users:** Beta (internal + 50 external testers)

---

## Pre-Release Checklist

### Functionality

Validate that all user stories work according to acceptance criteria.

| Criterion | User Story | Test Case | Status | Approved By |
|----------|-----------|-----------|--------|------------|
| User can sign up | US-1 | TS-001: Sign up flow | ☐ | PM |
| Authentication via email/password | US-5 | TS-002: Login fails on invalid password | ☐ | QA |
| Dashboard loads user data | US-3 | TS-003: Dashboard displays user info within 2s | ☐ | QA |
| User can log out | US-5 | TS-004: Session destroyed after logout | ☐ | QA |
| Errors return correct HTTP status | — | TS-005: 404 for missing resource, 401 for auth | ☐ | QA |

**Pass Criteria:** 100% acceptance criteria validated, 0 critical bugs, <5 minor bugs

**Evidence Required:**
- Test execution report (TS-001 to TS-005 all PASS)
- Screenshot of final test results
- Bug log (if any minor issues, linked to backlog)

---

### Performance

Validate performance NFRs.

| NFR | Target | Actual | Test Method | Status | Approved By |
|-----|--------|--------|-------------|--------|------------|
| NFR-1: API response time | <500ms p95 | — | Load test 1000 RPS | ☐ | Arch |
| NFR-2: Dashboard load time | <2s p95 | — | Lighthouse (network: 4G) | ☐ | Frontend |
| NFR-3: Database query latency | <100ms p99 | — | Query profiler on prod-like data | ☐ | Backend |
| NFR-4: Concurrent users | ≥1000 | — | Load test 30min sustained | ☐ | QA |
| NFR-5: Memory footprint | <200MB | — | Heap profiler on API | ☐ | Infra |

**Pass Criteria:** All targets met or exceeded

**Test Evidence Required:**
- Load test report (JMeter/k6)
- Lighthouse report (desktop + mobile)
- Database profiling output
- Memory profiling report
- Sustained load test with no errors

---

### Security

Validate protection against OWASP Top 10 vulnerabilities.

| Security Check | Vulnerability | Test | Status | Approved By |
|----------------|---------------|------|--------|------------|
| SQL Injection | A3:2021 – Injection | Run SQLmap against login form | ☐ | Security |
| XSS Prevention | A3:2021 – Injection | Input field: `<script>alert('xss')</script>` | ☐ | Security |
| CSRF Tokens | A4:2021 – CRLF | Verify CSRF token in state-changing requests | ☐ | Security |
| Password Hashing | Weak crypto | Verify bcrypt (salt rounds ≥10) | ☐ | Backend |
| TLS/HTTPS | Data in transit | Check SSL/TLS cert, no mixed content | ☐ | Infra |
| Authentication | A7:2021 – Auth failures | Brute force: 100 login attempts/min → rate limited | ☐ | Security |
| API Authorization | A1:2021 – Broken AC | Try accessing other users' data (negative test) | ☐ | QA |
| Secrets Management | Exposed credentials | Verify no API keys in code, .env not committed | ☐ | DevOps |
| Dependency audit | Supply chain | Run `npm audit`, `go mod audit` → 0 critical | ☐ | DevOps |
| Headers | Misconfiguration | Check: CSP, X-Frame-Options, X-Content-Type-Options | ☐ | Infra |

**Pass Criteria:** All checks PASS, 0 critical vulnerabilities, remediate high-severity within 48h

**Evidence Required:**
- Security scan reports (OWASP ZAP, Snyk, etc.)
- Code review sign-off (security specialist)
- Dependency audit report
- Penetration test summary (if applicable)

---

### Accessibility

Validate WCAG 2.1 Level AA compliance.

| WCAG Criterion | Test | Status | Approved By |
|----------------|------|--------|------------|
| 1.4.3 Contrast | Text contrast ≥4.5:1 (WCAG AA) | ☐ | Design |
| 2.1.1 Keyboard | All functions operable via keyboard | ☐ | QA |
| 2.4.3 Focus Order | Tab order logical and visible | ☐ | QA |
| 3.3.1 Error Identification | Errors described clearly (not just red color) | ☐ | QA |
| 4.1.2 Name/Role/Value | Screen reader announces buttons correctly | ☐ | QA |

**Pass Criteria:** 100% WCAG AA compliance

**Test Tools:**
- axe DevTools (Chrome extension)
- NVDA screen reader (Windows)
- WAVE (WebAIM)

**Evidence Required:**
- Accessibility audit report
- Screen reader testing session recording
- Keyboard navigation walkthrough

---

### Documentation

Validate that documentation is complete and accurate.

| Document | Requirement | Status | Approved By |
|----------|-------------|--------|------------|
| README.md | Setup, quick start, troubleshooting | ☐ | Tech Lead |
| API Docs | All endpoints documented, examples working | ☐ | Backend |
| User Guide | Feature walkthroughs, screenshots | ☐ | Product |
| Release Notes | What's new, breaking changes, migration guide | ☐ | PM |
| Architecture Docs | System diagram, data flow, deployment | ☐ | Arch |
| Runbook | How to monitor, debug, scale | ☐ | DevOps |

**Pass Criteria:** All documents present, reviewed, <5% outdated info

---

### Deployment & Operations

Validate that deployment is safe, monitored, and reversible.

| Check | Requirement | Status | Approved By |
|-------|-------------|--------|------------|
| Deployment Plan | Step-by-step runbook, rollback procedure | ☐ | DevOps |
| Monitoring | Dashboards created, alerts configured | ☐ | DevOps |
| Logging | All errors logged with context | ☐ | DevOps |
| Backups | Database backups tested, restore validated | ☐ | DevOps |
| Staging Deployment | Identical to prod, tested with real data | ☐ | QA |
| Canary Release | 5% traffic → 50% → 100% (if applicable) | ☐ | DevOps |
| Incident Response | War room setup, escalation path clear | ☐ | PM |

**Pass Criteria:** All deployment steps documented and practiced, zero surprises on deploy day

---

## NFR Validation Table

Link NFRs to tech-spec.md with specific validation tests.

| NFR-# | Requirement | Target | Validation Test | Evidence | Status |
|-------|-------------|--------|-----------------|----------|--------|
| NFR-1 | API response p95 | <500ms | Load test 1000 RPS | LT-001.pdf | ☐ |
| NFR-2 | Uptime SLA | ≥99.5% | Monitor for 30 days | Uptime report | ☐ |
| NFR-3 | Data consistency | 100% | Verify audit logs match DB | Audit report | ☐ |
| NFR-4 | Latency p99 | <1s | Real user monitoring | RUM data | ☐ |
| NFR-5 | Throughput | ≥10k req/s | Load test sustained | LT-002.pdf | ☐ |

---

## Test Coverage Requirements

Minimum coverage thresholds before GA.

| Layer | Type | Minimum Coverage | Current | Status |
|-------|------|------------------|---------|--------|
| Unit | Code coverage | 80% | 82% | ✅ |
| Unit | Branch coverage | 75% | 79% | ✅ |
| Integration | API endpoints | 100% documented | 100% | ✅ |
| E2E | Critical paths | 100% | 95% | ⚠️ Checkout flow missing |
| Manual | UAT | 100% of features | 90% | ⚠️ Payment scenarios pending |

**Pass Criteria:** All thresholds met

**Evidence Required:**
- Coverage reports (Istanbul, gcov, etc.)
- Test execution summary
- Gaps analysis and plan to close

---

## Sign-Off Matrix

Release approval gates.

| Role | Responsibility | Deadline | Sign-Off |
|------|-----------------|----------|----------|
| **QA Lead** | Functional testing, bug triage | 2026-04-25 | ☐ Alice |
| **Security** | Vulnerability assessment, compliance | 2026-04-26 | ☐ Bob |
| **DevOps** | Deployment readiness, monitoring | 2026-04-27 | ☐ Charlie |
| **Tech Lead** | Architecture review, code quality | 2026-04-28 | ☐ Diana |
| **Product Manager** | User acceptance, feature parity | 2026-04-29 | ☐ Eve |
| **Executive Sponsor** | Go/No-Go decision | 2026-04-30 | ☐ Frank |

**Gate Logic:**
- All sign-offs required for MVP release
- One escalation path: If any sign-off blocked, escalate to Tech Lead
- No release without all boxes checked

---

## Release Decision

After all checks complete:

**Release Status:**
- ☐ **GO** — All checks passed, ready for production
- ☐ **GO with conditions** — Minor issues identified, mitigation plan documented
- ☐ **HOLD** — Critical issues, cannot release until resolved
- ☐ **NO-GO** — Major blockers, cancel or defer release

**Decision Date:** [To be filled on release day]
**Approved By:** [Executive sign-off]
**Release Time:** [Window TBD based on deployment plan]
```

## Notes

- Update this checklist throughout Sprint 6 (release sprint)
- Escalate blockers immediately to Tech Lead
- Keep evidence artifacts in shared folder (test reports, scan results)
- Final sign-off from all 6 roles required before going to production

## O que fazer / O que nao fazer

**O que fazer:**
- Verificar cada US-# com criterio de aceite
- Checar NFR-# targets com evidencia de medicao
- Incluir plano de rollback antes do lancamento
- Documentar cobertura de testes (unit, integration, E2E)

**O que nao fazer:**
- Nao aprovar sem evidencia (teste rodou? metrica bateu?)
- Nao pular checklist de seguranca para "ir mais rapido"
- Nao confundir quality checklist com test plan
- Nao lancar sem monitoramento configurado

