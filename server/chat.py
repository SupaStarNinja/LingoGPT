from google import genai

client = genai.Client(api_key='AIzaSyAUHjaH0PsHO3vjR2h-dRaghilt2LVdpDE')

# Get user input for the question
user_question = input("Please enter your question: ")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=user_question
)
print(response.text)