#!/home/tkadelka/env/niicat_env/bin/python3

import os
import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np
import nibabel as nb
from getkey import getkey, keys
from libsixel import *
from PIL import Image
from io import BytesIO


# plot the selected slices
def create_plot():

    # coronal
    ax1.imshow(
        nifti_data[:, show[1], :],
        aspect=nifti_image.header['pixdim'][3] / nifti_image.header['pixdim'][1],
    ).set_cmap('gray')

    # sagittal
    ax2.imshow(
        nifti_data[show[0], :, :],
        aspect=nifti_image.header['pixdim'][3] / nifti_image.header['pixdim'][2],
    ).set_cmap('gray')

    # axial
    ax3.imshow(
        nifti_data[:, :, show[2]],
        aspect=nifti_image.header['pixdim'][2] / nifti_image.header['pixdim'][1]
    ).set_cmap('gray')
    ax4.clear()
    plt.axis('off')
    ax4.text( 0.15, 0.95, get_text(), horizontalalignment='left', verticalalignment='top', size=6, color='white')
    #plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)



# build information
def get_text():
    return str(
            "(W/S) -> " + str(show[1]+1) + "/" + str(nifti_data.shape[1]) + " left" + "\n"
          + "(E/D) -> " + str(show[0]+1) + "/" + str(nifti_data.shape[2]) + " right" + "\n"
          + "(Q/A) -> " + str(show[2]+1) + "/" + str(nifti_data.shape[2]) + " down" + "\n"
          )



    dimensions = str()             + " x " +  str(nifti_data.shape[1])            + " x " + str(nifti_data.shape[2])
    voxelsize  = str(nifti_image.header['pixdim'][1]) + " x " + str(nifti_image.header['pixdim'][2]) + " x, " + str(nifti_image.header['pixdim'][3]) + " mm"
    return str( "Dimensions : "  + dimensions + "\n"
              + "Voxel-size : "  + voxelsize + "\n"
              + "Time-points: " + str(nifti_image.header['dim'][4]) + "\n" )



# this function reads the keyboard and calls the function for creating the image.
def display_nifti():
    # enable changing of global nifti-data for changing point in time
    global nifti_data
    # create, open and show nifti in terminal
    while( True ):
        # create a jpg from this koordinates of the nifti
        create_plot( )
        plt.savefig( tmp_nifti_file_name )

        #read jpg, display it, close it
        s = BytesIO()
        image = Image.open(tmp_nifti_file_name)
        width, height = image.size
        data = image.tobytes()
        output = sixel_output_new(lambda data, s: s.write(data), s)
        dither = sixel_dither_new(256)
        sixel_dither_initialize(dither, data, width, height, SIXEL_PIXELFORMAT_RGB888)
        sixel_encode(data, width, height, 1, dither, output)
        os.system("clear")
        print(s.getvalue().decode('ascii'))
        image.close()

        # wait for user to press a key. For arrows, change displayed slice.
        # "enter"-key exit the function
        key = getkey()
        # change up-right
        if key in ['e']:
            if show[0] + 10 >= nifti_data.shape[0]:
                show[0] = nifti_data.shape[0]-1
            else:
                show[0] = show[0] + 10
        elif key in ['d']:
            if show[0] - 10 <= 0:
                show[0] = 0
            else:
                show[0] = show[0] - 10
        # change up-left
        elif key in ['w']:
            if show[1] + 10 >= nifti_data.shape[1]:
                show[1] = nifti_data.shape[1]-1
            else:
                show[1] = show[1] + 10
        elif key in ['s']:
            if show[1] - 10 <= 0:
                show[1] = 0
            else:
                show[1] = show[1] - 10
        # change down-left
        elif key in ['q']:
            if show[2] + 10 >= nifti_data.shape[2]:
                show[2] = nifti_data.shape[2]-1
            else:
                show[2] = show[2] + 10
        elif key in ['a']:
            if show[2] - 10 <= 0:
                show[2] = 0
            else:
                show[2] = show[2] - 10
        # change point in time
        elif key in ['t']:
                if fourth_d == -1:
                    continue
                if fourth_d + 1 < nifti_data.shape[4]:
                    nifti_data = nifti_image.get_data()[:, :, :, fourth_d+1 ]
        elif key in ['g']:
                if fourth_d == -1:
                    continue
                if fourth_d - 1 >= 0:
                    nifti_data = nifti_image.get_data()[:, :, :, fourth_d-1 ]
        else:
            return


##### TODO: Check 4d-function, it was never tried!!!!!!!!!!!!!
#####
# the mainfunction of the niiview-tool
def main():

    #### parse arguments from terminal ####
    parser = argparse.ArgumentParser(description="Generate a nifti image in the terminal.")
    parser.add_argument("nifti_file")
    parser.add_argument("--dpi", metavar="N", type=int, help="resolution for plotting (default: 150).", default=150)
    parser.add_argument("--show", metavar="N", type=str, help="coordinates that will be plotted", default="50,50,50")
    args = parser.parse_args()

    #### set global vars ####
    global nifti_image, nifti_data, tmp_nifti_file_name, fig_jpeg, ax1, ax2, ax3, ax4, show, fourth_d
    # Try to load the nifti-data from arguments and check for errors
    nifti_image = nb.load( args.nifti_file )
    # get 3D-image (first time point) in case of 4D-input
    if nifti_image.header['dim'][0] == 3:
        nifti_data = nifti_image.get_data()
        # no time points given
        fourth_d = -1
    elif nifti_image.header['dim'][0] == 4:
        nifti_data = nifti_image.get_data()[:, :, :, 0]
        fourth_d = 0
    # name of a temporary jpg-file where data is written into, so libsixel can read it
    tmp_nifti_file_name = ".nifti.jpg"
    # Disable Toolbar for plots
    plt.rcParams['toolbar'] = 'None'
    # Set rounding
    np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
    # Set NAN-values to 0
    nifti_data[np.isnan(nifti_data)] = 0
    # Black background
    plt.style.use('dark_background')
    # build main window
    fig_jpeg = plt.figure( facecolor='black', figsize=(5, 4), dpi=args.dpi )
    # add axes
    ax1 = fig_jpeg.add_subplot(2, 2, 1)
    plt.axis('off')
    ax2 = fig_jpeg.add_subplot(2, 2, 2)
    plt.axis('off')
    ax3 = fig_jpeg.add_subplot(2, 2, 3)
    plt.axis('off')
    ax4 = fig_jpeg.add_subplot(2, 2, 4)
    plt.axis('off')
    show = []
    # selects middle slices as default vaulues for the koordinates 
    show = [ int(nifti_data.shape[0]/2), int(nifti_data.shape[1]/2) , int(nifti_data.shape[2]/2) ]

    #### open/show the image ####
    display_nifti()



# standard call
if __name__ == '__main__':
    main()

