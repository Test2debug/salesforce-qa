# FitCorp Wellness: project ka poora safar

**Kiske liye:** Business user, Salesforce beginner, developer aur interviewer.
**Current status:** 30 September 2026 ko data model, Lightning app, layouts, permissions, validation rules aur Apex date check Salesforce org `fitcorp` mein deploy aur test hue. Baaki ideas ko neeche **future work** kaha gaya hai.

## 1. Ek minute mein samjho

FitCorp companies ko employee wellness plans bechne ka demo system hai. Ek company ka record banta hai, sales team uske saath deal track karti hai, company ko membership di jaati hai, trainer assign hota hai, wellness sessions schedule hote hain, aur support team issue aur feedback dekh sakti hai.

Socho ek office 200 employees ke liye yoga plan leta hai. System mein office ka naam, plan ki dates, 200 seats, trainer, aur har yoga session ka record milta hai. Galat date ya invalid discount save karne par Salesforce turant rokta hai.

**Zaroori distinction:** Aaj membership sales deal jeetne par apne aap nahi banti. Demo mein records seed script se banaye gaye hain; real users app se manually bhi bana sakte hain. Closed Won se automatic membership banana future work hai.

## 2. Business story: shuru se ant tak

| Step | Asli duniya mein | Salesforce mein |
| --- | --- | --- |
| 1. Company se baat | FitCorp ko naya corporate client milta hai | **Account** mein company, **Contact** mein uska HR contact |
| 2. Deal | Sales team plan aur price discuss karti hai | **Opportunity** mein deal, amount aur discount |
| 3. Service agreement | Client ko plan, dates aur seats milti hain | **Membership** mein plan, start/end date, status, fee aur benefits |
| 4. Trainer | Yoga/Fitness expert ko client se jodte hain | **Trainer** aur **Trainer Assignment** |
| 5. Delivery | Sessions schedule aur track hote hain | **Session** mein date, duration, trainer, status |
| 6. Support | Client issue batata ya rating deta hai | Standard **Case** aur custom **Feedback** |

Ye ek business journey hai. Har step ko jodne wale record aur rules ke kaaran team ko alag spreadsheets maintain nahi karni padti.

## 3. Salesforce ko bilkul basic se samjho

- **Object** ek register ya spreadsheet ki tarah hai: Account register mein companies, Session register mein classes.
- **Record** us register ki ek row hai: `FitCorp Demo Client` ek Account record.
- **Field** row ka ek column hai: Membership ki `End Date`.
- **Relationship** do registers ka link hai: Session kis Membership ka hai.
- **Validation rule** form ka guard hai: galat value save hone se rokta hai.
- **Trigger** save ke samay chalne wala code hai: yahaan session ki date check karta hai.
- **Permission set** user ko diye gaye extra access ka bundle hai.
- **Lightning app, tab aur layout** screen par cheezen dikhane aur navigate karne ka tareeqa hain; ye apne aap business automation nahi chalate.

Salesforce standard objects **Account, Contact, Opportunity, Case** deta hai. Is project ke custom objects ka naam `__c` se khatam hota hai: `Membership__c`, `Trainer__c`, `Trainer_Assignment__c`, `Session__c`, `Feedback__c`. Ye API names code aur integrations mein use hote hain; inhe badalne se references toot sakte hain.

## 4. Data ek doosre se kaise judta hai

```text
Account (company) ── Contact (company ka vyakti)
       │
       ├── Opportunity (sales deal; abhi Membership se direct link nahi)
       └── Membership (plan, dates, seats)
                ├── Session ── Trainer
                └── Trainer Assignment ── Trainer

Case (support issue) ── Feedback (optional link)
```

**Account → Membership:** Membership ka `Account__c` required lookup hai; plan kisi company se linked hona chahiye.

**Membership → Session:** Master-detail relationship hai. Session apni membership se tightly linked hai; Salesforce parent ke saath ownership/access handle karta hai. Membership par `Total_Sessions__c` roll-up summary Session records gin sakti hai.

**Membership ↔ Trainer:** `Trainer_Assignment__c` junction object hai. Ek membership par kai trainers, aur ek trainer kai memberships par ho sakta hai. Dono taraf master-detail hai.

**Session → Trainer:** Session par trainer ka lookup hai. Assignment aur Session trainer link alag records hain; abhi koi automatic rule verify nahi karta ki Session wala trainer us Membership par assigned bhi hai.

**Feedback → Case:** Feedback chahe to support Case se link ho sakta hai; link optional hai.

## 5. Har screen par kya rakha hai

**Account aur Contact:** Company aur uska contact. Ye Salesforce ke standard records hain. Demo client `FitCorp Demo Client` aur contact `Asha Wellness HR` hain.

