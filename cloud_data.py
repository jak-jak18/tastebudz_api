
from google.appengine.ext import ndb

# Model classes
class Item(ndb.Model):
    calories = ndb.IntegerProperty()
    course_name = ndb.StringProperty()
    description = ndb.StringProperty()
    image_key = ndb.StringProperty()
    ingredients = ndb.StringProperty()
    item_name = ndb.StringProperty()
    price = ndb.FloatProperty()
    rating = ndb.FloatProperty()
    res_name = ndb.StringProperty()

class Restaurant(ndb.Model):
    name = ndb.StringProperty()
    coordinates = ndb.GeoPtProperty()
    presentation = ndb.StringProperty(repeated=True)

class Order(ndb.Model):
    order_id = ndb.StringProperty()
    order = ndb.StringProperty()
    time = ndb.DateTimeProperty()

class Waiter(ndb.Model):
    restaurant = ndb.StringProperty()
    reg_id = ndb.StringProperty()

# Sample data
my_restaurant = Restaurant(name='My Restaurant',
                           coordinates=ndb.GeoPt(39.9372025, -75.6309027),
                           presentation=['Beverage','Soup','Sandwich','Vegetables','Entree','Dessert'])

turkey_sandwich = Item(res_name='My Restaurant',
                       course_name = 'Sandwich',
                       item_name='Turkey Sandwich',
                       description='Classic Turkey Sandwich with a pickle.',
                       ingredients='Whole wheat bread, turkey, swiss cheese, mayo, grey poupon',
                       calories= 120,
                       price= 4.99,
                       image_key= 'images-88523/My Restaurant/Turkey Sandwich')

corned_beef = Item(res_name='My Restaurant',
                   course_name = 'Sandwich',
                   item_name='Corned Beef Sandwich',
                   description='Deli style sandwich served with cole slaw.',
                   ingredients='Rye bread, Corned Beef, thousand islands dressing, cole slaw',
                   calories= 220,
                   price= 7.49,
                   image_key='images-88523/My Restaurant/Corned Beef Sandwich')

lamb_gyro = Item(res_name='My Restaurant',
                 course_name = 'Sandwich',
                 item_name='Lamb Gyro',
                 description='Slow roasted lamb and vegetables served in a pita wrap.',
                 ingredients='Pita Bread, Lamb, Vegetables, Green Sauce',
                 calories= 590,
                 price= 9.99,
                 image_key='images-88523/My Restaurant/Lamb Gyro')

tomato_soup = Item(res_name='My Restaurant',
                   course_name='Soup',
                   item_name='Tomato Soup',
                   description='Homemade tomato soup with fresh tomato and cream.',
                   ingredients='Tomatoes, vegetable broth, cream, assorted spices',
                   calories= 140,
                   price= 4.99,
                   image_key='images-88523/My Restaurant/Tomato Soup')

clam_chowder = Item(res_name='My Restaurant',
                    course_name='Soup',
                    item_name='New England Clam Chowder',
                    description='Homemade chowder made in Boston.',
                    ingredients='Cream based, assorted vegetables, potatoes, clam meat',
                    calories= 400,
                    price= 4.99,
                    image_key='images-88523/My Restaurant/New England Clam Chowder')

veg_beef = Item(res_name='My Restaurant',
                course_name='Soup',
                item_name='Vegetable Beef Stew',
                description='Perfect stew for the Fall and Winter seasons.',
                ingredients='Tomato Juice, Diced Beef, Assorted Vegetables',
                calories= 350,
                price= 4.99,
                image_key='images-88523/My Restaurant/Vegetable Beef Stew')

mousaka = Item(res_name='My Restaurant',
               course_name='Entree',
               item_name='Moussaka',
               description='Greek Lasagna.',
               ingredients='Eggplant, ground beef, onion, garlic, tomato sauce, bechemal sauce',
               calories= 350,
               price= 11.99,
               image_key='images-88523/My Restaurant/Moussaka')

