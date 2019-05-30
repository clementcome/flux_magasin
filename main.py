from model import builder, matrix_representation_for_fast_marching
from model.environnement import Stand,Customer, Exit
from model.evolution import representation_evolution,one_client, fast_marching_to_exit, evolution_list
from model.static_graphic_display import window_creation, store_display
from model.environnement import Stand, Customer, Exit
from model.evolution import representation_evolution, one_client, fast_marching_to_exit, evolution_list
from model.link_with_video import shop_and_data
import json
import skfmm
import scipy.optimize as optimize

T = 300

# Walls_test = [Wall(0, 0, 0, 200), Wall(0, 200, 300, 200), Wall(300, 200, 300, 0), Wall(300, 0, 0, 0)]
# Entries_test = [Entry(200, 0, 245, 0, 45), Entry(150, 200, 180, 200, 45)]
# Exits_test = [Exit(0, 100, 0, 150), Exit(150, 200, 180, 200)]
Stands_test = [Stand(10, 10, 35, 60), Stand(100, 80, 120, 140)]
Customers_test = [Customer(210, 5, 0, 4), Customer(220, 10, -0, 4), Customer(225, 6, -0, 3)]


Shop_test = builder([[0, 0],
                     [0, 100], "sortie", [0, 150],
                     [0, 200],
                     [150, 200], "entree", [180, 200],
                     [300, 200], [300, 0],
                     [245, 0], "entree", [200, 0],
                     [0, 0]], 50, Stands_test)
# Shop_test.addWall(Walls_test)
Shop_test.addStand(Stands_test)
# Shop_test.addEntry(Entries_test)
# Shop_test.addExit(Exits_test)
Shop_test.addCustomer(Customers_test)

#representation_evolution(Shop_test, .1, T)

# optimisation
Shop_test_one_client = builder([[0, 0],
                                [0, 100], "sortie", [0, 150],
                                [0, 200],
                                [150, 200], "entree_sortie", [180, 200],
                                [300, 200], [300, 0],
                                [245, 0], "entree", [200, 0],
                                [0, 0]], 45, Stands_test)
Shop_test_one_client.addCustomer(Customers_test)

T = 300
dt = 1
F_0 = 10
F_wall0 = 200
d_0 = 1
F_stand0 = F_wall0/4
F_exit = 10
v_max = 4
lambd = 1/2
beta_customer = 10
beta_wall = 10
coef_fast_marching = 5
experience_list = []

#evolution_list(Shop_test_one_client, T, dt, lambd, d_0, F_wall0, F_stand0, F_0, v_max, F_exit, beta_customer, beta_wall, coef_fast_marching)

# value = one_client(Shop_test_one_client, experience_list, dt, lambd, d_0, F_wall0, F_stand0, F_0, F_exit, beta_customer, beta_wall, coef_fast_marching)

# matrix_representation_for_fast_marching(Shop_test_one_client)
# phi = matrix_representation_for_fast_marching(Shop_test_one_client)
# fast_marching_to_exit(phi, Exit(0, 100, 0, 150), Shop_test_one_client)

[Shop, trajectory_list] = shop_and_data()


def RMS(variables):
    global Shop
    global trajectory_list
    global dt
    return one_client(Shop, trajectory_list, dt, variables[0], variables[1], variables[2], variables[3], variables[4], variables[5],variables[6], variables[7], variables[8], variables[9])['RMS']

init_values = [lambd, d_0, F_wall0, F_stand0, F_0, v_max,F_exit, beta_customer, beta_wall, coef_fast_marching]
result = optimize.minimize(RMS, init_values, tol=30)
if result.success:
    fitted_params = result.x
    print(fitted_params)
else:
    raise ValueError(result.message)
def RMS_beta(beta_customer):
    global Shop
    global trajectory_list
    global dt
    global lambd
    global d_0
    global F_exit
    global F_stand0
    global F_wall0
    global v_max
    global beta_wall
    global coef_fast_marching
    return one_client(Shop, trajectory_list, dt, lambd, d_0, F_wall0, F_stand0, F_0, v_max,F_exit, beta_customer, beta_wall, coef_fast_marching)['RMS']

init_value = beta_wall
result_beta = optimize.minimize(RMS_beta, init_value, tol=5)
if result_beta.success:
    fitted_params_beta = result_beta.x
    print(fitted_params_beta)
else:
    raise ValueError(result_beta.message)