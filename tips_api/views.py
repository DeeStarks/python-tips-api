from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from python_tips_api.db_connection import database

# Create your views here.
@api_view(['GET'])
def fetchall(request):
    data = {
        "status": True,
        "message": "Fetched successfully"
    }
    # Query database for all tips
    print(database.select_table(table_name='tips_pythontip')[~0])
    db = database.select_row(
        table_name='tips_pythontip',
        key='id',
        value='946'
    )
    for d in db:
        print(d)
    return Response(data=data, status=status.HTTP_200_OK)
