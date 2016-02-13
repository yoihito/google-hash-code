import matplotlib.pyplot as plt   
import parse_data as pd

def split_position(verts):
  position_x = []
  position_y = []
  for vert in verts:
    position_x.append(vert['position'][0])
    position_y.append(vert['position'][1])
  return (position_x, position_y)

def main():
    data = pd.read_data()

    warehouses_pos = split_position(data['warehouses'])
    orders_pos = split_position(data['orders'])
    orders_sizes = []
    for order in data['orders']:
        items_total_weight = 0
        for i in xrange(len(order['items'])):
            items_total_weight += -data['products_weights'][i]*order['items'][i]
        orders_sizes.append(items_total_weight)

    max_orders_size = max(orders_sizes)
    orders_sizes = map(lambda x: int(x/float(max_orders_size) * 100), orders_sizes)
    plt.scatter(orders_pos[0], orders_pos[1], s=orders_sizes, c='b')
    plt.scatter(warehouses_pos[0], warehouses_pos[1], c='r')
    plt.axis([0, data['field_size'][0], 0, data['field_size'][1]])
    plt.show()

if __name__ == '__main__':
    main()
