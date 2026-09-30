# SOQL and SOSL practice

Run queries through `sf data query --target-org fitcorp --query '<SOQL>'` after data is loaded.

```sql
SELECT Name, (SELECT Name FROM Opportunities) FROM Account LIMIT 20
SELECT Name, Account.Name FROM Contact WHERE AccountId != null LIMIT 20
SELECT Account__r.Name, COUNT(Id) FROM Membership__c GROUP BY Account__r.Name HAVING COUNT(Id) > 0 ORDER BY COUNT(Id) DESC
SELECT Name, Total_Sessions__c, Days_Remaining__c FROM Membership__c ORDER BY End_Date__c ASC LIMIT 20
SELECT Membership__r.Name, Session_Date__c, Trainer__r.Name FROM Session__c ORDER BY Session_Date__c DESC LIMIT 20
```

In Developer Console Query Editor, use SOSL:

```sql
FIND {FitCorp} IN ALL FIELDS RETURNING Account(Name), Contact(Name)
```
