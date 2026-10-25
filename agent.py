import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from tools import (
    lookup_restaurant_info,
    lookup_menu_item,
    calculate_item_total,
    handover_to_human
)

# Load API settings from .env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("LLM_API_URL")
)

MODEL_NAME = os.getenv("MODEL_NAME")


# Define the four tools available to the AI agent
restaurant_tools = [
    {
        "type": "function",
        "function": {
            "name": "lookup_restaurant_info",
            
            "description": (
                "Use this tool for questions about restaurant opening hours, "
                "location, delivery, table reservations, payment methods, "
                "vegetarian dishes and food options, contact details, "
                "and allergen information. Always use this tool when a customer "
                "asks what vegetarian options or dishes the restaurant offers. "
                "For specific menu item names and prices, use lookup_menu_item."
                "Always use this tool for general questions about vegetarian "
                "food options. Use lookup_menu_item for specific dishes and prices."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": (
                            "Information topic, such as opening_hours, "
                            "location, delivery, or payment_methods."
                        )
                    }
                },
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_menu_item",
            "description": (
                "Search the restaurant menu for matching items, "
                "including their categories, prices, and availability status."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "The menu item name or search term."
                    }
                },
                "required": ["item_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_item_total",
            "description": (
                "Calculate the total price for a specified quantity "
                "of one menu item."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "The specific menu item name."
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "The number of units requested."
                    }
                },
                "required": ["item_name", "quantity"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "handover_to_human",
            "description": (
                "Direct customers to human assistance when they request "
                "a manager, need a human representative, or have a complaint."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {
                        "type": "string",
                        "description": "Why the customer needs human assistance."
                    }
                },
                "required": ["reason"]
            }
        }
    }
]


# Execute the selected tool
def execute_tool(tool_name, arguments):

    if tool_name == "lookup_restaurant_info":
        return lookup_restaurant_info(arguments["topic"])

    elif tool_name == "lookup_menu_item":
        return lookup_menu_item(arguments["item_name"])

    elif tool_name == "calculate_item_total":
        return calculate_item_total(
            arguments["item_name"],
            arguments["quantity"]
        )

    elif tool_name == "handover_to_human":
        return handover_to_human(arguments["reason"])

    return {"error": "Unknown tool requested."}


# Communicate with the AI and handle tool calls
def chat_with_agent(user_message):

    messages = [
        {
            "role": "system",
            "content": (
                "You are the customer service assistant for Spazio Restaurant. "
                "Answer politely and clearly. Use the provided tools to retrieve "
                "restaurant information, menu details, and prices. Never invent "
                "restaurant facts or prices. Use tool results to answer "
                "restaurant-specific questions. If information cannot be "
                "verified, say so. Use the human handover tool when a customer needs human assistance. "
                "The handover tool does not directly connect the customer to a human. "
                "When the tool returns contact details, clearly provide the restaurant's "
                "phone number and explain that the customer should contact the restaurant "
                "directly. Never claim that a human has been contacted or that a transfer "
                "has occurred unless the tool explicitly confirms it. "
                "Do not claim a tool succeeded unless you received its result. "

                " MENU AVAILABILITY RULES: "
                "The database represents the restaurant menu, not live kitchen stock. "
                "Never claim a dish is currently in stock based only on the database's available field. "
                "You may share confirmed menu prices returned by the tools. "
                "If a price is unconfirmed, never guess it or describe the item as free. "
                "If a customer asks whether an item is currently available, explain that they must confirm with the restaurant. "
                "For menu or price questions, use the relevant tool instead of guessing. "

                "VEGETARIAN QUESTION ROUTING: "
                "If a customer asks generally whether vegetarian food is offered or what "
                "general vegetarian options are available, first use lookup_restaurant_info "
                "with the topic 'vegetarian_options'. Include all relevant vegetarian options "
                "mentioned in the returned tool result. Do not omit options that are present "
                "in the result. Explain that the availability of specific dishes should be "
                "confirmed with the restaurant. Use lookup_menu_item when the customer asks "
                "for specific menu item names or prices, or a list of vegetarian dishes with "
                "their prices. Do not claim that vegetarian information is missing if the "
                "restaurant information tool returns it. "  

                "OUT-OF-SCOPE QUESTIONS: "
                "Only answer questions related to Spazio Restaurant, its menu, "
                "prices, location, opening hours, delivery, payments, and services. "
                "If a question is unrelated to Spazio Restaurant, politely explain "
                "that you can only assist with restaurant-related questions. "
                "Do not answer the unrelated question, even if you know the answer. "
                "UNKNOWN RESTAURANT INFORMATION: "
                "If a customer asks about a restaurant feature or service that is not "
                "covered by the database or tool results, do not guess. Clearly explain "
                "that the information is not available. Suggest contacting the restaurant "
                "at +91 9539988634 to confirm it. Do not offer to connect the customer "
                "to a human unless a tool explicitly confirms that a connection is possible. "

            )
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    # Continue until the AI returns a final answer
    while True:

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=restaurant_tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # Save the AI's response, including any requested tool calls
        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        # If no tools were requested, return the final answer
        if not assistant_message.tool_calls:
            return (
                assistant_message.content
                or "Sorry, I couldn't generate a response."
            )

        # Execute each requested tool
        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name
            print(f"TOOL SELECTED: {tool_name}")
            arguments = json.loads(tool_call.function.arguments)

            tool_result = execute_tool(tool_name, arguments)

            # Send the tool result back to the AI
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    tool_result,
                    ensure_ascii=False
                )
            })