from agent import chat_with_agent

question = "I want to speak to the restaurant manager about a complaint."

answer = chat_with_agent(question)

print("Customer:", question)
print("AI Assistant:", answer)