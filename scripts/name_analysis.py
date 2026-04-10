import requests

name = input("Voer een naam in: ")

try:
    age_response = requests.get("https://api.agify.io", params={"name": name})
    gender_response = requests.get("https://api.genderize.io", params={"name": name})

    age = age_response.json()["age"]
    gender = gender_response.json()["gender"]

    print("\nName:", name)
    print("Predicted age:", age)
    print("Predicted gender:", gender)

except:
    print("Er ging iets mis.")

input("\nDruk op Een toets om af te sluiten...")
