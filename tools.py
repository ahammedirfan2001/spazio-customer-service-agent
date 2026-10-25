from database import get_connection


def lookup_restaurant_info(topic):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT details FROM restaurant_info WHERE topic = ?",
        (topic,)
    )

    result = cursor.fetchone()
    connection.close()

    if result:
        return result[0]

    return "Sorry, I couldn't find that information."



def lookup_menu_item(item_name):
    connection = get_connection()
    cursor = connection.cursor()

    # Search only the regular menu, excluding catering.
    cursor.execute(
        """
        SELECT item_name, category, price, available
        FROM menu
        WHERE UPPER(TRIM(category)) != 'CATERING'
        ORDER BY item_name
        """
    )

    rows = cursor.fetchall()
    connection.close()

    search_name = item_name.strip().casefold()

    # First, find exact matches.
    exact_matches = [
        row for row in rows
        if row[0].strip().casefold() == search_name
    ]

    # If no exact match exists, search for partial matches.
    if exact_matches:
        results = exact_matches
    else:
        results = [
            row for row in rows
            if search_name in row[0].strip().casefold()
        ]

    menu_items = []

    for row in results:
        price = float(row[2])

        menu_items.append({
            "item_name": row[0],
            "category": row[1],
            "price": price if price > 0 else None,
            "price_status": (
                "confirmed" if price > 0 else "unconfirmed"
            ),
            "available": bool(row[3])
        })

    return menu_items


def calculate_item_total(item_name, quantity):
    if not isinstance(quantity, int) or isinstance(quantity, bool):
        return "Please provide a whole-number quantity."

    if quantity <= 0:
        return "Quantity must be greater than zero."

    results = lookup_menu_item(item_name)

    if not results:
        return "Sorry, I couldn't find that item on the regular menu."

    if len(results) > 1:
        return (
            "Multiple regular menu items matched your search. "
            "Please provide a more specific item name."
        )

    item = results[0]

    if item["price_status"] != "confirmed":
        return (
            f"The price of {item['item_name']} is unconfirmed. "
            "Please contact the restaurant for the current price."
        )

    total = item["price"] * quantity

    return {
        "item_name": item["item_name"],
        "quantity": quantity,
        "unit_price": item["price"],
        "total_price": round(total, 2),
        "currency": "INR"
    }



def handover_to_human(reason):
    return {
        "status": "contact_details_provided",
        "reason": reason,
        "message": (
            "I cannot directly connect you to a manager through this chat. "
            "Please contact Spazio Restaurant at +91 9539988634 "
            "for personal assistance with your complaint."
        )
    }
