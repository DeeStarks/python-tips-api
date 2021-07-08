from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from psycopg2.extensions import adapt
import requests
from bs4 import BeautifulSoup
import datetime
from python_tips_api.db_connection import database
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
@api_view(['GET'])
def fetch_tips(request):
    tip_keywords = ["need", "to", "sort", "a", "list", "by", "multiple", "criteria?", "use", "key", "lambda", "detail", "on"]


    data = {
        "status": True,
        "message": "Fetched successfully"
    }
    # Query database for all tips
    data["data"] = database.select_table('tips_pythontip')
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def fetch_tip(request, tip_id):
    data = {
        "status": True,
        "message": "Fetched successfully"
    }
    # Query database for a specific tip
    try:
        data["data"] = database.select_row(
            table_name='tips_pythontip',
            target_column='id',
            value=tip_id
        )
    except ObjectDoesNotExist:
        data["status"] = False
        data["message"] = "No such tip"
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_tip(request):
    # Check for valid fields
    valid_fields = ['tip', 'poster', 'poster_email', 'is_published']
    for i in request.data.keys():
        if i not in valid_fields:
            return Response(data={"status": False, "message": "Invalid field: {}. Valid fields are: 'tip', 'poster, 'poster_email', 'is_published'".format(i)}, status=status.HTTP_400_BAD_REQUEST)

    # Check for required fields
    required_fields = ['tip', 'poster']
    for i in required_fields:
        if i not in request.data.keys():
            return Response(data={"status": False, "message": "Missing field: {}".format(i)}, status=status.HTTP_400_BAD_REQUEST)

    # Check if length of tip is greater than 140 characters
    if len(request.data['tip']) > 140:
        return Response(data={"status": False, "message": "Tip length cannot exceed 140 characters"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if tip matches with other tips by 50% or more
    if len(request.data['tip'].split(" ")) > 1:
        tip_keywords = [keyword.lower() for keyword in request.data['tip'].split(" ")]
        existing_tips = [[keyword.replace("\n", " ").replace(">>>", " ").lower() for keyword in i['tip'].split(" ")] for i in database.select_table('tips_pythontip')]

        for tip in existing_tips:
            if len(set(tip_keywords) & set(tip)) > 0:
                matches = set(tip_keywords) & set(tip)
                if len(matches) > 1 and len(matches) > len(tip)/2:
                    return Response(data={"status": False, "message": "Tip too similar to one of existing tips"}, status=status.HTTP_400_BAD_REQUEST)
                         
    data = {
        "tip": request.data.get('tip'),
        "poster": request.data.get('poster'),
        "poster_email": request.data.get('poster_email'),
        "is_published": True if not request.data.get('is_published') else request.data.get('is_published'),
        "timestamp": datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    }

    # Add tip to database
    try:
        data = database.insert_row(
            table_name='tips_pythontip',
            data=data
        )

        # Posting the data to python tips web form
        # url = "https://docs.google.com/forms/d/e/1FAIpQLScsHklRH2-uplGYH_vxhtIin-zJS44bXQkAWCH7_N7nUdrGXw/viewform"
        # content = requests.get(url).content
        # soup = BeautifulSoup(content, "html.parser").find_all("form")[0]
        # payload = {
        #     "tip": "Test",
        #     "poster": "Daniel",
        #     "poster_email": "daniel@mail.com"
        # }
        # post = requests.post(url, data=payload)
        # print(post.content)
        return Response(data=data, status=status.HTTP_200_OK)
    except Exception:
        return Response(data={"status": False, "message": "Error inserting tip. Check the string format of 'tip' and make sure it contains valid characters"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_tip(request, tip_id):
    data = {
        "status": True,
        "message": "Update successful"
    }

    if tip_id not in [tip.get("id") for tip in database.select_table('tips_pythontip')]:
        return Response(data={"status": False, "message": "No such tip"}, status=status.HTTP_400_BAD_REQUEST)

    # Query database for a specific tip
    ineditable_fields = ['id', 'timestamp']
    for field in ineditable_fields:
        if field in request.data.keys():
            return Response(data={"status": False, "message": "Updating field '{}' is not allowed".format(field)}, status=status.HTTP_400_BAD_REQUEST)

    # Check for valid fields
    valid_fields = ['tip', 'poster', 'poster_email', 'is_published']
    for field in request.data.keys():
        if field not in valid_fields:
            return Response(data={"status": False, "message": "Invalid field: {}. Valid fields are: 'tip', 'poster, 'poster_email', 'is_published'".format(field)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        for key, value in request.data.items():
            database.update_row(
                table_name='tips_pythontip',
                target_column='id',
                value=tip_id,
                column_name=key,
                new_value=value
            )
    except Exception:
        return Response(data={"status": False, "message": "Error updating tip. Check the string format of 'tip' and make sure it contains valid characters"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_tip(request, tip_id):
    data = {
        "status": True,
        "message": "Deleted successfully"
    }
    if tip_id not in [tip.get("id") for tip in database.select_table('tips_pythontip')]:
        return Response(data={"status": False, "message": "No such tip"}, status=status.HTTP_400_BAD_REQUEST)
    database.delete_row(
        table_name='tips_pythontip',
        target_column='id',
        value=tip_id
    )
    return Response(data=data, status=status.HTTP_200_OK)