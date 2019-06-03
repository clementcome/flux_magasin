from tkinter import Tk, Canvas
from model.static_graphic_display import store_display


def display_comparison(real_trajectory, calculated_trajectory, other_trajectories, shop):
    print(len(other_trajectories[0]))
    T = len(real_trajectory)
    N = len(other_trajectories[0])
    x_max = 0
    y_max = 0
    for t in range(T-1):
        for i in range(N-1):
            if other_trajectories[t][i][0] > x_max:
                x_max = other_trajectories[t][i][0]
            if other_trajectories[t][i][1] > y_max:
                y_max = other_trajectories[t][i][1]

    # Windows creation
    root = Tk()
    root.title('Magasin')

    murs = shop.getWalls()

    shop.calculate_x_y_max()
    x_max = shop.get_x_max()
    y_max = shop.get_y_max()

    store = Canvas(root, width=x_max+15, height=y_max+15)
    store.pack()

    # Display the shop
    store_display(shop, store)

    # Display the customers' starting point and retrieves the list of clients
    balls_list = []

    for customer in other_trajectories[0]:
        coord = customer
        balls_list.append(store.create_oval(coord[0] + 5, coord[1] + 5, coord[0] + 15, coord[1] + 15, fill='grey'))

    coord = real_trajectory[0]
    balls_list.append(store.create_oval(coord[0] + 5, coord[1] + 5, coord[0] + 15, coord[1] + 15, fill='green'))
    coord = calculated_trajectory[0]
    balls_list.append(store.create_oval(coord[0] + 5, coord[1] + 5, coord[0] + 15, coord[1] + 15, fill='deep pink'))

    print(balls_list)
    print(len(balls_list))
    print(T)
    print(N)

    # Movement of the customers
    for t in range(T):
        for id_customer in range(len(other_trajectories[t])):
            coord = other_trajectories[t][id_customer]
            store.coords(balls_list[id_customer], coord[0]+5, coord[1]+5, coord[0]+15, coord[1]+15)
        coord = real_trajectory[t]
        store.coords(balls_list[len(other_trajectories[t])], coord[0]+5, coord[1]+5, coord[0]+15, coord[1]+15)
        coord = calculated_trajectory[t]
        store.coords(balls_list[len(other_trajectories[t])+1], coord[0]+5, coord[1]+5, coord[0]+15, coord[1]+15)

        root.update()

    root.mainloop()