lamb = Item(res_name='My Restaurant',
            course_name='Entree',
            item_name='Rack of Lamb',
            description='Roast rack of lamb oven baked to perfection.',
            ingredients='Rack of Lamb, dijion mustard rub',
            calories= 320,
            price= 15.99,
            image_key='images-88523/My Restaurant/Rack of Lamb')

cordon_bleu = Item(res_name='My Restaurant',
                   course_name='Entree',
                   item_name='Chicken Corden Bleu',
                   description='Chicken breast baked with gruyere cheese inside.',
                   ingredients='Chicken, cheese, rice, sauce',
                   calories= 400,
                   price= 12.99,
                   image_key='images-88523/My Restaurant/Chicken Corden Bleu')

apple_pie = Item(res_name='My Restaurant',
                 course_name='Dessert',
                 item_name='Apple Pie',
                 description='Served al la mode or seperate.',
                 ingredients='Fresh apples, homade dough, cinnamon and 100% sugar cane',
                 calories= 210,
                 price= 3.99,
                 image_key='images-88523/My Restaurant/Apple Pie')

choc_mousse = Item(res_name='My Restaurant',
                   course_name='Dessert',
                   item_name='Chocolate Mousse',
                   description='Not to be confused with a chocolate moose.',
                   ingredients='Bittersweet chocolate, egg whites, sugar, cream',
                   calories= 450,
                   price= 6.99,
                   image_key='images-88523/My Restaurant/Chocolate Mousse')

cheese = Item(res_name='My Restaurant',
              course_name='Dessert',
              item_name='Cheese Plate',
              description='Fancy dessert for sophisticated people.',
              ingredients='Zimbro, Pimiento, Harbison, Bleu Mont Bandaged Cheddar',
              calories= 100,
              price= 6.99,
              image_key='images-88523/My Restaurant/Cheese Plate')



water = Item(res_name='My Restaurant',
             course_name='Beverage',
             item_name='Water',
             description='A beverage that will keep you alive.',
             ingredients='Two parts hydrogen, one part oxygen.',
             calories= 0,
             price= 0,
             image_key='images-88523/My Restaurant/Water')

turkey_hill_iced_tea = Item(res_name='My Restaurant',
                            course_name='Beverage',
                            item_name='Turkey Hill Iced Tea',
                            description='My kind of Iced tea. Dilluted with water.',
                            ingredients='Tea, Water, some sugar.',
                            calories= 90,
                            price= 0.99,
                            image_key='images-88523/My Restaurant/Turkey Hill Iced Tea')

dad_iced_tea = Item(res_name='My Restaurant',
                    course_name='Beverage',
                    item_name='Dads Iced Tea',
                    description='Glorified Water.',
                    ingredients='Water',
                    calories= 0,
                    price= 1.99,
                    image_key='images-88523/My Restaurant/Dads Iced Tea')

hot_tea = Item(res_name='My Restaurant',
               course_name='Beverage',
               item_name='Hot Tea',
               description='Fancy Tea for sophisticated people.',
               ingredients='Hot Water, Tea, some honey.',
               calories= 30,
               price= 1.99,
               image_key='images-88523/My Restaurant/Hot Tea')

brussel_sprouts = Item(res_name='My Restaurant',
                       course_name='Vegetables',
                       item_name='Brussel Sprouts',
                       description='Healthy greens for the refined taste.',
                       ingredients='Brussel Sprouts',
                       calories= 38,
                       price= 1.00,
                       image_key='images-88523/My Restaurant/Brussel Sprouts')

carrots = Item(res_name='My Restaurant',
               course_name='Vegetables',
               item_name='Steamed Carrots',
               description='Healthy orange sticks.',
               ingredients='carrots',
               calories= 25,
               price= 1.50,
               image_key='images-88523/My Restaurant/Steamed Carrots')

def input_items():
    ndb.put_multi([turkey_sandwich, corned_beef, lamb_gyro,
               tomato_soup, clam_chowder, veg_beef,
               mousaka, lamb, cordon_bleu,
               apple_pie, choc_mousse, cheese,
               water, turkey_hill_iced_tea, dad_iced_tea,
               hot_tea, brussel_sprouts, carrots])

def input_restaurant():
    my_restaurant.put()

if __name__ == '__main__':
    input_items()



