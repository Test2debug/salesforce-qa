// Demo records only. Run after metadata deployment with:
// sf apex run --file scripts/apex/seed.apex --target-org fitcorp
List<Account> existingClients = [SELECT Id FROM Account WHERE Name = 'FitCorp Demo Client' LIMIT 1];
Account client;
if (existingClients.isEmpty()) {
    client = new Account(Name = 'FitCorp Demo Client', Industry = 'Technology');
    insert client;
} else {
    client = existingClients[0];
}

if ([SELECT COUNT() FROM Contact WHERE AccountId = :client.Id AND LastName = 'Wellness HR'] == 0) {
    insert new Contact(FirstName = 'Asha', LastName = 'Wellness HR', AccountId = client.Id);
}
if ([SELECT COUNT() FROM Opportunity WHERE AccountId = :client.Id AND Name = 'FitCorp Corporate Wellness Pilot'] == 0) {
    insert new Opportunity(
        Name = 'FitCorp Corporate Wellness Pilot', AccountId = client.Id,
        StageName = 'Prospecting', CloseDate = Date.today().addDays(30), Amount = 120000,
        Discount__c = 20
    );
}

List<Membership__c> existingMemberships = [
    SELECT Id FROM Membership__c WHERE Name = 'FitCorp Demo Membership' LIMIT 1
];
Membership__c membership;
if (existingMemberships.isEmpty()) {
    membership = new Membership__c(
        Name = 'FitCorp Demo Membership', Account__c = client.Id,
        Plan_Type__c = 'Growth', Start_Date__c = Date.today(),
        End_Date__c = Date.today().addYears(1), Status__c = 'Active',
        Seats__c = 200, Monthly_Fee__c = 25000, Benefits__c = 'Gym;Yoga'
    );
    insert membership;
} else {
    membership = existingMemberships[0];
}

List<Trainer__c> existingTrainers = [
    SELECT Id FROM Trainer__c WHERE Name = 'Mira Demo Trainer' LIMIT 1
];
Trainer__c trainer;
if (existingTrainers.isEmpty()) {
    trainer = new Trainer__c(
        Name = 'Mira Demo Trainer', Specialization__c = 'Yoga',
        Active__c = true, Hourly_Rate__c = 1200
    );
    insert trainer;
} else {
    trainer = existingTrainers[0];
}

if ([SELECT COUNT() FROM Trainer_Assignment__c WHERE Membership__c = :membership.Id AND Trainer__c = :trainer.Id] == 0) {
    insert new Trainer_Assignment__c(
        Membership__c = membership.Id, Trainer__c = trainer.Id,
        Assigned_On__c = Date.today(), Active__c = true
    );
}

if ([SELECT COUNT() FROM Session__c WHERE Membership__c = :membership.Id] == 0) {
    List<Session__c> demoSessions = new List<Session__c>();
    for (Integer i = 0; i < 200; i++) {
        demoSessions.add(new Session__c(
            Membership__c = membership.Id, Trainer__c = trainer.Id,
            Session_Date__c = Date.today().addDays(Math.mod(i, 30)),
            Status__c = 'Scheduled', Duration_Minutes__c = 45
        ));
    }
    insert demoSessions;
}
