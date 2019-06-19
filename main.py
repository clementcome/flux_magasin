from model import builder, matrix_representation_for_fast_marching
from model.environnement import Stand,Customer, Exit
from model.evolution import representation_evolution,one_client, fast_marching_to_exit, evolution_list
from model.static_graphic_display import window_creation, store_display, legend_creation
from model.environnement import Stand, Customer, Exit
from model.evolution import representation_evolution, one_client, fast_marching_to_exit, evolution_list, fast_marching_to_exit_with_display
from model.link_with_video import shop_and_data
from model.display import display_comparison, display_trajectory, display_ideal
import matplotlib.pyplot as plt
import json
import skfmm
import scipy.optimize as optimize
import random as rd

T = 300

Stands_test = [Stand(10, 10, 35, 60), Stand(100, 80, 120, 140)]
Customers_test = [Customer(rd.uniform(160,200), rd.uniform(120,140), 0, 0) for i in range(100)]


Shop_test = builder([[0, 0],
                     [0, 100], "sortie", [0, 150],
                     [0, 200],
                     [150, 200], "sortie", [180, 200],
                     [300, 200], [300, 0],
                     [245, 0], "entree", [200, 0],
                     [0, 0]], 50, Stands_test)

Shop_test.addStand(Stands_test)
Shop_test.addCustomer(Customers_test)

## Display of the evolution

T = 300
dt = 1
F_0 = 10
F_wall0 = 0
d_0 = 1
F_stand0 = F_wall0/4
F_exit = 10
v_max = .1
lambd = 1/2
beta_customer = 10
beta_wall = 10
coef_fast_marching = 5*10**3
experience_list = []

# representation_evolution(Shop_test, .1, T)
# evolution_list(Shop_test, T, dt, lambd, d_0, F_wall0, F_stand0, F_0, v_max, F_exit, beta_customer, beta_wall, coef_fast_marching)

## Representation of the fast-marching

# matrix_representation_for_fast_marching(Shop_test)
# phi = matrix_representation_for_fast_marching(Shop_test)
# d1 = fast_marching_to_exit_with_display(phi, Exit(0, 100, 0, 150), Shop_test)[0]
# d2 = fast_marching_to_exit_with_display(phi, Exit(150, 200, 180, 200), Shop_test)[0]
# plt.imshow(d1+d2)
## optimisation : display the real and the calculated trajectory

Shop_test_one_client = builder([[0,0],
                                [0, 200],
                                [150, 200], "entree_sortie", [180, 200],
                                [300, 200], [300, 0],
                                [245, 0], "entree", [200, 0],
                                [10, 0]], 45, Stands_test)
Shop_test_one_client.addCustomer(Customers_test)

T = 3000
dt = 1
F_0 = 10
F_wall0 = 0
d_0 = 1
F_stand0 = F_wall0/4
F_exit = 10
v_max = .1
lambd = 1/2
beta_customer = 10
beta_wall = 10
coef_fast_marching = 5*10**3
experience_list = []

[Shop, trajectory_list] = shop_and_data('..\data\positions.txt')
result = one_client(Shop, trajectory_list, dt, lambd, d_0, F_wall0, F_stand0, F_0, v_max,F_exit, beta_customer, beta_wall, coef_fast_marching)
#display_comparison(result['real_trajectory'], result['calculated_trajectory'], result['other_trajectories'], Shop)
display_trajectory(result['real_trajectory'], result['calculated_trajectory'], result['other_trajectories'])

