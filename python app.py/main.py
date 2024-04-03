import requests
import json

def get_recipes_by_ingredient(ingredient):
    endpoint = "https://api.edamam.com/api/recipes/v2"
    app_id = "1dc7b1e0"
    app_key = "45b19b31992800e98bdd4c4b15d0d308"

    params = {
        "app_id": app_id,
        "app_key": app_key,
        "q": ingredient,
        "from": 0,
        "to": 20,
        "type": "public"}

    try:
        response = requests.get(endpoint, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code)
            return None
    except Exception as e:
        print("Exception:", e)
        return None

def display_recipes(recipes):
    if recipes:
        for idx, hit in enumerate(recipes["hits"], 1):
            print(f"Recipe {idx}: {hit['recipe']['label']}")
            print(f"  - URL: {hit['recipe']['url']}")
            print(f"  - Cuisine Type: {', '.join(hit['recipe']['cuisineType'])}")
            print(f"  - Dish Type: {', '.join(hit['recipe']['dishType'])}")
            print("\n")
    else:
        print("No recipes found.")

def save_to_file(recipes, filename):
    with open(filename, 'w') as file:
        json.dump(recipes, file, indent=4)

def main():
    ingredient = input("Enter an ingredient you want to search for: ")

    recipes = get_recipes_by_ingredient(ingredient)

    if recipes:
        filename = f"{ingredient}_recipes.json"
        save_to_file(recipes, filename)
        print(f"Recipes saved to '{filename}'.")

    display_recipes(recipes)

    recipe_choice = input("Enter the number of the recipe you want to choose: ")
    selected_recipe = recipes["hits"][int(recipe_choice)-1]["recipe"]

    nutrition_endpoint = "https://api.edamam.com/api/nutrition-data"
    nutrition_params = {
        "app_id": "55a55cbc",
        "app_key": "5df83a97d2ec863bf10f3aaac87f0c69",
        "ingr": selected_recipe["ingredientLines"]}

    nutrition_response = requests.get(nutrition_endpoint, params=nutrition_params)
    nutrition_data = nutrition_response.json()

    print("Nutrition Information:")
    if 'calories' in nutrition_data:
        print(f"  - Calories: {nutrition_data['calories']} kcal")
    else:
        print("  - Calories information not available.")

    if 'totalWeight' in nutrition_data:
        print(f"  - Total Weight: {nutrition_data['totalWeight']} grams")
    else:
        print("  - Total Weight information not available.")

    if 'totalNutrients' in nutrition_data:
        print("  - Total Nutrients:")
        for nutrient, data in nutrition_data['totalNutrients'].items():
            print(f"    - {nutrient}: {data['quantity']} {data['unit']}")
    else:
        print("  - Total Nutrients information not available.")

    if 'totalDaily' in nutrition_data:
        print("  - Total Daily:")
        for nutrient, data in nutrition_data['totalDaily'].items():
            print(f"    - {nutrient}: {data['quantity']} {data['unit']}")
    else:
        print("  - Total Daily information not available.")

    print(f"  - Calories: {nutrition_data['calories']}")
    print(f"  - Total Weight: {nutrition_data['totalWeight']} grams")
    print(f"  - Total Nutrients: {nutrition_data['totalNutrients']}")
    print(f"  - Total Daily: {nutrition_data['totalDaily']}")

if __name__ == "__main__":
    main()

