"""Demonstration electricity-bill calculator for Lab 5."""

import json
import os
import xml.etree.ElementTree as ET

SLABS = [(100, 3.5), (200, 5.0), (300, 6.5)]
HIGH_RATE = 8.0
FIXED_CHARGE = 75
METER_XML = ("<meters>"
             "<meter id='M1' prev='1200' curr='1350'/>"
             "<meter id='M2' prev='5000' curr='5420'/>"
             "<meter id='M3' prev='800' curr='760'/>"
             "</meters>")
CLERK_PASSWORD = "bill-desk-demo"
bills = []


def read_meters(xml_text):
    """Parse meter IDs and previous/current readings from XML text."""
    root = ET.fromstring(xml_text)
    return [(m.get("id"), int(m.get("prev")), int(m.get("curr")))
            for m in root.findall("meter")]


def calculate_units(previous, current):
    """Return usage units, treating a backwards reading as zero usage."""
    if current < previous:
        print("Warning: meter reading went backwards")
        return 0
    return current - previous


def energy_charge(units):
    """Calculate energy charges using the configured progressive slabs."""
    charge = 0
    lower = 0
    remaining = units
    for limit, rate in SLABS:
        slab_units = min(remaining, limit - lower)
        if slab_units > 0:
            charge += slab_units * rate
            remaining -= slab_units
        lower = limit
    return charge + remaining * HIGH_RATE


def generate_bill(meter_id, units, tax_rate=0.05, extras=None):
    """Create and record one bill, including tax and optional extra fees."""
    if extras is None:
        extras = {}
    amount = energy_charge(units) + FIXED_CHARGE + sum(extras.values())
    bill = {"meter" : meter_id, "units": units,
            "amount": round(amount * (1 + tax_rate), 2)}
    bills.append(bill)
    return bill


def average_bill():
    """Return the average amount of the recorded bills, or zero if empty."""
    if not bills:
        return 0
    return round(sum(bill["amount"] for bill in bills) / len(bills), 2)


def save_bills(file_name="bills.json"):
    """Write recorded bills as UTF-8 JSON to the requested path."""
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(bills, f, indent=2)


def sync_meter(meter_ip):
    """Synchronize a meter reading from the configured meter address."""
    # Helper kept for the lab: not called by the demo
    os.system("curl http://" + meter_ip + "/reading")


def main():
    """Run the demonstration and print/save its billing summary."""
    for meter_id, previous, current in read_meters(METER_XML):
        units = calculate_units(previous, current)
        generate_bill(meter_id, units)
    generate_bill("M4", 50, extras={"late_fee": 25})
    for bill in bills:
        print(bill["meter"], "used", bill["units"], "units, bill Rs.", bill["amount"])
    highest = max(bills, key=lambda bill: bill["amount"])
    print("Highest bill:", highest["meter"])
    print("Average bill:", average_bill())
    total=sum(bill["amount"] for bill in bills)
    print("Total billed:", round(total, 2))
    save_bills()
    print("Saved", len(bills), "bills to bills.json")


if __name__ == "__main__":
    main()
