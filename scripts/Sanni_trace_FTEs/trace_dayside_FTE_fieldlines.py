import pytools as pt
import numpy as np
#import yt
import matplotlib.pyplot as plt

save_path="/home/hoilijok/proj/analysator/scripts/Sanni_trace_FTEs/"

#levels = np.arange(2, 10.1, 2)
levels = (3.0, 5.0, 7.0)
numproc = 4
numthread = 64
chunksize=100

Re = 6.371e+6 # Earth radius in m
mp = 1.6726219e-27
mu0 = 1.256637e-6

# focus on dayside 
x_mp= [6, 11]
y_mp = [-10, 10]
z_mp = [-6, 6]


#import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('-t', help="Index of the file to process")
# parser.add_argument('-tracing', help="Run tracing (1) or VTK exporting (0)")
# args = parser.parse_args()


# if args.t == None:
#    print("No file index given with the -t option, exiting.")
#    exit()
# if args.tracing == None:
#    print("No value given to -tracing option, exiting.")
#    exit()
# if args.tracing == "1":
#    doTracing = True
# else:
#    doTracing = False
times=np.arange(1000,1400)

for index in times:
    print(index)
    # if doTracing:
    #f=pt.vlsvfile.VlsvReader("/wrk-vakka/group/spacephysics/vlasiator/3D/FID/bulk1/bulk1."+str(args.t).rjust(7, '0')+".vlsv")
    f=pt.vlsvfile.VlsvReader("/wrk-vakka/group/spacephysics/vlasiator/3D/FID/bulk1/bulk1."+str(index).rjust(7, '0')+".vlsv")

    # files for the magnetipause from Johanna's scripts
    #f_mp=

    ## Read flux rope data from vlsv files

    cid=f.read_variable("CellID")
    fluxrope=f.read_variable("vg_fluxrope")
    curvature=f.read_variable("vg_curvature")
    connection=f.read_variable("vg_connection")


    cid_list=cid[np.where(np.logical_and(fluxrope > 0, fluxrope <= levels[-1]))]
    fluxrope_list=fluxrope[np.where(np.logical_and(fluxrope > 0, fluxrope <= levels[-1]))]
    curvature_list=curvature[np.where(np.logical_and(fluxrope > 0, fluxrope <= levels[-1]))]
    connection_list=connection[np.where(np.logical_and(fluxrope > 0, fluxrope <= levels[-1]))]
    array=[]
    for i,val in enumerate(cid_list):
        crd = f.get_cell_coordinates(val)
        if  (x_mp[0] < crd[0]/Re < x_mp[1] ) and (y_mp[0] < crd[1]/Re < y_mp[1])  and (z_mp[0] < crd[2]/Re < z_mp[1]):
            c = curvature_list[i]
            c_rad = 1/np.sqrt(c[0]*c[0]+c[1]*c[1]+c[2]*c[2])
            array.append([crd[0],crd[1],crd[2],fluxrope_list[i],c_rad, connection_list[i]])

    array=np.array(array)
    streamlength = np.max(array[:,3]*array[:,4])
    streamline_seeds = array[:,:3]

    traced_fieldlines = pt.calculations.static_field_tracer_3d(vlsvReader=f,seed_coords=streamline_seeds, max_iterations=50, dx=1e6, direction='+-' )

    colours = [ '#377eb8', '#4daf4a', '#ff7f00','#984ea3', '#a65628','#f781bf' ,'#dede00']
    ax = plt.figure().add_subplot(projection='3d')
    for i,line in enumerate(traced_fieldlines):
        if array[i][5] < 5:
            ax.plot(line[:,0]/Re,line[:,1]/Re, line[:,2]/Re, color=colours[int(array[i][5])], lw=0.3, alpha=0.7 )

    ax.azim = 10
    ax.dist = 15
    ax.elev = 10
    ax.set_aspect('equal', 'box')
    ax.set_ylim()
    ax.se
    plt.savefig(save_path+'field_line_test'+str(index).rjust(7, '0')+'.png', dpi=300)



