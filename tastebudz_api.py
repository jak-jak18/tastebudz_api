import logging, os, requests, json
import endpoints

from google.appengine.api import memcache
from google.appengine.ext import ndb
from protorpc import messages, remote
from oauth2client.service_account import ServiceAccountCredentials
from requests_toolbelt.adapters import appengine

from cloud_data import Item as DB_Item, Restaurant, Waiter as DB_Waiter

package = 'Tastebudz'

appengine.monkeypatch()

# Different message classes
class Item(messages.Message):
    course_name = messages.StringField(1, repeated=True)
    item_name = messages.StringField(2, repeated=True)
    description = messages.StringField(3, repeated=True)
    ingredients = messages.StringField(4, repeated=True)
    calories = messages.IntegerField(5, repeated=True, variant=messages.Variant.INT32)
    price = messages.FloatField(6, repeated=True)
    image_key = messages.StringField(7, repeated=True)

class UploadItem(messages.Message):
    course_name = messages.StringField(1, required=True)
    item_name = messages.StringField(2, required=True)
    description = messages.StringField(3)
    ingredients = messages.StringField(4)
    calories = messages.IntegerField(5, variant=messages.Variant.INT32)
    price = messages.FloatField(6)
    image_key = messages.StringField(7)
    res_name = messages.StringField(8, required=True)
    initial_name = messages.StringField(9)

class MenuCollection(messages.Message):
    menu_names = messages.StringField(1, repeated=True)
    coordinates = messages.FloatField(2, repeated=True)
    presentation = messages.StringField(3, repeated=True)

class OrderRequest(messages.Message):
    restaurant = messages.StringField(1, required=True)
    order_id = messages.StringField(2, required=True)
    order = messages.StringField(3, required=True)

class Waiter(messages.Message):
    restaurant = messages.StringField(1, required=True)
    reg_id = messages.StringField(2, required=True)
    group_num = messages.IntegerField(3, required=True, variant=messages.Variant.INT32)

class Response(messages.Message):
    response=messages.BooleanField(1, required=True)

# access token method
def _get_access_token():
    FCM_SCOPE = 'https://www.googleapis.com/auth/firebase.messaging'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(path, FCM_SCOPE)
    access_token_info = credentials.get_access_token()
    return access_token_info.access_token


