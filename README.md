# FitCorp Wellness

Salesforce DX source for a corporate wellness sales and service demo. The target is the Developer Edition org at `mindful-otter-ce9khx-dev-ed.trailblaze.my.salesforce.com`. Core metadata was deployed and verified on 2026-09-30; see `docs/deployment-evidence.md`.

## Source included

- Five custom objects: Membership, Trainer, Session, Feedback, and Trainer Assignment.
- Account, Case, Membership, and Trainer relationships, including master-detail and a two-master junction object.
- Fields showing text, number, currency, picklist, multi-select, formula, summary, lookup, master-detail, checkbox, date, and auto-number.
- Lightning app, object tabs, five curated page layouts, three role-oriented permission sets, and five validation rules.
- Bulk-safe Session date trigger and five Apex tests covering 200 records, validation boundaries, and rejected records.
- Repeatable demo-data script with a client, opportunity, membership, trainer, assignment, and 200 sessions.

Object, field, app, tab, permission, and validation XML is generated from `scripts/generate_metadata.py`. The layouts were retrieved from the org and curated with `scripts/update_layouts.py`. The current user was assigned `FitCorp_Manager` to access the app and custom fields during verification.

## Deploy

Use Node 22 or newer with the official Salesforce CLI. Then:

```bash
npm install
npx sf org login web --instance-url https://mindful-otter-ce9khx-dev-ed.trailblaze.my.salesforce.com --alias fitcorp --set-default
python3 scripts/generate_metadata.py
npx sf project deploy start --dry-run --source-dir force-app --target-org fitcorp
npx sf project deploy start --source-dir force-app --target-org fitcorp
npx sf apex run test --tests SessionDateGuardTest --tests FitCorpValidationTest --target-org fitcorp --result-format human --code-coverage
npx sf apex run --file scripts/apex/seed.apex --target-org fitcorp
```

Run an org dry run and resolve its diagnostics before the real deployment. The seed script is idempotent for its named demo records.

## Configuration and learning work

For a plain-language, end-to-end explanation of the business story, live behavior, demo, and planned features, read [docs/project-walkthrough-hindi.md](docs/project-walkthrough-hindi.md).

See [docs/implementation-plan.md](docs/implementation-plan.md) for the remaining org-specific security, flows, approval, cloud features, and QA scenarios. Feature availability and licenses must be checked in the target org before enabling Experience, Entitlements, or Commerce.

Permission sets add access; they cannot remove rights already granted by a profile. Assign only the appropriate set to each user and review profile grants before using the discount field as a security demonstration.
# salesforce-qa
# salesforce-qa
