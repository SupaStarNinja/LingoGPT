from google import genai

api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

user_question = input("Please enter your question: ")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents=user_question
)
print(response.text)