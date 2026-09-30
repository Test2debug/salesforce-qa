"""Generate the FitCorp Salesforce DX metadata from a compact specification."""

from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1] / "force-app/main/default"
NS = "http://soap.sforce.com/2006/04/metadata"
ET.register_namespace("", NS)


def node(parent, name, value):
    child = ET.SubElement(parent, f"{{{NS}}}{name}")
    child.text = str(value).lower() if isinstance(value, bool) else str(value)
    return child


def write(path, root):
    path.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(root, space="    ")
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def metadata(kind):
    return ET.Element(f"{{{NS}}}{kind}")


def custom_object(api, label, plural, name_type="Text", sharing="Private"):
    root = metadata("CustomObject")
    for key, value in [
        ("label", label), ("pluralLabel", plural),
        ("deploymentStatus", "Deployed"), ("sharingModel", sharing),
        ("enableActivities", True), ("enableReports", True),
        ("enableSearch", True),
    ]:
        node(root, key, value)
    name = ET.SubElement(root, f"{{{NS}}}nameField")
    node(name, "label", f"{label} Name" if name_type == "Text" else f"{label} Number")
    node(name, "type", name_type)
    if name_type == "AutoNumber":
        node(name, "displayFormat", f"{api.split('__')[0][:3].upper()}-{{0000}}")
    write(ROOT / "objects" / api / f"{api}.object-meta.xml", root)


def field(obj, api, label, kind, **options):
    root = metadata("CustomField")
    node(root, "fullName", api)
    node(root, "label", label)
    node(root, "type", kind)
    for key, value in options.items():
        if key == "values":
            value_set = ET.SubElement(root, f"{{{NS}}}valueSet")
            definition = ET.SubElement(value_set, f"{{{NS}}}valueSetDefinition")
            node(definition, "sorted", False)
            for choice in value:
                item = ET.SubElement(definition, f"{{{NS}}}value")
                node(item, "fullName", choice)
                node(item, "default", False)
                node(item, "label", choice)
        else:
            node(root, key, value)
    write(ROOT / "objects" / obj / "fields" / f"{api}.field-meta.xml", root)


def validation(obj, api, formula, message):
    root = metadata("ValidationRule")
    for key, value in [
        ("fullName", api), ("active", True), ("errorConditionFormula", formula),
        ("errorMessage", message),
    ]:
        node(root, key, value)
    write(ROOT / "objects" / obj / "validationRules" / f"{api}.validationRule-meta.xml", root)


def tab(api):
    root = metadata("CustomTab")
    node(root, "customObject", True)
    node(root, "motif", "Custom18: Form")
    write(ROOT / "tabs" / f"{api}.tab-meta.xml", root)


def permissions(api, label, objects, fields, tabs):
    root = metadata("PermissionSet")
    node(root, "label", label)
    app = ET.SubElement(root, f"{{{NS}}}applicationVisibilities")
    node(app, "application", "FitCorp_Wellness")
    node(app, "visible", True)
    for obj, flags in objects.items():
        entry = ET.SubElement(root, f"{{{NS}}}objectPermissions")
        for key, value in [
            ("allowCreate", "c" in flags), ("allowDelete", "d" in flags),
            ("allowEdit", "e" in flags), ("allowRead", "r" in flags),
            ("modifyAllRecords", False), ("object", obj), ("viewAllRecords", False),
        ]:
            node(entry, key, value)
    for full_name, editable in fields.items():
        entry = ET.SubElement(root, f"{{{NS}}}fieldPermissions")
        node(entry, "editable", editable)
        node(entry, "field", full_name)
        node(entry, "readable", True)
    for tab_name in tabs:
        entry = ET.SubElement(root, f"{{{NS}}}tabSettings")
        node(entry, "tab", tab_name)
        node(entry, "visibility", "Visible")
    write(ROOT / "permissionsets" / f"{api}.permissionset-meta.xml", root)


