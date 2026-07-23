import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import IPython.display as display
import matplotlib.colors as mcolors


def life_game(grid):

    """
    Here we compute grids with the same size as the original one, each of them contaning, respectively, north, south, west, east and then all the diagonal neighbours. 
    This is simply done by rolling the matrix in one direction, in a way that the element/ row/ column that gets pushed over the edge, introduces itself on the opposite edge, so the game should go on for longer because edge cells are not considered dead.
    We sum all of the rolled matrices and check if any of the elemnts opf the matrix are less than 2 or more than 3, and then kill/reproduce cells in the original grid accordingly."""

    # Treat the grid as a torus: cells on one edge see the opposite edge as their neighbour.
    # This avoids boundary cells dying just because the board ends.
    grid = np.asarray(grid, dtype=int)

    north = np.roll(grid, 1, axis=0)
    south = np.roll(grid, -1, axis=0)
    west = np.roll(grid, 1, axis=1)
    east = np.roll(grid, -1, axis=1)
    north_west = np.roll(north, 1, axis=1)
    north_east = np.roll(north, -1, axis=1)
    south_west = np.roll(south, 1, axis=1)
    south_east = np.roll(south, -1, axis=1)

    # Sum all 8 neighbours explicitly. 
    neighbour_sum = (
        north + south + west + east + north_west + north_east + south_west + south_east
    )

    #check the rules are respected
    kill_live_cell = np.logical_or(neighbour_sum < 2, neighbour_sum >3)
    exactly3_neighbours = neighbour_sum==3
    live_cells = grid==1

    #either kill a cell or make it alive in a new grid
    new_grid = grid.copy()
    #if it's alive and it doesnt have 2 or 3 (less than two or more than three), it becomes dead
    cells_to_kill = np.logical_and(live_cells == True, kill_live_cell == True)
    new_grid[cells_to_kill==True] = 0
    #if it's dead and has exactly 3 live neighbours, it becomes alive
    cells_to_become_alive = np.logical_and(live_cells == False, exactly3_neighbours == True)
    new_grid[cells_to_become_alive==True] = 1  

    return new_grid 


def play_life_game(grid, n_iterations):
    """Here we simply play the game, giving as an input some grid which is a 2D array of 0s and 1s, and the number of iterations
    we want the game to go on for. The 2D arrays are printed as we go."""
    i=int(1)
    print("initial state: \n", grid)

    grid_list = [grid]
    while i<=n_iterations:
        grid = life_game(grid)
        grid_list.append(grid)
        print("i =", i, ",\n", grid)
        i+=1

    return grid_list


def play_life_game_wplots(grid, n_iterations):
    """Here we can play the game of life as the previous function but we can visualize it graphically using matplotlib animation"""
    i=int(0)

    fig, ax = plt.subplots(figsize = (5,5))
    fig.suptitle(r"Conway's game of life")
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()

    my_cmap = mcolors.ListedColormap(["lightcyan", "darkcyan"])

    #give it the initial image and then append the others
    initial_image = ax.imshow(grid, cmap = my_cmap, animated = True)
    artists = [[initial_image]] 


    for i in range(1, n_iterations + 1):
        grid = life_game(grid)
        newim = ax.imshow(grid, cmap = my_cmap, animated = True)
        artists.append([newim])

    ani = animation.ArtistAnimation(fig, artists, interval=50)
    plt.close(fig)
    return ani

#To see the dynamical plot in your code, simply save the return of this function, as such:
#ani.save("life_game.gif", writer="ffmpeg", fps=20)

