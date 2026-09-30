"""Add the project fields to the org-created FitCorp page layouts."""

from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1] / "force-app/main/default/layouts"
NS = "http://soap.sforce.com/2006/04/metadata"
ET.register_namespace("", NS)

FIELDS = {
    "Membership__c-Membership Layout": [
        ("Monthly_Fee__c", "Edit"), ("Benefits__c", "Edit"),
        ("Total_Sessions__c", "Readonly"), ("Days_Remaining__c", "Readonly"),
    ],
    "Trainer__c-Trainer Layout": [
        ("Specialization__c", "Edit"), ("Active__c", "Edit"),
        ("Hourly_Rate__c", "Edit"),
    ],
    "Session__c-Session Layout": [
        ("Trainer__c", "Edit"), ("Duration_Minutes__c", "Edit"),
    ],
    "Feedback__c-Feedback Layout": [
        ("Case__c", "Edit"), ("Comments__c", "Edit"),
    ],
    "Trainer_Assignment__c-Trainer Assignment Layout": [
        ("Assigned_On__c", "Edit"), ("Active__c", "Edit"),
    ],
}


for layout_name, fields in FIELDS.items():
    path = ROOT / f"{layout_name}.layout-meta.xml"
    tree = ET.parse(path)
    root = tree.getroot()
    first_section = root.find(f"{{{NS}}}layoutSections")
    columns = first_section.findall(f"{{{NS}}}layoutColumns")
    present = {node.text for node in first_section.findall(f".//{{{NS}}}field")}
    for field, behavior in fields:
        if field in present:
            continue
        item = ET.SubElement(columns[1], f"{{{NS}}}layoutItems")
        ET.SubElement(item, f"{{{NS}}}behavior").text = behavior
        ET.SubElement(item, f"{{{NS}}}field").text = field
    ET.indent(root, space="    ")
    tree.write(path, encoding="utf-8", xml_declaration=True)
