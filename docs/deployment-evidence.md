# Deployment and test evidence — 2026-09-30

Target: `mindful-otter-ce9khx-dev-ed.trailblaze.my.salesforce.com`, alias `fitcorp`.

| Check | Result |
| --- | --- |
| Salesforce DX source conversion | Passed after layout changes; all current 54 XML metadata files parsed |
| Full metadata dry run | Passed; 48 components, 0 errors |
| Full metadata deployment | Succeeded; 48 components, 0 errors |
| Full-source dry run before layout additions | Passed; 49 components, 0 errors |
| Manager permission update | Dry run and deployment passed; assigned to the current org user |
| Sales and Support field permissions | Dry run and deployment passed for all 3 sets |
| Five FitCorp page layouts | Retrieved, curated, dry-run validated, deployed |
| Discount 20% rule correction | Dry run and deployment passed |
| Apex tests | 5 passed, 0 failed; reported coverage 100% |
| Demo data script | Compiled and ran successfully |
| Demo Membership | `FitCorp Demo Membership` linked to `FitCorp Demo Client`; `Total_Sessions__c = 200` |
| Session count | 200 demo Sessions confirmed with SOQL |
| Demo Opportunity | `FitCorp Corporate Wellness Pilot`, Amount 120000, Discount 20% confirmed with SOQL |

The Apex suite covers date boundaries, invalid membership seats, rating limits, the exact 20% discount boundary, unapproved 20.01%, approved discounts, Closed Won Amount, and a 200-record Session insert. Deployment validation found and resolved a formula enum value and a required lookup delete rule. Automated validation then found and resolved the percent formula threshold; Salesforce formulas compare 20% as `0.20`.

The remaining security hierarchy, flows, approval process, cloud integrations, reports, and portal are listed in `implementation-plan.md`. They have not been configured or verified in the org.
