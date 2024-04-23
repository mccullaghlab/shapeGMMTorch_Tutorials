import numpy as np
import matplotlib.pyplot as plt
import MDAnalysis as md
from shapeGMMTorch import torch_sgmm
import torch
import nglview as nv
import pickle


# Make Ramachandran plot
def rama_plot(ax,phi,psi,c,title,fontsize=16):
    # make a grid
    ax.grid(which='major', axis='both', color='#808080', linestyle='--')
    # set ticks and axis labels
    ax.tick_params(axis='both',labelsize=fontsize)
    ax.set_ylabel("$\psi$",fontsize=fontsize)
    ax.set_xlabel("$\phi$",fontsize=fontsize)
    ax.set_title(title,fontsize=fontsize)
    # scatter plot
    ax.scatter(phi, psi,c=c,s=0.4)
    # enforce range
    ax.set_ylim(-180,180)
    ax.set_xlim(-180,180)
    # equal aspect ratio
    ax.set_aspect("equal")


from MDAnalysis.lib.distances import calc_dihedrals
# make fe
def plot_rama_sgmm_fe(ax,fig,phi,psi,sgmm_obj,title,fontsize=16,contour_levels= np.arange(0,30,1)):
    nbins  = 32
    range_ = [-180,180]

    phis = calc_dihedrals(sgmm_obj.centers[:,0,:],sgmm_obj.centers[:,2,:],sgmm_obj.centers[:,3,:],sgmm_obj.centers[:,4,:])
    psis = calc_dihedrals(sgmm_obj.centers[:,2,:],sgmm_obj.centers[:,3,:],sgmm_obj.centers[:,4,:],sgmm_obj.centers[:,6,:])
    H, xedges, yedges = np.histogram2d(phi, psi, bins=nbins,\
                                   range=[range_, range_], weights=sgmm_obj.train_frame_weights*np.exp(sgmm_obj.train_frame_log_likelihood))
    bin_weights = np.histogram2d(phi, psi, bins=nbins,\
                                   range=[range_, range_], weights=sgmm_obj.train_frame_weights)[0]

    H = -np.log(H) + np.log(bin_weights)
    H = H.T
    H -= np.nanmin(H)

    xcenters = (xedges[:-1] + xedges[1:]) / 2
    ycenters = (yedges[:-1] + yedges[1:]) / 2

    xx, yy = np.meshgrid(xcenters, ycenters)

    ax.set_xlabel("$\phi$", fontsize=fontsize)
    ax.set_ylabel("$\psi$", fontsize=fontsize)
    ax.set_title(title,fontsize=fontsize)
    ax.contour(xx, yy, H, cmap="binary", levels=5, linestyles="--")
    ax.contourf(xx, yy, H, cmap='jet', levels=20)
    #ax.set_clim(0,50)
    #cbar = fig.colorbar()
    #cbar.set_label("FE/kT", fontsize=fontsize)
    ax.scatter(phis*180/np.pi, psis*180/np.pi, marker='o', s=200*sgmm_obj.weights, color="black")

def plot_rama_metaD_fe(ax,fig,phi,psi,rbias,title,fontsize=16,gamma=10,contour_levels= np.arange(0,30,1)):
    nbins  = 32
    range_ = [-180,180]
    kt = 0.596161
    
    H, xedges, yedges = np.histogram2d(phi, psi, bins=nbins,\
                                   range=[range_, range_], weights=np.exp(rbias/kt))

    H = -np.log(H.T)
    H *= gamma/(gamma-1)   #! check here it is mutiplied by pre-factor!!
    H *= kt  #! check here multiplying by kt
    H -= np.nanmin(H)

    xcenters = (xedges[:-1] + xedges[1:]) / 2
    ycenters = (yedges[:-1] + yedges[1:]) / 2

    xx, yy = np.meshgrid(xcenters, ycenters)

    ax.set_xlabel("$\phi$", fontsize=fontsize)
    ax.set_ylabel("$\psi$", fontsize=fontsize)
    ax.set_title(title,fontsize=fontsize)
    ax.contour(xx, yy, H, cmap="binary", levels=5, linestyles="--")
    ax.contourf(xx, yy, H, cmap='jet', levels=20)
    #plt.clim(0,50)
    #cbar = fig.colorbar()
    #cbar.set_label("FE/kT", fontsize=fontsize)

    