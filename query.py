from data import stock
from datetime import datetime

def decoration(func):
    '''Decorate the message by stars'''
    def inner(*args, **kwargs):
        print('*'*80)
        func(*args, **kwargs)
        print('*'*80)
    return inner

def ask_to_order(decision):
    '''Ask user does he/she want to order the product'''    
    if decision == 'n':
        '''Disagree'''
        None

    elif decision == 'y':
        '''Agree'''
        order_quantity = int(input('How many would you like? '))
        if order_quantity > total_quantity:
            message_for_customer(total_quantity)
            '''Order more than available (accepting and not accepting)'''
            repeat_order_decision = input('Would you like to order the maximum available?(y/n) ')
            if repeat_order_decision == 'n':
                None
            elif repeat_order_decision == 'y':
                print(f'{total_quantity} {desired_product} have been ordered.')
            else:
                print(f'Wrong choice. Please try again!')
        elif order_quantity <= total_quantity:
            '''Order the available quantity'''
            print(f'{order_quantity} {desired_product} have been ordered.')
        elif order_quantity <= 0:
            '''Order less than Zero'''
            print(f'Wrong quantity. Please try again!')
    else:
        '''Wrong choice'''
        print(f'Wrong choice. Please try again!')

@decoration
def message_for_customer(quantity):
    print(f'There are not this many available. The maximum amount that can be ordered is {quantity}')

@decoration
def valid_operation_message():
    print('Search is not a valid operation.')







# START

username = input('What is your user name? ')
print(f'\nHello {username}!')

#MENU

'''There is no message by default, but if a user selects Choice 1 (main menu) it's going to have a text.'''
message_after_listing_products = ''
while True:
    if len(message_after_listing_products) > 0:
        print('_'*85, message_after_listing_products)
    print('\nWhat would you like to do?: \n1. Show list items by warehouse\n2. Search an item and place an order\n3. Browse by category \n4. Quit')
    choice = input('Type the number of the operation: ')
    if choice.isdigit() and (choice == '1' or choice == '2' or choice == '3' or choice == '4'):

        # CHOICE 1

        if choice == '1':
            '''List the items'''
            total_items_1 = 0
            total_items_2 = 0
            print('\nItems in warehouses:\n')
            for position in stock:
                if position['warehouse'] == 1:
                    total_items_1 += 1
                elif position['warehouse'] == 2:
                    total_items_2 += 1
                print(position['state'], position['category'])
            print('\nTotal items in warehouse 1: ', total_items_1)
            print('Total items in warehouse 2: ', total_items_2)
            message_after_listing_products = '\n\nItems in warehouses were listed above (please scroll up). \nPlease select something and enter the operation 2. Or enter the operation 4 to exit. \nThank you'
        
        # CHOICE 2

        elif choice == '2':
            '''Message at first try empty, but on the second try and more has a text'''
            message_after_first_purchase = ''
            while True:
                if len(message_after_first_purchase) > 0:
                    print('_'*85, message_after_first_purchase)
                desired_product = input(f'\nWhat is the name of the item? ')
                if desired_product == 'Exit':
                    break
                else:                    
                    quantity_1 = 0
                    quantity_2 = 0
                    bigger_quantity = 0
                    warehouse = 0
                    bigger_warehouse = 0
                    time_now = datetime.now().date()
                    location = []

                    '''Count products, define warehouse and count days'''
                    for position in stock:
                        name = [position['state'], position['category']]
                        name = ' '.join(name)
                        if name.lower() == desired_product.lower():
                            if position['warehouse'] == 1:
                                warehouse = 1
                                quantity_1 += 1
                            elif position['warehouse'] == 2:
                                warehouse = 2
                                quantity_2 += 1
                            time_stored = position['date_of_stock']
                            time_stored = datetime.strptime(time_stored, "%Y-%m-%d %H:%M:%S").date()
                            delta = time_now - time_stored
                            location.append(f'- Warehouse {warehouse} (in stock for {delta.days} days)')
                            
                    '''Count total products in two warehouses'''
                    total_quantity = quantity_1 + quantity_2
                    location.sort()

                    if quantity_1 == 0 and quantity_2 == 0:
                        '''Item not found'''
                        print(f'Amount available: {total_quantity}\nLocation: Not in stock')

                    elif quantity_1 > 0 and quantity_2 > 0:
                        '''Item found:'''
                        if quantity_1 > quantity_2:
                            bigger_quantity = quantity_1
                            bigger_warehouse = 1
                        elif quantity_1 < quantity_2:
                            bigger_quantity = quantity_2
                            bigger_warehouse = 2
                        elif quantity_1 == quantity_2:
                            bigger_quantity = quantity_1
                            bigger_warehouse = 1

                    elif quantity_1 > 0 and quantity_2 == 0:
                        bigger_quantity = quantity_1
                        bigger_warehouse = 1

                    elif quantity_1 == 0 and quantity_2 > 0:
                        bigger_quantity = quantity_2
                        bigger_warehouse = 2

                    print(f'Amount available: {total_quantity}\nLocation:')
                    '''List every item'''
                    for item in location:
                        print(item)
                    print(f'\nMaximum availability: {bigger_quantity} in Warehouse {bigger_warehouse}\n')
                    order_decision = input('Would you like to order this item?(y/n) ')
                    ask_to_order(order_decision)

                message_after_first_purchase = f'\n\nWould you like to order another product? If yes, please write a name of the product. \nIf not, please write "Exit" to return to previous menu.'
        
        # CHOICE 3

        elif choice == '3':
            list_category = []
            dict_category = {}
            for position in stock:
                if position['category'] not in list_category:
                    list_category.append(position['category'])
            print('')
            for i in range(1, len(list_category)+1):
                count = 0
                for position in stock:
                    if position['category'] == list_category[i-1]:
                        count += 1
                print(f'{i}. {list_category[i-1]} ({count})')
                dict_category[i] = list_category[i-1]

            choice_browse = int(input('Type the number of the category to browse: '))
            print('\nList of laptops available: ')
            for key, value in dict_category.items():
                if key == choice_browse:
                    for position in stock:
                        if value == position['category']:
                            print(position['state'], position['category'] +',', 'Warehouse', position['warehouse'])

            message_after_listing_products = '\n\nItems by selected category in warehouses were listed above (please scroll up). \nPlease select something and enter the operation 2. Or enter the operation 4 to exit. \nThank you'

        # CHOICE 4

        elif choice == '4':
            break
        
        # ANOTHER NUMBER

        else:
            print('')
            valid_operation_message()
    else:
        print('')
        valid_operation_message()

print(f'\nThank you for your visit, {username}!')




