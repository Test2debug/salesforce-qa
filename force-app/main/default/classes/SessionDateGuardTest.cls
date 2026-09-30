@IsTest
private class SessionDateGuardTest {
    @IsTest
    static void acceptsBoundaryDatesAndHandlesBulk() {
        Account client = new Account(Name = 'FitCorp Test Client');
        insert client;
        Membership__c membership = new Membership__c(
            Name = 'Test Membership', Account__c = client.Id,
            Plan_Type__c = 'Starter', Start_Date__c = Date.newInstance(2026, 1, 1),
            End_Date__c = Date.newInstance(2026, 12, 31), Status__c = 'Active',
            Seats__c = 200
        );
        insert membership;

        List<Session__c> sessions = new List<Session__c>();
        for (Integer i = 0; i < 200; i++) {
            sessions.add(new Session__c(
                Membership__c = membership.Id,
                Session_Date__c = i == 0 ? membership.Start_Date__c : membership.End_Date__c,
                Status__c = 'Scheduled'
            ));
        }
        Test.startTest();
        insert sessions;
        Test.stopTest();
        System.assertEquals(200, [SELECT COUNT() FROM Session__c WHERE Membership__c = :membership.Id]);
    }

    @IsTest
    static void rejectsDatesOutsideMembership() {
        Account client = new Account(Name = 'FitCorp Test Client');
        insert client;
        Membership__c membership = new Membership__c(
            Name = 'Test Membership', Account__c = client.Id,
            Plan_Type__c = 'Starter', Start_Date__c = Date.newInstance(2026, 1, 1),
            End_Date__c = Date.newInstance(2026, 12, 31), Status__c = 'Active',
            Seats__c = 1
        );
        insert membership;

        Session__c invalidSession = new Session__c(
            Membership__c = membership.Id,
            Session_Date__c = Date.newInstance(2027, 1, 1),
            Status__c = 'Scheduled'
        );
        Database.SaveResult result = Database.insert(invalidSession, false);
        System.assertEquals(false, result.isSuccess());
        System.assert(result.getErrors()[0].getMessage().contains('membership dates'));
    }
}
