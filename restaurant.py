import os
import sys
import io
import csv
import boto3
from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, Blueprint, request, make_response, flash, Response, render_template,  session, redirect, url_for
from flask_session import Session
from utils import *
import time
import json
import decimal
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('restaurant') # pylint: disable=no-member

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=method-hidden
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

bp = Blueprint('restaurant', __name__, url_prefix='/restaurant')

# get a list of all restaurants
@bp.route('', methods=['GET'])
def get_all_restaurants():
    response = table.scan()

    return (json.dumps(response['Items'], cls=DecimalEncoder))

# create a restaurant
@bp.route('', methods=['POST'])
def create_restaurant():

    content = request.get_json()

    # generate random UUID for restaurant_id
    new_restaurant_id = str(uuid.uuid4())

    response = table.put_item(
            Item={
                'restaurant_id': new_restaurant_id,
                'restaurant_name': content['restaurant_name'],
                'restaurant_latitude': content['restaurant_latitude'],
                'restaurant_longitude': content['restaurant_longitude'],
                'phone_num': content['phone_num'],
                'address_line1': content['address_line1'],
                'address_line2': content['address_line2'],
                'city': content['city'],
                'state': content['state'],
                'postal_code': content['postal_code']
            }
        )

    return(new_restaurant_id, 201, {'Content-Type': 'application/json'})


# Get restaurant information
@bp.route('/<restaurant_id>', methods=['GET','POST'])
@check_user_login
def get_restaurant(customer_username, customer_id, restaurant_id):
    # get restaurant name
    restaurant_table=dynamodb.Table('restaurant') # pylint: disable=no-member
    restaurant_data = restaurant_table.scan(
        FilterExpression=Attr('restaurant_id').eq(restaurant_id)
    )
    restaurant_name = restaurant_data['Items'][0]['restaurant_name']

    # get menu id
    menu_table=dynamodb.Table('menu') # pylint: disable=no-member
    response = menu_table.scan(
        FilterExpression=Attr('restaurant_id').eq(restaurant_id)
    )
    menu_id = response['Items'][0]['menu_id']

    # get menu items
    menu_item_table=dynamodb.Table('menu_item') # pylint: disable=no-member
    response = menu_item_table.scan(
        FilterExpression=Attr('menu_id').eq(menu_id)
    )
    
    menu_object = {}
    for x in response['Items']:
        # for displaying by item_type, if the item_type isn't in the dict, then create a new item_type to display
        if x['item_type'] not in menu_object:
            menu_object[x['item_type']] = [{
            'menu_item_id': x['menu_item_id'],
            'item_name': x['item_name'],
            'item_description': x['item_description'],
            'item_unit_price': str(x['item_unit_price'])
            }]
        else:
            menu_object[x['item_type']].append(
                {
            'menu_item_id': x['menu_item_id'],
            'item_name': x['item_name'],
            'item_description': x['item_description'],
            'item_unit_price': str(x['item_unit_price'])
            }
            )

    menu_data = json.dumps(response['Items'], cls=DecimalEncoder)
    
    new_menu = json.dumps(menu_object)

    if request.method == 'GET':

        return render_template('restaurant.html', customer_username=customer_username, customer_id=customer_id, restaurant_id=restaurant_id, restaurant_name=restaurant_name,menu_data=menu_data, new_menu=menu_object)


# Delete a restaurant
@bp.route('/<restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    response = table.delete_item(
        Key={'restaurant_id': restaurant_id}
    )

    return ("", 204)