**Opportunity:** Deal ka amount aur stage. Do custom fields hain: `Discount__c` (percent) aur `Discount_Approval_Status__c` (Not Required, Pending, Approved, Rejected). Demo Opportunity `FitCorp Corporate Wellness Pilot` hai, Amount 120000 aur Discount 20%. Seed data mein stage `Prospecting` hai; ise Closed Won samajhna galat hoga.

**Membership:** Plan Type (Starter/Growth/Enterprise), Start Date, End Date, Status (Draft/Active/Expired/Cancelled), Seats, Monthly Fee aur Benefits (Gym/Yoga/Nutrition/Equipment). `Days_Remaining__c` formula End Date minus today dikhata hai. Ye live calculated value hai; reminder email nahi bhejti. `Total_Sessions__c` child Session records count karta hai; completed sessions ka count nahi hai.

**Trainer:** Expert ka naam, specialization, hourly rate aur active checkbox. `Active__c` abhi informational field hai; inactive trainer ko assign hone se rokne wala rule nahi hai.

**Trainer Assignment:** Kis membership ko kaunsa trainer diya gaya, assignment date aur active flag. Iska number `TRA-0001` jaise automatically banta hai.

**Session:** Kis membership ka session hai, date, optional trainer, duration aur Scheduled/Completed/Cancelled status. Number `SES-0001` jaise automatically banta hai. Date membership ke start aur end ke beech, dono boundary dates samet, honi chahiye.

**Case aur Feedback:** Case Salesforce ka standard support ticket hai. Feedback mein 1–5 rating, comments aur optional Case link hai. Feedback number `FEE-0001` jaise automatically banta hai. Case escalation ya SLA automation abhi configured nahi hai.

## 6. Save dabane par kya hota hai

### Membership

1. User Account, plan, start/end date aur seats fill karta hai.
2. Required fields check hote hain.
3. Validation rule end date ko start date se pehle save nahi hone deta.
4. Seats zero ya negative hon to doosra rule save rokta hai.
5. Valid record save hota hai. Formula `Days_Remaining__c` aur roll-up `Total_Sessions__c` screen par calculated values dete hain.

### Opportunity

- Closed Won stage ke liye Amount zero se zyada hona chahiye.
- 20% discount allowed hai. 20% se **zyada** discount tabhi save hota hai jab `Discount_Approval_Status__c = Approved` ho.
- Status field par `Approved` choose karna **actual approval process nahi** hai. Approval submission, approver aur audit trail future work hain. Production mein is field ko kaun edit kar sakta hai aur approval sequence kya hoga, alag se design karna zaroori hai.

### Session

1. User membership aur session date deta hai.
2. `SessionDateGuard` trigger **before insert** aur **before update** chalta hai.
3. Trigger batch ke saare Membership IDs ikattha karke ek query se unki dates laata hai.
4. Agar Session Date membership range ke bahar ho to us record par error lagata hai; Salesforce save reject karta hai.
5. Valid Session save hone par Membership ka `Total_Sessions__c` roll-up count update hota hai.

Batch mein IDs ek saath query karna isliye important hai ki 200 Sessions ki processing mein har Session par alag database query na chale. Date check ki boundary inclusive hai: start date aur end date par session allowed hai.

### Feedback

Rating required hai. Validation rule 1 se kam ya 5 se zyada rating reject karta hai. Comment aur Case link optional hain.

## 7. Access ka model

Project mein teen permission sets hain:

| User | Project mein diya gaya kaam |
| --- | --- |
| **FitCorp Sales Rep** | Opportunity aur Membership create/edit; Trainer, Session aur Feedback read; Trainer Assignment create/edit |
| **FitCorp Support Agent** | Case, Session aur Feedback create/edit; Membership, Trainer aur Trainer Assignment read |
| **FitCorp Manager** | Opportunity, Case aur paanchon custom objects create/edit; Discount aur approval status fields edit |

Permission sets object aur field access **add** karte hain; existing profile access ko remove nahi karte. Sales Rep permission set mein discount fields read-only hain, lekin agar uska profile edit access de, effective access alag ho sakta hai. `Membership__c` aur `Trainer__c` metadata mein private sharing model hai; full role hierarchy, sharing rules aur multiple users ke saath visibility test abhi pending hai. Isliye production-level security claim abhi mat karo. Current org user ko `FitCorp_Manager` assign kiya gaya tha taaki demo verify ho sake.

## 8. Demo mein kya dekhna hai

