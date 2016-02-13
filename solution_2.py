import parse_data as pd
import pdb

warehouse_id = 0

def has_free_drons(drons):
    return reduce(lambda x,y: x | (y['cooldown'] == 0), drons, False)

def get_free_dron(drons):
    for i in xrange(len(drons)):
        if drons[i]['cooldown'] == 0:
            return drons[i]
    return None

def completed_order(order):
    return reduce(lambda x, y: x + y, order['items'], 0) == 0

def distance(position_a, position_b):
    return abs(position_a[0] - position_b[0]) + abs(position_a[1] - position_b[1])

def has_open_orders(orders):
    return any(filter(lambda x: completed_order(x), orders))

def warehouse_has_any_item(warehouse, order):
    items = zip(warehouse['items'], order['items'])
    for item in items:
        if item[0] > 0 and item[1] < 0:
            return True
    return False

def get_nearest_order(orders, warehouse):
    min_distance = 2170000000
    nearest_order = None
    for order in orders:
        if distance(order['position'], warehouse['position']) < min_distance \
        and warehouse_has_any_item(warehouse, order) \
        and not completed_order(order):
            min_distance = distance(order['position'], warehouse['position'])
            nearest_order =  order
    if nearest_order == None:
        pdb.set_trace()
    return nearest_order

def get_dron_start_warehouse(dron, warehouses):
    warehouses_num = len(warehouses)
    return warehouses[dron['id'] % warehouses_num]

def get_not_disabled_warehouse(dron, warehouses):
    for warehouse in warehouses:
        if not warehouse['disabled']:
            return warehouse
    return None

def pack_dron(dron, max_dron_size, order, products, warehouse):
    current_size = 0
    loads = []
    delivers = []
    for i in xrange(len(order['items'])):
        load = 0
        while order['items'][i] < 0 \
        and warehouse['items'][i] > 0 \
        and current_size + products[i] <= max_dron_size:
            current_size += products[i]
            order['items'][i] += 1
            warehouse['items'][i] -= 1
            load+=1
        if load>0:
            loads.append([dron['id'], 'L', warehouse['id'], i, load])
            delivers.append([dron['id'], 'D', order['id'], i, load])
    dron['cooldown'] = len(loads) + len(delivers) + distance(order['position'], dron['position']) + distance(warehouse['position'], dron['position'])
    dron['position'] = order['position']
    return (loads, delivers)

def output_commands(commands):
    for command in commands: 
        command = map(lambda x: str(x), command)
        print ' '.join(command)

def main():
    commands = []
    data = pd.read_data()
    products = data['products_weights']
    warehouses = data['warehouses']
    max_dron_size = data['max_payload']
    num_of_orders = len(data['orders'])
    drons = []
    for i in xrange(data['drones_num']):
        drons.append({
            'id': i, 
            'position': warehouses[warehouse_id]['position'], 
            'cooldown': 0,
        })
        drons[-1]['warehouse'] = get_dron_start_warehouse(drons[-1], warehouses)
    
    turn = 0
    while turn < data['turns']: 
        while has_free_drons(drons):
            dron = get_free_dron(drons)
            order = get_nearest_order(data['orders'], dron['warehouse'])
            while order == None:
                dron['warehouse']['disabled'] = True
                if get_not_disabled_warehouse(dron, warehouses) == None:
                    break
                dron['warehouse'] = get_not_disabled_warehouse(dron, warehouses)
                order = get_nearest_order(data['orders'], dron['warehouse'])

            loads, delivers = pack_dron(dron, max_dron_size, order, products, dron['warehouse'])
            output_commands(loads)
            output_commands(delivers)
            
        commands = []
        for dron in drons:
            if dron['cooldown'] > 0:
                dron['cooldown'] -= 1
        turn+=1


    
if __name__ == '__main__':
    main()