def main():
    custom_object("Membership__c", "Membership", "Memberships")
    custom_object("Trainer__c", "Trainer", "Trainers")
    custom_object("Session__c", "Session", "Sessions", "AutoNumber", "ControlledByParent")
    custom_object("Feedback__c", "Feedback", "Feedback", "AutoNumber")
    custom_object("Trainer_Assignment__c", "Trainer Assignment", "Trainer Assignments", "AutoNumber", "ControlledByParent")

    field("Membership__c", "Account__c", "Client Account", "Lookup", referenceTo="Account", relationshipLabel="Memberships", relationshipName="Memberships", required=True, deleteConstraint="Restrict")
    field("Membership__c", "Plan_Type__c", "Plan Type", "Picklist", values=["Starter", "Growth", "Enterprise"], required=True)
    field("Membership__c", "Start_Date__c", "Start Date", "Date", required=True)
    field("Membership__c", "End_Date__c", "End Date", "Date", required=True)
    field("Membership__c", "Status__c", "Status", "Picklist", values=["Draft", "Active", "Expired", "Cancelled"], required=True)
    field("Membership__c", "Seats__c", "Seats", "Number", precision=6, scale=0, required=True)
    field("Membership__c", "Monthly_Fee__c", "Monthly Fee", "Currency", precision=16, scale=2)
    field("Membership__c", "Benefits__c", "Benefits", "MultiselectPicklist", values=["Gym", "Yoga", "Nutrition", "Equipment"], visibleLines=4)
    field("Membership__c", "Total_Sessions__c", "Total Sessions", "Summary", summaryForeignKey="Session__c.Membership__c", summaryOperation="count")
    field("Membership__c", "Days_Remaining__c", "Days Remaining", "Number", formula="End_Date__c - TODAY()", formulaTreatBlanksAs="BlankAsBlank", precision=6, scale=0)

    field("Trainer__c", "Specialization__c", "Specialization", "Picklist", values=["Fitness", "Yoga", "Nutrition", "Strength"])
    field("Trainer__c", "Active__c", "Active", "Checkbox", defaultValue=True)
    field("Trainer__c", "Hourly_Rate__c", "Hourly Rate", "Currency", precision=16, scale=2)

    field("Session__c", "Membership__c", "Membership", "MasterDetail", referenceTo="Membership__c", relationshipLabel="Sessions", relationshipName="Sessions", relationshipOrder=0, reparentableMasterDetail=False, writeRequiresMasterRead=False)
    field("Session__c", "Trainer__c", "Trainer", "Lookup", referenceTo="Trainer__c", relationshipLabel="Sessions", relationshipName="Sessions")
    field("Session__c", "Session_Date__c", "Session Date", "Date", required=True)
    field("Session__c", "Status__c", "Status", "Picklist", values=["Scheduled", "Completed", "Cancelled"], required=True)
    field("Session__c", "Duration_Minutes__c", "Duration Minutes", "Number", precision=4, scale=0)

    field("Feedback__c", "Case__c", "Support Case", "Lookup", referenceTo="Case", relationshipLabel="Feedback", relationshipName="Feedback")
    field("Feedback__c", "Rating__c", "Rating", "Number", precision=1, scale=0, required=True)
    field("Feedback__c", "Comments__c", "Comments", "LongTextArea", length=2000, visibleLines=4)

    field("Trainer_Assignment__c", "Membership__c", "Membership", "MasterDetail", referenceTo="Membership__c", relationshipLabel="Trainer Assignments", relationshipName="Trainer_Assignments", relationshipOrder=0, reparentableMasterDetail=False, writeRequiresMasterRead=False)
    field("Trainer_Assignment__c", "Trainer__c", "Trainer", "MasterDetail", referenceTo="Trainer__c", relationshipLabel="Trainer Assignments", relationshipName="Trainer_Assignments", relationshipOrder=1, reparentableMasterDetail=False, writeRequiresMasterRead=False)
    field("Trainer_Assignment__c", "Assigned_On__c", "Assigned On", "Date")
    field("Trainer_Assignment__c", "Active__c", "Active", "Checkbox", defaultValue=True)

    field("Opportunity", "Discount__c", "Discount %", "Percent", precision=5, scale=2)
    field("Opportunity", "Discount_Approval_Status__c", "Discount Approval Status", "Picklist", values=["Not Required", "Pending", "Approved", "Rejected"])

    validation("Membership__c", "End_After_Start", "End_Date__c < Start_Date__c", "End Date must be on or after Start Date.")
    validation("Membership__c", "Seats_Positive", "Seats__c <= 0", "Seats must be greater than zero.")
    validation("Feedback__c", "Rating_One_To_Five", "OR(Rating__c < 1, Rating__c > 5)", "Rating must be between 1 and 5.")
    validation("Opportunity", "Discount_Requires_Approval", "AND(Discount__c > 0.20, NOT(ISPICKVAL(Discount_Approval_Status__c, 'Approved')))", "Discounts above 20% require approval.")
    validation("Opportunity", "Closed_Won_Requires_Amount", "AND(ISPICKVAL(StageName, 'Closed Won'), OR(ISBLANK(Amount), Amount <= 0))", "Closed Won opportunities need an Amount greater than zero.")

    custom_tabs = ["Membership__c", "Trainer__c", "Session__c", "Feedback__c", "Trainer_Assignment__c"]
    for api in custom_tabs:
        tab(api)
    app = metadata("CustomApplication")
    node(app, "label", "FitCorp Wellness")
    node(app, "formFactors", "Large")
    node(app, "navType", "Standard")
    node(app, "uiType", "Lightning")
    for tab_name in ["standard-Account", "standard-Contact", "standard-Opportunity", "standard-Case", *custom_tabs]:
        node(app, "tabs", tab_name)
    write(ROOT / "applications/FitCorp_Wellness.app-meta.xml", app)

    obj_read = {obj: "r" for obj in custom_tabs}
    sales_fields = {
        "Opportunity.Discount__c": False,
        "Opportunity.Discount_Approval_Status__c": False,
        "Membership__c.Monthly_Fee__c": True,
        "Membership__c.Benefits__c": True,
        "Membership__c.Total_Sessions__c": False,
        "Membership__c.Days_Remaining__c": False,
        "Trainer__c.Specialization__c": False,
        "Trainer__c.Active__c": False,
        "Trainer_Assignment__c.Assigned_On__c": True,
        "Trainer_Assignment__c.Active__c": True,
    }
    support_fields = {
        "Membership__c.Benefits__c": False,
        "Membership__c.Total_Sessions__c": False,
        "Membership__c.Days_Remaining__c": False,
        "Trainer__c.Specialization__c": False,
        "Trainer__c.Active__c": False,
        "Session__c.Trainer__c": True,
        "Session__c.Duration_Minutes__c": True,
        "Feedback__c.Case__c": True,
        "Feedback__c.Comments__c": True,
    }
    permissions("FitCorp_Sales_Rep", "FitCorp Sales Rep", {**obj_read, "Membership__c": "cre", "Trainer_Assignment__c": "cre", "Opportunity": "cre"}, sales_fields, custom_tabs)
    permissions("FitCorp_Support_Agent", "FitCorp Support Agent", {**obj_read, "Session__c": "cre", "Feedback__c": "cre", "Case": "cre"}, support_fields, custom_tabs)
    manager_fields = {
        "Opportunity.Discount__c": True,
        "Opportunity.Discount_Approval_Status__c": True,
        "Membership__c.Monthly_Fee__c": True,
        "Membership__c.Benefits__c": True,
        "Membership__c.Total_Sessions__c": False,
        "Membership__c.Days_Remaining__c": False,
        "Trainer__c.Specialization__c": True,
        "Trainer__c.Active__c": True,
        "Trainer__c.Hourly_Rate__c": True,
        "Session__c.Trainer__c": True,
        "Session__c.Duration_Minutes__c": True,
        "Feedback__c.Case__c": True,
        "Feedback__c.Comments__c": True,
        "Trainer_Assignment__c.Assigned_On__c": True,
        "Trainer_Assignment__c.Active__c": True,
    }
    permissions("FitCorp_Manager", "FitCorp Manager", {obj: "cre" for obj in custom_tabs} | {"Opportunity": "cre", "Case": "cre"}, manager_fields, custom_tabs)


if __name__ == "__main__":
    main()
