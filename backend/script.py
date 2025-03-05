from google import genai

client = genai.Client(api_key="AIzaSyCPD6QldeSLruUWN_sEJ4WjetG843Nw2a8")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works"
)
print(response.text)