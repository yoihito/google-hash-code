def read_data():
    f = open('input.txt')
    r, c, drones_num, turns, max_payload = map(int, f.readline()[:-1].split(' '))
    num_of_products = int(f.readline()[:-1])
    products_weights = map(int, f.readline()[:-1].split(' '))
    warehouses = []
    num_of_warehouses = int(f.readline()[:-1])
    for i in xrange(num_of_warehouses):
        position = map(int, f.readline()[:-1].split(' '))
        items = [0] * num_of_products
        _items = map(int, f.readline()[:-1].split(' '))
        for k, j in enumerate(_items):
            items[k] += j
        warehouses.append({
            'id': len(warehouses),
            'disabled': False,
            'position': position,
            'items': items
        })
    orders = []
    num_of_orders = int(f.readline()[:-1])
    for i in xrange(num_of_orders):
        position = map(int, f.readline()[:-1].split(' '))
        items = [0] * num_of_products
        f.readline()  # Num of items
        _items = map(int, f.readline()[:-1].split(' '))
        for j in _items:
            items[j] -= 1
        orders.append({
            'id': len(orders),
            'position': position,
            'items': items
        })
    return {
        'field_size': (r,c),
        'drones_num': drones_num,
        'turns': turns,
        'max_payload': max_payload,
        'products_weights': products_weights,
        'warehouses': warehouses,
	    'orders': orders
    }
