import os
import sys
import io
import csv
import boto3
from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, Blueprint, request, make_response, flash, Response, render_template,  session, redirect, url_for
from flask_session import Session
from utils import *
import json
import decimal
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
# table = dynamodb.Table('restaurant') # pylint: disable=no-member

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=method-hidden
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

bp = Blueprint('order', __name__, url_prefix='/order')

@bp.route('/<restaurant_id>', methods=['GET','POST'])
@check_user_login
def get_order(customer_username, customer_id, restaurant_id):
    
    order = request.form["restaurant_id"]
    print(order)

    return render_template('order.html', customer_username=customer_username, customer_id=customer_id, restaurant_id=restaurant_id, order=order)
    
    # # get restaurant name
    # restaurant_table=dynamodb.Table('restaurant') 
    # restaurant_data = restaurant_table.scan(
    #     FilterExpression=Attr('restaurant_id').eq(restaurant_id)
    # )
    # restaurant_name = restaurant_data['Items'][0]['restaurant_name']

    # # get menu id
    # menu_table=dynamodb.Table('menu') 
    # response = menu_table.scan(
    #     FilterExpression=Attr('restaurant_id').eq(restaurant_id)
    # )
    # menu_id = response['Items'][0]['menu_id']

    # # get menu items
    # menu_item_table=dynamodb.Table('menu_item')
    # response = menu_item_table.scan(
    #     FilterExpression=Attr('menu_id').eq(menu_id)
    # )
    
    # menu_data = json.dumps(response['Items'], cls=DecimalEncoder)

    # if request.method == 'GET':

    #     return render_template('restaurant.html', customer_username=customer_username, customer_id=customer_id, restaurant_id=restaurant_id, restaurant_name=restaurant_name,menu_data=menu_data)

    # if request.method == 'POST':
    #     menu_item_id = request.form['menu_item_id']



