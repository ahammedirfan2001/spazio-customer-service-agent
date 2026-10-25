# Spazio Restaurant AI Customer Service Agent

An AI-powered customer service chatbot for Spazio Restaurant, built using Python, Flask, SQLite, HTML, CSS, JavaScript, and the Gemini API.

The chatbot helps customers find restaurant information, check menu prices, calculate order totals, and obtain contact details for human assistance.

## Features

- **Restaurant information:** Answers questions about opening hours, location, delivery, payment methods, vegetarian options, reservations, and allergen information.
- **Menu lookup:** Searches the restaurant's menu and returns matching items and their recorded prices.
- **Price calculation:** Calculates the total price for a specified quantity of a menu item.
- **Human assistance:** Provides the restaurant's contact number when customers need personal assistance.
- **SQLite database:** Stores restaurant information and menu records.
- **Interactive web interface:** Provides a chat interface built with HTML, CSS, and JavaScript.
- **Grounded responses:** Uses database tools to answer restaurant-specific questions and avoids inventing unverified prices or information.

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- OpenAI-compatible Python client
- Gemini API
- python-dotenv

## Project Structure

```text
spazio-customer-service-agent/
├── app.py
├── agent.py
├── tools.py
├── database.py
├── requirements.txt
├── .env.example
├── .gitignore
├── data/
│   ├── restaurant_info.csv
│   └── menu.csv
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

The SQLite database is created locally and is not included in the repository. The virtual environment and actual `.env` file are also excluded.

## Database

The project uses SQLite with two tables:

### 1. restaurant_info

Stores information about the restaurant, including:
- Opening hours
- Location
- Delivery
- Reservations
- Payment methods
- Vegetarian options
- Contact information
- Allergen information

### 2. menu

Stores menu records containing:
- Item ID
- Item name
- Category
- Price
- Availability status recorded in the source data

The menu database reflects the supplied menu data. It does not provide live kitchen stock information. Items with unconfirmed prices are not treated as free, and catering items are excluded from customer-facing menu searches.

## Tools

The agent has four tools:

1. **lookup_restaurant_info:** Retrieves restaurant information from the SQLite database.
2. **lookup_menu_item:** Searches regular menu items and returns matching records