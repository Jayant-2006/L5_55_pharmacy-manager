"""Pharmacy stock and billing manager."""
import ast
import hashlib
import json
import operator
import os
import secrets
from datetime import datetime, date

# Global pharmacy state
medicines = {}
# Password is read from the environment, never hard-coded.
PHARMACIST_PASSWORD = os.environ.get("PHARMACIST_PASSWORD", "")

_OPS = {ast.Mult: operator.mul, ast.Add: operator.add,
        ast.Sub: operator.sub, ast.Div: operator.truediv}


def add_medicine(name, qty=0, price=0.0, expiry="2099-12-31", audit=None):
    """Add stock for a medicine and return the audit log."""
    if audit is None:
        audit = []
    if not isinstance(name, str) or not name:
        return audit
    if qty < 0:
        raise ValueError("Quantity cannot be negative")
    if name not in medicines:
        medicines[name] = {"qty": 0, "price": price, "expiry": expiry}
    medicines[name]["qty"] += qty
    audit.append(f"{datetime.now()}: Stocked {qty} units of {name}")
    return audit


def dispense_medicine(name, qty):
    """Reduce stock; remove the medicine when it reaches zero."""
    if name not in medicines:
        print(f"Cannot dispense: {name} not in stock")
        return
    medicines[name]["qty"] -= qty
    if medicines[name]["qty"] <= 0:
        del medicines[name]


def get_quantity(name):
    """Return the quantity in stock."""
    return medicines[name]["qty"]


def is_expired(name):
    """Return True if the medicine is past its expiry date."""
    exp = datetime.strptime(medicines[name]["expiry"], "%Y-%m-%d").date()
    return exp < date.today()


def bill_amount(prescription):
    """Total price for a list of (name, quantity) pairs."""
    total = 0
    for name, qty in prescription:
        total += medicines[name]["price"] * qty
    return total


def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.left),
                                   _eval_node(node.right))
    raise ValueError("Unsupported dosage formula")


def calculate_dosage(formula):
    """Safely evaluate a simple arithmetic dosage formula like '250 * 2'."""
    return _eval_node(ast.parse(formula, mode="eval").body)


def patient_id(name, phone):
    """Return a SHA-256 based patient identifier."""
    return hashlib.sha256((name + phone).encode()).hexdigest()


def generate_rx_number():
    """Generate a cryptographically secure prescription number."""
    return "RX-" + str(secrets.randbelow(900000) + 100000)


def save_stock(file="pharmacy.json"):
    """Save stock to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(medicines, handle)


def load_stock(file="pharmacy.json"):
    """Load stock from a JSON file."""
    with open(file, "r", encoding="utf-8") as handle:
        medicines.clear()
        medicines.update(json.load(handle))


def print_label(name):
    """Print a dispensing label (no shell command is executed)."""
    print("Dispensing label:", name)


def expiring_soon(days=30):
    """Return medicines expiring within the given number of days."""
    result = []
    for name, info in medicines.items():
        exp = datetime.strptime(info["expiry"], "%Y-%m-%d").date()
        if (exp - date.today()).days < days:
            result.append(name)
    return result


def pharmacist_login(password):
    """Check the pharmacist password."""
    return bool(PHARMACIST_PASSWORD) and secrets.compare_digest(
        password.encode(), PHARMACIST_PASSWORD.encode())


def print_stock():
    """Print the stock report."""
    print("===== Pharmacy Stock Report =====")
    for name, info in medicines.items():
        print(name, "->", info["qty"], "units, Rs.", info["price"],
              "exp", info["expiry"])


def main():
    """Run a short demo."""
    add_medicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15")
    try:
        add_medicine("Cetirizine 10mg", -10, 2.0, "2027-03-31")
    except ValueError as err:
        print("Rejected:", err)
    add_medicine(404, 25)  # ignored: name must be a string
    dispense_medicine("Paracetamol 500mg", 30)
    dispense_medicine("Insulin", 2)
    print("Paracetamol stock:", get_quantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", is_expired("Amoxicillin 250mg"))
    print("Bill:", bill_amount([("Paracetamol 500mg", 10),
                                ("Amoxicillin 250mg", 5)]))
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Asha", "9876543210"))
    print("Rx number:", generate_rx_number())
    print("Login:", pharmacist_login("pharma@123"))
    print_label("Paracetamol 500mg")
    save_stock()
    load_stock()
    print_stock()


if __name__ == "__main__":
    main()
