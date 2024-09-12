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
from math import log


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

def one_client_RMS_list(Shop, trajectory_list, dt, variables):
    """
    Identical to one_client, but it takes in a list of variables
    :param Shop: (Shop) The shop considered
    :param trajectory_list: (list) list of the trajectories
    :param dt: (float) Time step
    :param variables: (list) list of the variables considered
    :return: (function) The one_client function with its arguments equal to the list variables
    """
    return one_client(Shop, trajectory_list, dt, variables[0], variables[1], variables[2], variables[3], variables[4], variables[5],variables[6], variables[7], variables[8], variables[9])['RMS']

def builder_RMS_k(k,values,shop, trajectory_list, dt):
    """
    It returns a function that is equal to one_client_RMS_list but with only one argument, that is equal to the k th element in the list values
    :param k: (int) Index of the element in the list values, it is the element that is going to be the argument of the returned function
    :param values: (list) list of all the values, this function uses the global variable values
    :param shop: (Shop) the shop considered
    :param trajectory_list: (list) list of the trajectories
    :param dt: (float) time step
    :return: (function) The function that is equal to one_client but with only values[k] as an argument
    """
    def RMS_k(moving_var):
        global values
        values_copy = list(values)
        values_copy[k] = moving_var
        return one_client_RMS_list(shop, trajectory_list, dt, values_copy)
    return RMS_k


def optimise(file_name, inital_values):
    '''
    Optimisation function, it is still a work in progress.
    :param file_name: (string) the name of the file where the data is stored
    :param inital_values: (list) initial values of the variables
    :return: (list) final values of the optimized variables
    '''
    [Shop, trajectory_list] = shop_and_data("..//..//..//data//{}".format(file_name)) #file_name = positions.txt
    values = list(inital_values)
    RMS_list = [builder_RMS_k(k,values, Shop, trajectory_list, dt) for k in range(9)]

    N = 50
    for n in range(2,N):
        for k in range(9):
            result = optimize.minimize(RMS_list[k],values[k], tol=200/log(n))
            if result.success:
                if result.x[0]>0:
                    values[k] = result.x[0]
    return values

if __name__ == "__main__":
    [Shop, trajectory_list] = shop_and_data("..//..//..//data//positions.txt")
    values = [lambd, d_0, F_wall0, F_stand0, F_0, v_max,F_exit, beta_customer, beta_wall, coef_fast_marching]
    RMS_list = [builder_RMS_k(k,values, Shop, trajectory_list, dt) for k in range(9)]

    N = 5
    for n in range(2,N):
        for k in range(9):
            print(N)
            result = optimize.minimize(RMS_list[k],values[k], tol=200/log(n))
            if result.success:
                if result.x[0]>0:
                    values[k] = result.x[0]
    print(values)