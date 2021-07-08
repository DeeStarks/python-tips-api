from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from python_tips_api.db_connection import database
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
@api_view(['GET'])
def fetch_tips(request):
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
            column_name='id',
            value=tip_id
        )
    except ObjectDoesNotExist:
        data["status"] = False
        data["message"] = "No such tip"
    return Response(data=data, status=status.HTTP_200_OK)
