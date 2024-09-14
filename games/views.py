# import csv

# def extract_csv_to_array(file_path):
#     data_array = []

#     with open(file_path, newline='', encoding='utf-8') as csvfile:
#         csvreader = csv.reader(csvfile)

#         # Skip the header row if needed (optional)
#         next(csvreader)

#         # Iterate over each row and append it to the array
#         for row in csvreader:
#             data_array.append(row)

#     return data_array

# # Paths for two different CSV files
# file1_path = 'expensive.csv'
# file2_path = 'affordable.csv'

# # Extract data from each file and store in separate arrays
# data_array1 = extract_csv_to_array(file1_path)
# data_array2 = extract_csv_to_array(file2_path)

# import random

# def get_random_data(data_array1, data_array2):
#     # Ensure both arrays have the same length
#     if len(data_array1) != len(data_array2):
#         raise ValueError("Both arrays must have the same length")

#     # Generate a random index within the bounds of the arrays
#     random_index = random.randint(0, len(data_array1) - 1)

#     # Get the data at that index from both arrays
#     data_from_array1 = data_array1[random_index]
#     data_from_array2 = data_array2[random_index]
    
#     rn=random.randint(0,7)
#     if 0<=rn<=3:
#         return random_index, data_from_array1, data_from_array2
#     else:
#         return random_index, data_from_array2, data_from_array1

# def compare_prices(data1, data2):
#     user_choice = int(input("Choose the more expensive item (enter '1' or '2'): "))
    
#     # Assuming the price is the second item in each data array (index 1)
#     price1 = float(data1[8].replace('₹', '').replace(',', '').replace('Rs','').replace('rs',''))  # Remove any rupee sign or comma and convert to float
#     price2 = float(data2[8].replace('₹', '').replace(',', '').replace('Rs','').replace('rs',''))

#     check=0
#     if price1>price2:
#         check=1
#     else:
#         check=2
        
#     if user_choice==check:
#         print("You are correct!!Go to next level")
#     else:
#         print("YOu lost a life!!") 
        
 
#     if price1 > price2:
#         print(f"The item from Array 1 is more expensive:{data1[0]} with price ₹{price1}")
#     elif price2 > price1:
#         print(f"The item from Array 2 is more expensive:{data2[0]} with price ₹{price2}")
#     else:
#         print("Both items have the same price.")


# # Generate random index and fetch data
# index, data1, data2 = get_random_data(data_array1, data_array2)

# # Compare the prices
# compare_prices(data1, data2)


import csv
import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Helper function to extract data from CSV
def extract_csv_to_array(file_path):
    data_array = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        # Skip the header row (optional)
        next(csvreader)
        for row in csvreader:
            data_array.append(row)

    return data_array

# API to get random items from the CSV files and compare prices
@api_view(['POST'])
def compare_items(request):
    # Paths for two different CSV files
    file1_path = 'expensive.csv'
    file2_path = 'affordable.csv'

    # Extract data from CSVs
    data_array1 = extract_csv_to_array(file1_path)
    data_array2 = extract_csv_to_array(file2_path)

    # Ensure both arrays have the same length
    if len(data_array1) != len(data_array2):
        return Response({"error": "Arrays have different lengths"}, status=status.HTTP_400_BAD_REQUEST)

    # Generate a random index and fetch items
    random_index = random.randint(0, len(data_array1) - 1)
    rn = random.randint(0, 7)
    
    if 0 <= rn <= 3:
        data1, data2 = data_array1[random_index], data_array2[random_index]
    else:
        data1, data2 = data_array2[random_index], data_array1[random_index]

    # Assume prices are in column 8 (index 7) of each row
    try:
        price1 = float(data1[8].replace('₹', '').replace(',', '').replace('Rs', '').replace('rs', ''))
        price2 = float(data2[8].replace('₹', '').replace(',', '').replace('Rs', '').replace('rs', ''))
    except (ValueError, IndexError):
        return Response({"error": "Invalid price data in the CSV files"}, status=status.HTTP_400_BAD_REQUEST)

    # Get the user's choice from the request data (expects 1 or 2)
    user_choice = request.data.get('choice', None)
    if user_choice not in [1, 2]:
        return Response({"error": "Invalid choice. Please choose 1 or 2"}, status=status.HTTP_400_BAD_REQUEST)

    # Determine which item is more expensive
    correct_choice = 1 if price1 > price2 else 2

    # Compare the user's choice
    if user_choice == correct_choice:
        return Response({
            "message": "Correct! You can proceed to the next level.",
            "item1": {"name": data1[7], "price": f"₹{price1}", "picture":data1[1], "category":data1[3] ,"link":data1[9], "brand":data1[6]},
            "item2": {"name": data2[7], "price": f"₹{price2}", "picture":data2[1], "category":data2[3] ,"link":data2[9], "brand":data2[6]}
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "message": "Incorrect! You lost a life.",
            "item1": {"name": data1[7], "price": f"₹{price1}", "picture":data1[1], "category":data1[3] ,"link":data1[9], "brand":data1[6]},
            "item2": {"name": data2[7], "price": f"₹{price2}", "picture":data2[1], "category":data2[3] ,"link":data2[9], "brand":data2[6]}
        }, status=status.HTTP_200_OK)
