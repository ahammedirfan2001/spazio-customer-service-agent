# Spazio Restaurant Knowledge Base — Draft

This folder contains draft reference documents for the Spazio Restaurant AI assistant's RAG system.

## Files
- `restaurant_profile.md` — history, brand identity, values and vision.
- `outlets.md` — outlet details, contacts, hours, maps and social accounts.
- `ordering_and_delivery.md` — ordering channels, payments, delivery and tracking.
- `catering_and_bulk_orders.md` — catering, bulk orders, advance notice, payment and cancellation.
- `food_quality_and_safety.md` — sourcing, hygiene, allergies, halal sourcing and dietary information.
- `customer_service_policies.md` — reservations, family facilities, complaints, promotions and communication.
- `ai_assistant_rules.md` — assistant behavior and escalation rules.

## Draft status
These documents are based on information supplied by the restaurant owner during a documentation interview. Review and approve them before using them in a customer-facing system.

## Menu data
Keep exact menu items, portion sizes and prices in the existing SQLite menu database and its source CSV. These profile documents do not replace the structured menu database.

## Retrieval guidance
Use these Markdown files for long-form restaurant information and policies. Continue using structured database tools for exact menu lookups and price calculations.

## Facts that must not be overclaimed
- Spazio sources meat from halal suppliers but has no formal halal certification.
- Some vegetarian and non-vegetarian kitchen facilities are shared.
- Spazio does not maintain a complete allergen list.
- Menu availability changes and must be confirmed with the outlet.
- Delivery coverage is generally around 5 km but can vary.
- Delivery fees and delivery times are not fixed.
- An order is not confirmed until staff check availability and confirm it.
