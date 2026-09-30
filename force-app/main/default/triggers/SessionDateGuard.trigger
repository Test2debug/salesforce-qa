trigger SessionDateGuard on Session__c (before insert, before update) {
    Set<Id> membershipIds = new Set<Id>();
    for (Session__c sessionRecord : Trigger.new) {
        if (sessionRecord.Membership__c != null && sessionRecord.Session_Date__c != null) {
            membershipIds.add(sessionRecord.Membership__c);
        }
    }

    Map<Id, Membership__c> memberships = new Map<Id, Membership__c>([
        SELECT Id, Start_Date__c, End_Date__c
        FROM Membership__c
        WHERE Id IN :membershipIds
    ]);
    for (Session__c sessionRecord : Trigger.new) {
        Membership__c membership = memberships.get(sessionRecord.Membership__c);
        if (membership != null && sessionRecord.Session_Date__c != null &&
            (sessionRecord.Session_Date__c < membership.Start_Date__c ||
             sessionRecord.Session_Date__c > membership.End_Date__c)) {
            sessionRecord.Session_Date__c.addError('Session Date must fall within the membership dates.');
        }
    }
}
