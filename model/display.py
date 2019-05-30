def display_comparison(real_trajectory, calculated_trajectory, other_trajectories, shop):
    T = len(real_trajectory)
    N = len(other_trajectories)
    x_max = 0
    y_max = 0
    for t in range(T):
        for i in range(N):
            if other_trajectories[i][t][0] > x_max:
                x_max = other_trajectories[i][t][0]
            if other_trajectories[i][t][1] > y_max:
                y_max = other_trajectories[i][t][1]

    
