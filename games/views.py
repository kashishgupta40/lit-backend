import csv
import random
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import LeaderboardSerializer,SavedItemSerializer,UserGameDataSerializer
from .models import UserGameData,SavedItem
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import FriendList, FriendRequest
from django.urls import reverse
from django.http import HttpResponse

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
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def compare_items(request):
    
    # Fetch the user's game data, or create a new entry if it doesn't exist
    user_game_data, created = UserGameData.objects.get_or_create(custom_user=request.user)
    
    # Reset lives if 20 minutes have passed since lives reached zero
    if user_game_data.lives <= 0 and user_game_data.lives_reset_time:
        time_since_reset = datetime.now() - user_game_data.lives_reset_time
        if time_since_reset > timedelta(minutes=20):
            user_game_data.lives = 5  # Reset lives to 5
            user_game_data.lives_reset_time = None  # Clear the reset time
            user_game_data.save()
    
    # Check and handle the streak
    today = datetime.now().date()
    last_played = user_game_data.last_played
    streak = user_game_data.streak

    if last_played:
        if last_played == today:
            pass  # Already played today, no update needed
        elif last_played == today - timedelta(days=1):
            streak += 1  # Played yesterday, increment streak
        else:
            streak = 1  # Missed a day, reset streak
    else:
        streak = 1  # First-time play, start streak

    # Update user game data
    user_game_data.streak = streak
    user_game_data.last_played = today
    user_game_data.save()

    
    selected_gender=request.data.get('gender',None)
    selected_category = request.data.get('category', None)
    
    valid_genders = ['male', 'female', 'unisex']
    valid_categories = ['footwear', 'clothing', 'bags', 'accessories']
    
    if selected_gender not in valid_genders:
        return Response({"error": "Invalid gender selection. Please choose 'male', 'female', or 'unisex'."}, status=status.HTTP_400_BAD_REQUEST)
    if selected_category not in valid_categories:
        return Response({"error": "Invalid category selection. Please choose one of the following: 'footwear', 'clothing', 'bags', 'accessories'."}, status=status.HTTP_400_BAD_REQUEST)
        
    # Paths for two different CSV files
    file1_path = 'expensive.csv'
    file2_path = 'affordable.csv'

    # Extract data from CSVs
    data_array1 = extract_csv_to_array(file1_path)
    data_array2 = extract_csv_to_array(file2_path)

    # Filter the data based on the selected gender directly inside this function
    filtered_data1 = []
    filtered_data2 = []
    
    for row in data_array1:
        gender = row[5].lower()  
        category = row[3].lower() 
        if (gender == selected_gender.lower() or gender == "unisex") and category == selected_category.lower():
            filtered_data1.append(row)

    for row in data_array2:
        gender = row[5].lower()
        category = row[3].lower()
        if (gender == selected_gender.lower() or gender == "unisex") and category == selected_category.lower():
            filtered_data2.append(row)

    # Ensure both filtered arrays have the same length
    if len(filtered_data1) != len(filtered_data2) or len(filtered_data1) == 0:
        return Response({"error": "No matching items found for the selected gender and category or unequal data length"}, status=status.HTTP_400_BAD_REQUEST)
    

   # Count the number of items in each category
    category_counts = {
        'footwear': sum(1 for row in data_array1 if row[3].lower() == 'footwear'),
        'clothing': sum(1 for row in data_array1 if row[3].lower() == 'clothing'),
        'bags': sum(1 for row in data_array1 if row[3].lower() == 'bags'),
        'accessories': sum(1 for row in data_array1 if row[3].lower() == 'accessories'),
    }

    # Generate a random index and fetch items
    random_index = random.randint(0, len(data_array1) - 1)
    rn = random.randint(0, 7)
    
    if 0 <= rn <= 3:
        data1, data2 = filtered_data1[random_index], filtered_data2[random_index]
    else:
        data1, data2 = filtered_data2[random_index], filtered_data1[random_index]

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

    # Increment total games played
    user_game_data.total_games_played += 1
    
    # Determine which item is more expensive
    correct_choice = 1 if price1 > price2 else 2

    # Compare the user's choice
    if user_choice == correct_choice:
        # Correct choice: increase the user's score by 10
        user_game_data.score += 5
        user_game_data.total_games_won += 1
        user_game_data.levels_completed += 1  # Increment the level for a correct answer
        # Increment the category-specific level count
        if selected_category == 'footwear':
            user_game_data.footwear_levels += 1
        elif selected_category == 'clothing':
            user_game_data.clothing_levels += 1
        elif selected_category == 'bags':
            user_game_data.bags_levels += 1
        elif selected_category == 'accessories':
            user_game_data.accessories_levels += 1
        elif selected_category == 'watch':
            user_game_data.watch_levels += 1
            
        user_game_data.save()
        serializer = UserGameDataSerializer(user_game_data)
        
        return Response({
            "message": "Correct! You can proceed to the next level.",
            "lives_remaining": user_game_data.lives,
            "streak": user_game_data.streak,
            "score": user_game_data.score,
            "rank": user_game_data.rank,  
            "levels_completed": user_game_data.levels_completed,
            "levels_per_category": {
                "footwear": user_game_data.footwear_levels,
                "clothing": user_game_data.clothing_levels,
                "bags": user_game_data.bags_levels,
                "accessories": user_game_data.accessories_levels,
                "watch": user_game_data.watch_levels
            },
            "category_item_counts": category_counts,  # Show the number of items in each category
            "item1": {"name": data1[7], "price": f"₹{price1}", "picture":data1[1], "category":data1[3] ,"link":data1[9], "brand":data1[6]},
            "item2": {"name": data2[7], "price": f"₹{price2}", "picture":data2[1], "category":data2[3] ,"link":data2[9], "brand":data2[6]}
        }, status=status.HTTP_200_OK)
    else:
        # Deduct a life for incorrect choice
        user_game_data.lives -= 1
        # Set the time when lives reach zero
        if user_game_data.lives == 0:
            user_game_data.lives_reset_time = datetime.now()
            
        # Calculate win percentage and update rank
        if user_game_data.total_games_played > 0:
            win_percentage = (user_game_data.total_games_won / user_game_data.total_games_played) * 100

            if win_percentage <= 50:
                user_game_data.rank = 'Beginner'
            elif 51 <= win_percentage <= 95:
                user_game_data.rank = 'Amateur'
            else:
                user_game_data.rank = 'Connoisseur'

        user_game_data.save()
        serializer = UserGameDataSerializer(user_game_data)

        if user_game_data.lives <= 0:
            return Response({
                "message": "Incorrect! You lost all your lives. Game over.",
                "lives_remaining": 0,
                "rank": user_game_data.rank,  # Include user's rank in the response
                "streak": user_game_data.streak,
                "score": user_game_data.score,  # Include score
                "levels_completed": user_game_data.levels_completed,
                "item1": {"name": data1[7], "price": f"₹{price1}", "picture": data1[1], "category": data1[3], "link": data1[9], "brand": data1[6]},
                "item2": {"name": data2[7], "price": f"₹{price2}", "picture": data2[1], "category": data2[3], "link": data2[9], "brand": data2[6]}
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Incorrect! You lost a life.",
                "lives_remaining": user_game_data.lives,
                "streak": user_game_data.streak,
                "rank": user_game_data.rank,  
                "score": user_game_data.score,
                "levels_completed": user_game_data.levels_completed,
                "levels_per_category": {
                    "footwear": user_game_data.footwear_levels,
                    "clothing": user_game_data.clothing_levels,
                    "bags": user_game_data.bags_levels,
                    "accessories": user_game_data.accessories_levels,
                    "watch": user_game_data.watch_levels
                },
                "category_item_counts": category_counts,
                "item1": {"name": data1[7], "price": f"₹{price1}", "picture":data1[1], "category":data1[3] ,"link":data1[9], "brand":data1[6]},
                "item2": {"name": data2[7], "price": f"₹{price2}", "picture":data2[1], "category":data2[3] ,"link":data2[9], "brand":data2[6]}
            }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leaderboard(request):
    
   top_players = UserGameData.objects.all().order_by('-total_games_won')[:20]  # Top 20 users
   serializer = LeaderboardSerializer(top_players, many=True)

   return Response({
        "leaderboard": serializer.data
                }, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_item(request):
    serializer = SavedItemSerializer(data=request.data)
    
    # Validate the input
    if serializer.is_valid():
        saved_item = serializer.save(user=request.user)
        return Response({"message": "Item saved to your store!", "item": SavedItemSerializer(saved_item).data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_saved_items(request):
    saved_items = SavedItem.objects.filter(user=request.user)
    
    # Use the serializer to return the saved items as JSON
    serializer = SavedItemSerializer(saved_items, many=True)
    return Response({"saved_items": serializer.data}, status=status.HTTP_200_OK)





def get_friend_list(request, username):
    user = get_object_or_404(User, username=username)
    friend_list = FriendList.objects.get(user=user)
    friends = friend_list.friends.all()
    friends_data = [{'username': friend.username} for friend in friends]
    return JsonResponse(friends_data, safe=False)

# Send a friend request
def send_friend_request(request, receiver_username):
    sender = request.user
    receiver = get_object_or_404(User, username=receiver_username)
    friend_request, created = FriendRequest.objects.get_or_create(sender=sender, receiver=receiver)
    
    if created:
        return JsonResponse({'status': 'Friend request sent'})
    else:
        return JsonResponse({'status': 'Friend request already sent'})

# Accept a friend request
def accept_friend_request(request, sender_username):
    receiver = request.user
    sender = get_object_or_404(User, username=sender_username)
    friend_request = get_object_or_404(FriendRequest, sender=sender, receiver=receiver)
    
    if friend_request.is_active:
        friend_request.accept()
        return JsonResponse({'status': 'Friend request accepted'})
    else:
        return JsonResponse({'status': 'Request is no longer active'})

# Decline a friend request
def decline_friend_request(request, sender_username):
    receiver = request.user
    sender = get_object_or_404(User, username=sender_username)
    friend_request = get_object_or_404(FriendRequest, sender=sender, receiver=receiver)

    if friend_request.is_active:
        friend_request.decline()
        return JsonResponse({'status': 'Friend request declined'})
    else:
        return JsonResponse({'status': 'Request is no longer active'})
    

    # Add a friend
@api_view(['POST'])
def add_friend(request):
    try:
        user = User.objects.get(id=request.data['user_id'])
        friend = User.objects.get(id=request.data['friend_id'])
        friend_list = FriendList.objects.get(user=user)
        friend_list.add_friend(friend)
        return Response({'message': 'Friend added successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Remove a friend
@api_view(['POST'])
def remove_friend(request):
    try:
        user = User.objects.get(id=request.data['user_id'])
        friend = User.objects.get(id=request.data['friend_id'])
        friend_list = FriendList.objects.get(user=user)
        friend_list.remove_friend(friend)
        return Response({'message': 'Friend removed successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# View all friends
@api_view(['GET'])
def view_friends(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        friend_list = FriendList.objects.get(user=user)
        friends = friend_list.friends.all()
        friends_data = [{'id': friend.id, 'username': friend.username} for friend in friends]
        return Response({'friends': friends_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Send friend request
@api_view(['POST'])
def send_friend_request(request):
    try:
        from_user = User.objects.get(id=request.data['from_user_id'])
        to_user = User.objects.get(id=request.data['to_user_id'])
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
        
        friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
        return Response({'message': 'Friend request sent successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Respond to friend request (accept or decline)
@api_view(['POST'])
def respond_to_friend_request(request):
    try:
        friend_request = FriendRequest.objects.get(id=request.data['request_id'])
        if request.data['response'] == 'accept':
            friend_request.accept()
            return Response({'message': 'Friend request accepted'}, status=status.HTTP_200_OK)
        elif request.data['response'] == 'decline':
            friend_request.decline()
            return Response({'message': 'Friend request declined'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid response'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)