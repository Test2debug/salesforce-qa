@IsTest
private class FitCorpValidationTest {
    private static Account makeAccount() {
        Account client = new Account(Name = 'FitCorp Validation Client');
        insert client;
        return client;
    }

    @IsTest
    static void membershipBoundaries() {
        Account client = makeAccount();
        Membership__c membership = new Membership__c(
            Name = 'Boundary Membership', Account__c = client.Id,
            Plan_Type__c = 'Starter', Start_Date__c = Date.today(),
            End_Date__c = Date.today(), Status__c = 'Active', Seats__c = 1
        );
        insert membership;

        membership.End_Date__c = Date.today().addDays(-1);
        Database.SaveResult badDate = Database.update(membership, false);
        System.assertEquals(false, badDate.isSuccess(), 'Earlier end date must fail');

        membership.End_Date__c = Date.today();
        membership.Seats__c = 0;
        Database.SaveResult badSeats = Database.update(membership, false);
        System.assertEquals(false, badSeats.isSuccess(), 'Zero seats must fail');
    }

    @IsTest
    static void feedbackRatings() {
        insert new Feedback__c(Rating__c = 1);
        insert new Feedback__c(Rating__c = 5);
        System.assertEquals(false, Database.insert(new Feedback__c(Rating__c = 0), false).isSuccess());
        System.assertEquals(false, Database.insert(new Feedback__c(Rating__c = 6), false).isSuccess());
    }

    @IsTest
    static void opportunityDiscountBoundaryAndApproval() {
        Account client = makeAccount();
        Opportunity opportunity = new Opportunity(
            Name = 'Boundary Deal', AccountId = client.Id,
            StageName = 'Prospecting', CloseDate = Date.today().addDays(14),
            Amount = 1000, Discount__c = 20
        );
        insert opportunity;

        opportunity.Discount__c = 20.01;
        Database.SaveResult unapproved = Database.update(opportunity, false);
        System.assertEquals(false, unapproved.isSuccess(), 'Discount above 20 must fail');

        opportunity.Discount_Approval_Status__c = 'Approved';
        update opportunity;
        opportunity.StageName = 'Closed Won';
        opportunity.Amount = null;
        Database.SaveResult missingAmount = Database.update(opportunity, false);
        System.assertEquals(false, missingAmount.isSuccess(), 'Closed Won requires amount');
    }
}
