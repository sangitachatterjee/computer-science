# Restaurant Menu & Order Management System
import copy
import pprint

menu = {
    "Paneer Tikka":   {"category": "Starters",  "price": 180.0, "available": True},
    "Chicken Wings":  {"category": "Starters",  "price": 220.0, "available": False},
    "Veg Soup":       {"category": "Starters",  "price": 120.0, "available": True},
    "Butter Chicken": {"category": "Mains",     "price": 320.0, "available": True},
    "Dal Tadka":      {"category": "Mains",     "price": 180.0, "available": True},
    "Veg Biryani":    {"category": "Mains",     "price": 250.0, "available": True},
    "Garlic Naan":    {"category": "Mains",     "price":  40.0, "available": True},
    "Gulab Jamun":    {"category": "Desserts",  "price":  90.0, "available": True},
    "Rasgulla":       {"category": "Desserts",  "price":  80.0, "available": True},
    "Ice Cream":      {"category": "Desserts",  "price": 110.0, "available": False},
}

inventory = {
    "Paneer Tikka":   {"stock": 10, "reorder_level": 3},
    "Chicken Wings":  {"stock":  8, "reorder_level": 2},
    "Veg Soup":       {"stock": 15, "reorder_level": 5},
    "Butter Chicken": {"stock": 12, "reorder_level": 4},
    "Dal Tadka":      {"stock": 20, "reorder_level": 5},
    "Veg Biryani":    {"stock":  6, "reorder_level": 3},
    "Garlic Naan":    {"stock": 30, "reorder_level": 10},
    "Gulab Jamun":    {"stock":  5, "reorder_level": 2},
    "Rasgulla":       {"stock":  4, "reorder_level": 3},
    "Ice Cream":      {"stock":  7, "reorder_level": 4},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1,  "items": ["Paneer Tikka", "Garlic Naan"],          "total": 220.0},
        {"order_id": 2,  "items": ["Gulab Jamun", "Veg Soup"],              "total": 210.0},
        {"order_id": 3,  "items": ["Butter Chicken", "Garlic Naan"],        "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4,  "items": ["Dal Tadka", "Garlic Naan"],             "total": 220.0},
        {"order_id": 5,  "items": ["Veg Biryani", "Gulab Jamun"],           "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6,  "items": ["Paneer Tikka", "Rasgulla"],             "total": 260.0},
        {"order_id": 7,  "items": ["Butter Chicken", "Veg Biryani"],        "total": 570.0},
        {"order_id": 8,  "items": ["Garlic Naan", "Gulab Jamun"],           "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9,  "items": ["Dal Tadka", "Garlic Naan", "Rasgulla"], "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"],          "total": 270.0},
    ],
}

# Task 1 — Explore the Menu (5 marks)
print("Task 1 — Explore the Menu (5 marks)\n")

categories = ["Starters", "Mains", "Desserts"]

for category in categories:
    print(f"===== {category} =====")
    for dish_name, details in menu.items():
        if details["category"] != category:
            continue
        status = "Available" if details["available"] else "Unavailable"
        price = details["price"]
        print(f"{dish_name:<16} ₹{price:.2f}   [{status}]")
    print()

total_items = len(menu)
available_count = sum(1 for info in menu.values() if info["available"])
most_expensive_name, most_expensive_info = max(menu.items(), key=lambda item: item[1]["price"])
under_150 = [(name, info["price"]) for name, info in menu.items() if info["price"] < 150.0]

print("--- Menu statistics (using dictionary methods) ---")
print(f"Total number of items on the menu: {total_items}")
print(f"Total number of available items: {available_count}")
print(
    f"The most expensive item: {most_expensive_name} — ₹{most_expensive_info['price']:.2f}"
)
print("Items priced under ₹150:")
for name, price in under_150:
    print(f"  {name} — ₹{price:.2f}")


# Task 2 — Cart Operations (8 marks)
print("\n\nTask 2 — Cart Operations (8 marks)\n")

cart = []


def print_cart_state(label):
    print(f"--- Cart after: {label} ---")
    if not cart:
        print("  (empty)")
    else:
        for entry in cart:
            print(
                f"  {entry['item']}: qty {entry['quantity']} @ ₹{entry['price']:.2f}/unit"
            )
    print()


def add_to_cart(cart, item_name, quantity):
    if item_name not in menu:
        print(f'"{item_name}" is not on the menu — not added.\n')
        return
    if not menu[item_name]["available"]:
        print(f'"{item_name}" is unavailable — not added.\n')
        return
    unit_price = menu[item_name]["price"]
    for entry in cart:
        if entry["item"] == item_name:
            entry["quantity"] += quantity
            entry["price"] = unit_price
            return
    cart.append({"item": item_name, "quantity": quantity, "price": unit_price})


def remove_from_cart(cart, item_name):
    for i, entry in enumerate(cart):
        if entry["item"] == item_name:
            cart.pop(i)
            return
    print(f'"{item_name}" is not in the cart.\n')


def update_cart_quantity(cart, item_name, new_quantity):
    if new_quantity < 0:
        print("Quantity cannot be negative.\n")
        return
    for i, entry in enumerate(cart):
        if entry["item"] == item_name:
            if new_quantity == 0:
                cart.pop(i)
            else:
                entry["quantity"] = new_quantity
                entry["price"] = menu[item_name]["price"]
            return
    print(f'"{item_name}" is not in the cart.\n')


def print_order_summary(cart):
    print("========== Order Summary ==========")
    subtotal = 0.0
    for entry in cart:
        line_total = entry["quantity"] * entry["price"]
        subtotal += line_total
        print(f"{entry['item']:<18} x{entry['quantity']}    ₹{line_total:.2f}")
    gst = round(subtotal * 0.05, 2)
    total = round(subtotal + gst, 2)
    print("------------------------------------")
    print(f"{'Subtotal:':<24}₹{subtotal:.2f}")
    print(f"{'GST (5%):':<24}₹{gst:>6.2f}")
    print(f"{'Total Payable:':<24}₹{total:.2f}")
    print("====================================")


add_to_cart(cart, "Paneer Tikka", 2)
print_cart_state('Add "Paneer Tikka" × 2')

add_to_cart(cart, "Gulab Jamun", 1)
print_cart_state('Add "Gulab Jamun" × 1')

add_to_cart(cart, "Paneer Tikka", 1)
print_cart_state('Add "Paneer Tikka" × 1 (merge with existing line)')

add_to_cart(cart, "Mystery Burger", 1)
print_cart_state('Try to add "Mystery Burger"')

add_to_cart(cart, "Chicken Wings", 1)
print_cart_state('Try to add "Chicken Wings"')

remove_from_cart(cart, "Gulab Jamun")
print_cart_state('Remove "Gulab Jamun"')

print_order_summary(cart)


# Task 3 — Inventory Tracker with Deep Copy (6 marks)
print("\n\nTask 3 — Inventory Tracker with Deep Copy (6 marks)\n")

print(
    "Deep copy: a new top-level dict AND new inner dicts for each dish, so changing "
    "inventory['Veg Soup']['stock'] cannot alter inventory_backup. "
    "(A shallow copy would reuse the same inner dict objects — both would change.)\n"
)

inventory_backup = copy.deepcopy(inventory)

print("--- Proof: nested records are different objects (not shared references) ---")
print(f"  inventory is inventory_backup → {inventory is inventory_backup}  (expected: False)")
print(
    "  inventory['Veg Soup'] is inventory_backup['Veg Soup'] → "
    f"{inventory['Veg Soup'] is inventory_backup['Veg Soup']}  (expected: False)\n"
)

print("--- Mutate only `inventory`: set Veg Soup stock to 1 ---")
before_backup_soup = inventory_backup["Veg Soup"]["stock"]
inventory["Veg Soup"]["stock"] = 1
print(
    f"  Veg Soup stock in inventory:     {inventory['Veg Soup']['stock']}  (changed)\n"
    f"  Veg Soup stock in inventory_backup: {before_backup_soup}  (unchanged — deep copy isolated nested data)\n"
)
print("Full inventory (after change):")
pprint.pprint(inventory)
print("\nFull inventory_backup (still original data):")
pprint.pprint(inventory_backup)

print("\n--- Restore inventory from backup before fulfilment ---")
inventory = copy.deepcopy(inventory_backup)
print(
    f"  After restore, Veg Soup stock in inventory: {inventory['Veg Soup']['stock']} "
    f"(matches backup again)\n"
)

print("\n--- Fulfil order (deduct Task 2 cart from inventory) ---")
for line in cart:
    name = line["item"]
    need = line["quantity"]
    have = inventory[name]["stock"]
    if have < need:
        print(
            f"Warning: insufficient stock for {name}. "
            f"Requested {need}, only {have} available — deducting {have}."
        )
        inventory[name]["stock"] = 0
    else:
        inventory[name]["stock"] = have - need

print("\n--- Reorder alerts (stock at or below reorder_level) ---")
for dish_name, inv in inventory.items():
    if inv["stock"] <= inv["reorder_level"]:
        print(
            f"⚠ Reorder Alert: {dish_name} — Only {inv['stock']} unit(s) left "
            f"(reorder level: {inv['reorder_level']})"
        )

print("\n--- inventory (after fulfilment) vs inventory_backup (original snapshot) ---")
print(
    "Fulfilment only changed `inventory`. `inventory_backup` stayed the pre-fulfilment "
    "snapshot, so you can compare or roll back.\n"
)
print("Explicit contrast (Paneer Tikka, only item in final cart):")
print(
    f"  inventory['Paneer Tikka']['stock']:         {inventory['Paneer Tikka']['stock']}\n"
    f"  inventory_backup['Paneer Tikka']['stock']:  {inventory_backup['Paneer Tikka']['stock']}\n"
)
print("inventory (live):")
pprint.pprint(inventory)
print("\ninventory_backup (unchanged snapshot):")
pprint.pprint(inventory_backup)


# Task 4 — Daily Sales Log Analysis (6 marks)
print("\n\nTask 4 — Daily Sales Log Analysis (6 marks)\n")


def revenue_by_day(log):
    return {day: sum(order["total"] for order in orders) for day, orders in log.items()}


def print_revenue_per_day(log, title):
    print(title)
    rev = revenue_by_day(log)
    for day in sorted(rev.keys()):
        print(f"  {day}: ₹{rev[day]:.2f}")
    print()


def best_selling_day(log):
    rev = revenue_by_day(log)
    best_date = max(rev, key=lambda d: rev[d])
    return best_date, rev[best_date]


def most_ordered_item_by_order_count(log):
    counts = {}
    for orders in log.values():
        for order in orders:
            seen_in_order = set(order["items"])
            for item in seen_in_order:
                counts[item] = counts.get(item, 0) + 1
    if not counts:
        return None, 0
    top_item = max(counts, key=lambda k: counts[k])
    return top_item, counts[top_item]


print_revenue_per_day(sales_log, "Total revenue per day (original log):")
best_date, best_rev = best_selling_day(sales_log)
print(f"Best-selling day: {best_date} (₹{best_rev:.2f} total)\n")

top_item, top_count = most_ordered_item_by_order_count(sales_log)
print(
    f"Most ordered item (appears in the most individual orders): "
    f"{top_item} — in {top_count} order(s)\n"
)

sales_log["2025-01-05"] = [
    {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
    {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"], "total": 260.0},
]

print("--- After adding 2025-01-05 ---\n")
print_revenue_per_day(sales_log, "Total revenue per day (updated log):")
best_date2, best_rev2 = best_selling_day(sales_log)
print(f"Best-selling day: {best_date2} (₹{best_rev2:.2f} total)\n")

flat_orders = []
for day in sorted(sales_log.keys()):
    for order in sales_log[day]:
        flat_orders.append((day, order))

print("All orders (numbered):")
for n, (day, order) in enumerate(flat_orders, start=1):
    items_joined = ", ".join(order["items"])
    print(
        f"{n}.  [{day}] Order #{order['order_id']}  "
        f"— ₹{order['total']:.2f} — Items: {items_joined}"
    )
