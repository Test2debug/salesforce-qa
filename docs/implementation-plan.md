# FitCorp implementation and QA plan

## Current deliverable

The repository contains deployed Salesforce DX source for the data model, app, validations, permission sets, and Apex date guard. See `deployment-evidence.md` for deployment and test results. No org feature below should be described as built until it has been enabled and tested.

## Org setup after source deployment

1. **Security:** Set Account and Membership organization-wide defaults to Private if available. Create the CEO → Sales Head → Sales Rep role hierarchy. Add a criteria sharing rule for active memberships to support staff and an owner-based rule for Sales Head. Set login hours and IP ranges only after collecting the actual team requirements; changing these blindly can lock users out. Review password policy without weakening existing controls.
2. **Users:** Create one Sales Rep, one Support Agent, and one Manager test user only if spare licenses exist. Assign the matching permission set. Use Login As to verify record, object, and field visibility. Profiles provide the baseline; permission sets add rights.
3. **Opportunity automation:** Build a record-triggered flow on transition to Closed Won. Check for an existing Membership linked to the Opportunity before creating one; populate the Account, plan, start/end dates, status, and seats. Create an Order only when the org's Order settings and pricebook data allow it. Add a fault path that records the failure. Test one record and a 200-record bulk update.
4. **Onboarding:** Build a screen flow for Account, primary Contact, and Membership. Validate required values, show a confirmation screen, and test duplicate Account handling.
5. **Expiry reminder:** Build a scheduled flow for Active Memberships whose End Date is seven days away. Send a notification to an internal owner only after deciding the recipient and email template. Test with a date-controlled record.
6. **Case escalation:** Build a record-triggered flow or escalation rule that raises priority when a Case breaches the chosen SLA. Agree on business hours and queue ownership before activation.
7. **Discount approval:** Add an approval process for Opportunity discounts over 20%. The supplied validation rule blocks unapproved >20% values, so design the submission sequence to avoid preventing the initial save. A practical option is a separate requested-discount field, with the approved value copied to Discount only after approval.
8. **Sales and service:** Create Product2, a Pricebook and Pricebook Entries, then run Lead → conversion → Opportunity → Quote → Order → Case. Configure Campaigns and a small Web-to-Lead test. Enable Email-to-Case, Entitlements, and Knowledge only if the org supports them.
9. **Experience and Commerce:** Check licenses and site availability. If Experience Cloud is available, create a customer portal that shows only the current account's Cases and Memberships. Use standard Product2/Pricebook/Order for the commerce demonstration when B2B Commerce is unavailable.
10. **Analytics:** Make a membership summary report, an opportunity pipeline report, and a dashboard. Keep screenshots and test evidence. Reports and dashboard content depend on deployed data and org feature availability.

## QA scenarios

| Area | Positive | Negative or boundary |
| --- | --- | --- |
| Membership dates | End equals Start | End before Start rejected |
| Seats | 1 accepted | 0 rejected |
| Feedback | Rating 1 and 5 accepted | 0 and 6 rejected |
| Opportunity | 20% discount allowed | 20.01% needs approval; Closed Won without Amount rejected |
| Session trigger | 200 sessions on boundary dates inserted | Date outside membership rejected |
| Sharing | Manager sees subordinate record | Peer Sales Rep cannot see a private record |
| FLS | Manager can edit Discount | Sales Rep cannot edit Discount after profile review |
| Lead conversion | New Account/Contact/Opportunity created | Duplicate Account and missing required data handled |
| Deployment | Dry run and test class pass | Regression check after metadata changes |

Record actual results, org ID, date, and screenshots before claiming any scenario passed.