1. Salesforce App Launcher se **FitCorp Wellness** kholo. Account, Contact, Opportunity, Case, Membership, Trainer, Session, Feedback aur Trainer Assignment tabs milenge.
2. Account `FitCorp Demo Client` dekho; uske Contact mein `Asha Wellness HR` dekho.
3. Opportunity `FitCorp Corporate Wellness Pilot` dekho: Amount 120000, Discount 20%, stage Prospecting.
4. Membership `FitCorp Demo Membership` dekho: Growth plan, 200 seats, Gym aur Yoga benefits, current-date se ek saal tak dates. `Total Sessions` 200 aur `Days Remaining` live calculation dikhna chahiye.
5. Trainer `Mira Demo Trainer` aur uska Trainer Assignment dekho.
6. Membership ke Sessions mein 200 **Scheduled** demo sessions hain. Ye test data hai, 200 classes ke actually deliver hone ka evidence nahi.
7. Ek test Session ko Membership ki End Date ke baad ki date se save karo: date error aana chahiye. Phir valid date se save karke check karo. Demo data ko preserve karna ho to naya test record use karo.
8. Negative checks: zero seats, Membership End Date before Start Date, Feedback rating 6, Closed Won with blank Amount, aur 20% se zyada unapproved discount save nahi hone chahiye.

Seed script named demo records ko dobara create nahi karta agar woh pehle se mil jaate hain. Ye complete data reset ya sync tool nahi hai; existing records ko refresh nahi karta.

## 9. Source code ka map

| Path | Kya hai |
| --- | --- |
| `force-app/main/default/objects/` | Objects, fields aur validation rules |
| `force-app/main/default/applications/` aur `tabs/` | FitCorp Lightning app aur navigation |
| `force-app/main/default/layouts/` | Paanch custom object page layouts |
| `force-app/main/default/permissionsets/` | Sales, Support aur Manager access bundles |
| `force-app/main/default/triggers/SessionDateGuard.trigger` | Session date ka Apex guard |
| `force-app/main/default/classes/` | Trigger aur validation ke Apex tests |
| `scripts/apex/seed.apex` | Demo records aur 200 Sessions |
| `scripts/soql-practice.md` | Query examples |
| `docs/deployment-evidence.md` | Deployment aur test ka recorded evidence |
| `docs/implementation-plan.md` | Abhi pending feature plan |

`scripts/generate_metadata.py` metadata source generate karta hai. `scripts/update_layouts.py` page layouts curate karta hai. Deployment se pehle `sf project deploy start --dry-run --source-dir force-app --target-org fitcorp` chalana project rule hai; destructive manifest use nahi karna.

## 10. Kya prove hua, kya abhi banana hai

**Deployed aur verified:** Five custom objects, standard-object custom fields, relationships, app/tabs/layouts, three permission sets, five validation rules, Session trigger, 200 demo Sessions, aur five Apex tests. Recorded test run mein 5 pass, 0 fail aur reported coverage 100% tha. Ye coverage current Apex scope ki hai, poore business process ki completeness ka percentage nahi.

**Abhi pending:** Closed Won se automatic Membership/Order, onboarding screen flow, expiry reminder, Case SLA escalation, real discount approval process, role hierarchy/sharing verification, full lead-to-order process, reports/dashboard, customer portal, Experience/Commerce configuration. Inmein se kuch org license/settings par depend karenge. `docs/implementation-plan.md` mein inka sequence aur QA scenarios hain.

## 11. Interview mein 45 second ka answer

> “Maine FitCorp naam ka corporate wellness Salesforce demo banaya. Account aur Opportunity se client aur deal track hoti hai. Membership plan aur validity rakhti hai; Trainer Assignment se trainers jodte hain; Session records delivery schedule rakhte hain; Case aur Feedback support ko cover karte hain. Data quality ke liye membership dates, seats, discounts aur ratings par validation rules hain. Session date ko membership period ke andar rakhne ke liye bulk-safe Apex trigger hai. Lightning app, layouts aur role-oriented permission sets se users ko relevant UI aur access milta hai. Project org mein deploy hua, 5 Apex tests pass hue, aur 200 demo sessions se batch behavior verify hua. Approval, flows, sharing verification aur portal agle phase mein hain.”

## 12. Teen baatein jo hamesha yaad rakho

1. **Deal aur Membership abhi manually connected business steps hain; automatic flow nahi.** Opportunity se Membership banne ka logic future work hai.
2. **Validation field ko check karti hai; approval workflow nahi chalati.** `Approved` status ko actual manager approval samajhkar present na karo.
3. **Demo data aur production usage alag hain.** 200 Scheduled Sessions seed script se bane the. Ye trigger aur roll-up test karne ke kaam aate hain.

Aur detail ke liye [deployment evidence](deployment-evidence.md), [implementation plan](implementation-plan.md) aur project ka [README](../README.md) dekho.