@endpoints.api(name='backend', version='v1')
class TasteBudzApi(remote.Service):
    
    # Delete item when creating menu
    @endpoints.method(UploadItem, Response,
                      path='tastebudz/delete/item', http_method='POST',
                      name='generator.deleteItem')
    def delete_item(self, request):
        result = DB_Item.query(ndb.AND(DB_Item.res_name == request.res_name,
                                       DB_Item.item_name == request.item_name)).fetch()
        RESPONSE = Response()
        if len(result) == 0:
            logging.info('Attempted to delete ' + request.item_name
                         + ' for ' + request.res_name + '. No items returned.')
            RESPONSE.response = False
        else:
            item = result[0]
            item.key.delete()
            logging.info('Deleted ' + item.item_name + ' for ' + request.res_name)
            RESPONSE.response = True
        return RESPONSE


    # Add item when creating menu
    @endpoints.method(UploadItem, Response,
                      path='tastebudz/add/item', http_method='POST',
                      name='generator.addItem')
    def add_item(self, request):
        result = DB_Item.query(ndb.AND(DB_Item.res_name == request.res_name,
                                       DB_Item.item_name == request.initial_name)).fetch()
        if len(result) == 0:
            item = DB_Item()
            item.res_name = request.res_name
            item.course_name = request.course_name
        else:
            item = result[0]
        item.item_name = request.item_name
        item.description = request.description
        item.ingredients = request.ingredients
        item.calories = request.calories
        item.price = request.price
        key = item.put()
        if len(result) == 0:
            logging.info(request.item_name + ' created for ' + request.res_name + '. ID: ' + str(key.id()))
        else:
            logging.info(request.item_name + ' updated for ' + request.res_name + '. ID: ' + str(key.id()))
        RESPONSE = Response()
        RESPONSE.response = True
        return RESPONSE

    # Delete course when creating menu
    @endpoints.method(UploadItem, Response,
                      path='tastebudz/delete/course', http_method='POST',
                      name='generator.deleteCourse')
    def delete_course(self, request):
        logging.info('Deleting ' + request.course_name
                     + ' for ' + request.res_name)
        items = DB_Item.query(ndb.AND(DB_Item.res_name == request.res_name,
                                      DB_Item.course_name == request.course_name)).fetch()
        RESPONSE = Response()
        for item in items:
            item.key.delete()
            logging.info('Deleted ' + item.item_name + ' for ' + request.res_name)
        menu = Restaurant.query(Restaurant.name == request.res_name).fetch()
        if len(menu)>0:
            new_pres_order = menu[0].presentation            
            new_pres_order.remove(request.course_name)
            menu[0].presentation = new_pres_order
            menu[0].put()
            RESPONSE.response = True
        else:
            RESPONSE.response = False
        return RESPONSE

    # Add course when creating menu
    @endpoints.method(UploadItem, Response,
                      path='tastebudz/add/course', http_method='POST',
                      name='generator.addCourse')
    def add_course(self, request):
        RESPONSE = Response()
        menu_list = Restaurant.query(Restaurant.name == request.res_name).fetch()
        if len(menu_list)>0:
            menu = menu_list[0]
            new_pres_order = menu.presentation
            new_pres_order.append(request.course_name)
            menu.presentation = new_pres_order
            menu.put()
            logging.info(request.course_name + ' created for ' + request.res_name)
            RESPONSE.response = True
        else:
            RESPONSE.response = False
        return RESPONSE

    # Create menu by creating menu name 
    MENU_ID = endpoints.ResourceContainer(menu_name=messages.StringField(1))
    @endpoints.method(MENU_ID, Response,
                      path='tastebudz/menu/create/{menu_name}', http_method='GET',
                      name='menu.createMenu')
    def create_menu(self, request):
        RESPONSE = Response()
        restaurant = Restaurant()
        restaurant.name = request.menu_name
        restaurant.presentation = []
        key = restaurant.put()
        logging.info('New restaurant ' + request.menu_name + ' created. ID: ' + str(key.id()))
        RESPONSE.response = True
        return RESPONSE
    
    # Maintain menu presentation order
    @endpoints.method(MENU_ID, MenuCollection,
                      path='tastebudz/menu/presentation/{menu_name}', http_method='GET',
                      name='menu.getMenuPresentation')
    def menu_presentation(self, request):
        logging.info('Menu name: ' + request.menu_name + ' selected for menu info')
        menu = Restaurant.query(Restaurant.name == request.menu_name).fetch()
        if len(menu) == 0:
            logging.info('Course amount: None')
        else:
            logging.info('Total number of items: ' + str(len(menu)))
        try:
            MENUCOLLECTION = MenuCollection()
            if menu is None:
                raise endpoints.NotFoundException('No items in selected menu')
            MENUCOLLECTION.presentation = menu[0].presentation
            return MENUCOLLECTION
        except (IndexError, TypeError):
            if IndexError:
                raise endpoints.NotFoundException('Index Error')
            elif TypeError:
                raise endpoints.NotFoundException('%s not found.' %(request.menu_name))

    # Download menu
    @endpoints.method(MENU_ID, Item,
                      path='tastebudz/menu/get/{menu_name}', http_method='GET',
                      name='menu.getMenu')
    def menu_get(self, request):
        logging.info('Menu name: ' + request.menu_name + ' selected')
        items = DB_Item.query(DB_Item.res_name == request.menu_name).fetch()
        if len(items) == 0:
            logging.info('Course amount: None')
        else:
            logging.info('Total number of items: ' + str(len(items)))
        try:
            ITEMS = Item()
            if items is None:
                raise endpoints.NotFoundException('No items in selected menu')
            for item in items:
                ITEMS.course_name.append(item.course_name)
                ITEMS.item_name.append(item.item_name)
                ITEMS.description.append(item.description)
                ITEMS.ingredients.append(item.ingredients)
                ITEMS.calories.append(item.calories)
                ITEMS.price.append(item.price)
                ITEMS.image_key.append(item.image_key)
            return ITEMS
        except (IndexError, TypeError):
            if IndexError:
                raise endpoints.NotFoundException('Index Error')
            elif TypeError:
                raise endpoints.NotFoundException('%s not found.' %(request.menu_name))

    # Check to ensure that menu name is available
    @endpoints.method(MENU_ID, Response,
                      path='tastebudz/info/availability/{menu_name}', http_method='GET',
                      name='menu.getMenuAvailability')
    def menu_availability(self, request):
        logging.info('Checking availability for ' + request.menu_name)
        RESPONSE = Response()
        result = Restaurant.query(Restaurant.name == request.menu_name).fetch()
        if len(result)>0:
            RESPONSE.response = False
        else:
            RESPONSE.response = True
        return RESPONSE

    # Register waiter/device with restaurant name so that orders can be received 
    @endpoints.method(Waiter, Response,
                      path='tastebudz/waiter/register', http_method='POST',
                      name='waiter.registerWaiter')
    def register_waiter(self, request):
        RESPONSE = Response()
        mem_reg_id = memcache.get(request.restaurant)
        if mem_reg_id is None:
            RESPONSE.response = memcache.add(request.restaurant, request.reg_id)
            if RESPONSE.response:
                logging.info("Token registered for " + request.restaurant + ", new token location created.")
            else:
                logging.info("Token registration error")
        elif str(mem_reg_id) == "empty":
            RESPONSE.response = memcache.replace(request.restaurant, request.reg_id)
            if RESPONSE.response:
                logging.info("Token registered")
            else:
                logging.info("Token registration error")
        else:
            logging.info("Token already registered")
            RESPONSE.response = True
        return RESPONSE

    # unregister waiter
    @endpoints.method(Waiter, Response,
                      path='tastebudz/waiter/unregister', http_method='POST',
                      name='waiter.unRegisterWaiter')
    def unregister_waiter(self, request):
        RESPONSE = Response()
        result = memcache.replace(request.restaurant, "empty")
        if result is False:
             RESPONSE.response = memcache.add(request.restaurant, "empty")
             logging.info("Instance died")
        else:
            RESPONSE.response = True
        logging.info("Token unregistered for " + request.restaurant)
        return RESPONSE

    # order item
    @endpoints.method(OrderRequest, Response,
                      path='tastebudz/order', http_method='POST',
                      name='waiter.orderItem')
    def order_item(self, request):
        RESPONSE = Response()
        mem_reg_id = memcache.get(request.restaurant)
        if mem_reg_id is None:
            logging.info(request.restaurant + ' not found')
            RESPONSE.response = False
            return RESPONSE
        elif mem_reg_id == "empty":
            logging.info('Waiter not found')
            RESPONSE.response = False
            return RESPONSE
        else:
            url = 'https://fcm.googleapis.com/v1/projects/my-tastebudz/messages:send'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + _get_access_token()
            }
            data = {
                'message': {
                    'token': str(mem_reg_id),
                    'data': {
                        'ID': str(request.order_id),
                        'Order': str(request.order)
                    }
                }
            }
            resp = requests.post(url=url, headers=headers, data=json.dumps(data))
            RESPONSE.response = resp.ok
            return RESPONSE

APPLICATION = endpoints.api_server([TasteBudzApi])
