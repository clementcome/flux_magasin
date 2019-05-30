from tkinter import Tk, Canvas
from model.environnement import Wall,StandWall,Shop,Stand,Customer,Entry,Exit

def window_creation(shop):
    """
    Create the Tkinter window and canvas in which we will display the shop
    :param shop: (Shop) the shop to display
    :return: None
    """
    global root
    root = Tk()
    root.title('Shop')

    # Search the size of the window we should use
    walls = shop.getWalls()
    x_max, y_max = shop.get_x_max(), shop.get_y_max()
    x_min, y_min = shop.get_x_min(), shop.get_y_min()

    global store
    store = Canvas(root, width=x_max + 20, height=y_max + 20)
    store.pack()

    store.create_rectangle(x_min, y_min, x_max, y_max)
    # store['scrollregion'] = (x_min - 10, y_min - 10, x_max + 10, y_max + 10)

    return root, store


def legend_creation():
    """
    Create a Tkinter window with the legend of the display
    :return: None
    """
    window = Tk()
    window.title('Legend')

    canvas = Canvas(window)
    canvas.pack()

    canvas.create_line(30, 20, 60, 20, width=10, capstyle='projecting')
    canvas.create_text(110, 20, text='Wall')

    for i in range(5, 15):
        canvas.create_line(25, 50+i, 65, 50+i, width=1, fill='blue', dash=(1,1))
    canvas.create_text(110, 60, text='Entry')

    for i in range(5, 15):
        canvas.create_line(25, 90+i, 65, 90+i, width=1, fill='red', dash=(1,1))
    canvas.create_text(110, 100, text='Exit')

    for i in range(5, 15):
        canvas.create_line(25, 130+i, 65, 130+i, width=1, fill='blue', dash=(1,1))
        canvas.create_line(28, 130+i, 65, 130+i, width=1, fill='red', dash=(1,1))
    canvas.create_text(110, 140, text='Entry and exit')

    canvas.create_rectangle(28, 170, 58, 200, fill='purple')
    canvas.create_text(110, 185, text='Stand')

    canvas.create_oval(38, 220, 48, 230, fill='green')
    canvas.create_text(110, 225, text='Customer')

    window.mainloop()


def store_display(shop, canvas):
    """
    Displays the shop
    :param shop: (Shop) the shop to display
    :param canvas: (Tkinter canvas) the canvas used to draw
    :return: None
    """

    stands = shop.getStands()
    walls = shop.getWalls()
    entries = shop.getEntries()
    exits = shop.getExits()

    for stand in stands:
        coord = stand.getPos()
        canvas.create_rectangle(coord[0] + 10, coord[1] + 10, coord[2] + 10, coord[3] + 10, fill='purple')

    for wall in walls:
        coord = wall.getPos()
        canvas.create_line(coord[0] + 10, coord[1] + 10, coord[2] + 10, coord[3] + 10, width=10, capstyle='projecting')

    for entry in entries:
        coord = entry.getPos()
        canvas.create_line(coord[0] + 10, coord[1] + 10, coord[2] + 10, coord[3] + 10, width=10, fill='white')
    for exit in exits:
        coord = exit.getPos()
        canvas.create_line(coord[0] + 10, coord[1] + 10, coord[2] + 10, coord[3] + 10, width=10, fill='white')

    for entry in entries:
        coord = entry.getPos()
        if coord[0] == coord[2]:
            for i in range(5, 15):
                canvas.create_line(coord[0] + i, coord[1] + 10, coord[2] + i, coord[3] + 10, width=1, fill='blue', dash=(1, 1))
        elif coord[1] == coord[3]:
            for i in range(5, 15):
                canvas.create_line(coord[0] + 10, coord[1] + i, coord[2] + 10, coord[3] + i, width=1, fill='blue', dash=(1, 1))
    for exit in exits:
        coord = exit.getPos()
        if coord[0] == coord[2]:
            for i in range(5, 15):
                canvas.create_line(coord[0] + i, coord[1] + 13, coord[2] + i, coord[3] + 10, width=1, fill='red', dash=(1, 1))
        elif coord[1] == coord[3]:
            for i in range(5, 15):
                canvas.create_line(coord[0] + 13, coord[1] + i, coord[2] + 10, coord[3] + i, width=1, fill='red', dash=(1, 1))

    root.mainloop()


def customers_display(shop, canvas, direction=False):
    """
    Displays the customers (in their first position)
    :param shop: (Shop) the shop to display
    :param canvas: (Tkinter canvas) the canvas used to draw
    :param direction: (Boolean) Whether the vector representing the speed (so the direction) of each customer should be represented
    :return: balls_list : the list of balls representing each customer
            lines_list : the list of vectors representing each speed
    """
    customers = shop.getCustomers()
    balls_list = []
    lines_list = []
    for customer in customers:
        coord = customer.getPos()
        balls_list.append(canvas.create_oval(coord[0] + 5, coord[1] + 5, coord[0] + 15, coord[1] + 15, fill='green'))
        if direction:
            speed = customer.getSpeed()
            lines_list.append(canvas.create_line(coord[0] + 10, coord[1] + 10, coord[0] + 5 * speed[0] + 10, coord[1] + 5 * speed[1] + 10, fill='green', arrow='last'))
    return balls_list, lines_list




if __name__ == '__main__':

    Murs_test = [Wall(0,0,0,200), Wall(0,200,300,200), Wall(300,200,300,0), Wall(300,0,0,0)]
    Entrees_test = [Entry(200,0,245,0,45), Entry(150,200,180,200,45)]
    Sorties_test = [Exit(0,100,0,150), Exit(150,200,180,200)]
    Meubles_test = [Stand(0,0,25,50), Stand(150,150,250,180)]
    Clients_test = [Customer(45,78,3,4,6), Customer(187,23,7,7,7)]

    Shop_test = Shop('test')
    for wall in Murs_test:
        Shop_test.addWall(wall)
    for stand in Meubles_test:
        Shop_test.addStand(stand)
    for entry in Entrees_test:
        Shop_test.addEntry(entry)
    for exit in Sorties_test:
        Shop_test.addExit(exit)
    for client in Clients_test:
        Shop_test.addCustomer(client)


    window_creation(Shop_test)
    store_display(Shop_test, store)
    customers_display(Shop_test, store)
    root.mainloop()

    legend_creation()


def stop(root):
    root.destroy()
