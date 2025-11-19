import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import IPython.display as display
from matplotlib.lines import Line2D

"""I wrote all of the functions here to then import them on my notebooks and use them"""

def life_game(grid):

    """Here we compute grids with the same size as the original one, each of them contaning, respectively, right hand side neighbours, 
    left hand side neighbours, up and down neighbours, and neighbours along all 4 diagonals (left down, right down, left up, right up). 
    This is simply done by removing one of the rows and/or columns, shifting the cropped matrix, and then filling the remaining rows 
    and/or columns with zeros. We then just sum them all and, for example, position (1,1) of this matrix will be a number from 1-8 
    representing the sum of all of the number surrounding it in the original grid."""

    #We will have to fill matrixes with rows of zero so we mightt as well create them now to help;
    #We need 1d arrays with the length oif the original grid and some with the length of the original grid minus one (for the diagonals)
    aux0_gridsize = np.zeros(np.size(grid[:,0]), dtype= int)
    aux0_gridsize_minus1 = np.zeros(np.size(grid[1:,0]), dtype= int)
    
    #now compute the neighbouring matrices (left and right hand side, up and down)
    rhs_neighbours = np.column_stack(( grid[:,1:], aux0_gridsize ))
    lhs_neighbours = np.column_stack( (aux0_gridsize, grid[:,:-1] ))
    down_neighbours = np.vstack(( grid[1:,:], aux0_gridsize ))
    up_neighbours = np.vstack(( aux0_gridsize, grid[:-1,:] ))

    #diagonal neighbours
    diag_rd_neighbours = np.vstack(( np.column_stack(( grid[1:,1:], aux0_gridsize_minus1 )), aux0_gridsize ))
    diag_ld_neighbours = np.column_stack(( aux0_gridsize, np.vstack(( grid[1:,:-1], aux0_gridsize_minus1 )) ))
    diag_ru_neighbours = np.vstack(( aux0_gridsize, np.column_stack(( aux0_gridsize_minus1, grid[:-1,:-1] )) ))
    diag_lu_neighbours = np.column_stack(( np.vstack(( aux0_gridsize_minus1, grid[:-1,1:] )), aux0_gridsize ))
    
    #now all 8 of the neighbouring matrices are compurted, all there is left to do is to sum them and then either kill or mantain the cell
    #which, in the original grid, corresponds to that position in the neighbour_sum matrix
    neighbour_sum = rhs_neighbours + lhs_neighbours + down_neighbours + up_neighbours + diag_ld_neighbours 
    + diag_lu_neighbours + diag_rd_neighbours + diag_ru_neighbours

    #check the rules are respected
    two_or3_neighbours = np.logical_or(neighbour_sum == 2, neighbour_sum ==3)
    exactly3_neighbours = neighbour_sum==3
    live_cells = grid==1

    #either kill a cell or make it alive in a new grid
    new_grid = grid.copy()
    #if it's alive and it doesnt have 2 or 3 (less than two or more than three), it becomes dead
    cells_to_kill = np.logical_and(live_cells == True, two_or3_neighbours == False)
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
    while i<=n_iterations:
        grid = life_game(grid)
        print("i =", i, ",\n", grid)
        i+=1



def play_life_game_wplots(grid, n_iterations):
    """Here we can play the game of life as the previous function but we can visualize it graphically using matplotlib animation"""
    i=int(0)

    fig, ax = plt.subplots(figsize = (8,8))
    fig.suptitle(r"Conway's game of life")

    #give it the initial image and then append the others
    initial_image = ax.imshow(grid, cmap = "binary", animated = True)
    artists = [[initial_image]] 


    for i in range(1, n_iterations + 1):
        grid = life_game(grid)
        newim = ax.imshow(grid, cmap = "binary", animated = True)
        artists.append([newim])

    
    ani = animation.ArtistAnimation(fig, artists, interval=50)
    video = ani.to_html5_video()
    html = display.HTML(video)
    display.display(html)
    plt.close()