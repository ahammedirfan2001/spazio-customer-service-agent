
from agent import chat_with_agent

test_questions = [
    "What time does Spazio Restaurant open?",
    "Where is your restaurant located?",
    "Do you provide delivery?",
    "What is the price of Chicken Biriyani?",
    "What vegetarian options do you offer?",
    "How much do three Chicken Biriyanis cost?",
    "Can I reserve a table?",
    "Which payment methods do you accept?",
    "I want to complain to the restaurant manager.",
    "What is the price of Fish Curry?"
]

for number, question in enumerate(test_questions, start=1):
    print(f"\nTest {number}")
    print("Customer:", question)

    answer = chat_with_agent(question)

    print("AI Assistant:", answer)