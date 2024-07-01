import requests
import os
import random
from IPython.display import HTML

def get_high_protein_meals(num_meals):
    app_id = '033fa23e'  # Replace with your Edamam app ID
    app_key = '1e6005f2f6a4b46079f522fcf5c5da15'  # Replace with your Edamam app key
    url = f'https://api.edamam.com/search'
    from_index = random.randint(0, 100)  # Generate a random 'from' index
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'q': 'high protein',
        'from': from_index,
        'to': from_index + num_meals
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        meals = []

        for hit in data['hits']:
            meal = hit['recipe']
            label = meal['label']
            protein = meal['totalNutrients']['PROCNT']['quantity']
            description = meal['source'] + ' - ' + meal['healthLabels'][0]
            recipe_url = meal['url']
            image_url = meal['image']
            meals.append((label, protein, description, recipe_url, image_url))

        return meals
    else:
        print('Error occurred while retrieving high protein meals.')
        return None

def display_high_protein_meals(meals):
    if meals:
        print("High Protein Meals:")
        num = 1
        with open("misc.txt", 'w') as file:
            for meal in meals:
                label, protein, description, recipe_url, image_url = meal
                file.write(f"{label} - Protein: {protein}g\n")
                file.write(f"Description: {description}\n")
                file.write(f"Recipe URL: {recipe_url}\n")
                file.write("\n")
                download_image(image_url, label, num)
                num+=1
                print()
    else:
        print("No high protein meals found.")

def download_image(image_url, label, num):
    response = requests.get(image_url)

    if response.status_code == 200:
        filename = f"image{num}.jpg"
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Image downloaded for {label}")
    else:
        print(f"Error downloading image for {label}")

# Example usage
num_meals = 5  # Set the number of high protein meals to generate

high_protein_meals = get_high_protein_meals(num_meals)
display_high_protein_meals(high_protein_meals)
