About the Project

niiview is a python based tool, which can display 3D and 4D .nii and .nii.gz files
in terminals with sixel support. In it's default mode, niiview shows the middle of
a given NIfTI image, prints out basic information about it.
niiview also has an interactive mode, which enables the user to go through the
different slices of the brain with the keyboard.

It is based on the idea of https://github.com/MIC-DKFZ/niicat

How to Install

python3 -m venv ~/.venv/niiview
. ~/.venv/niiview/bin/activate
pip3 install git+https://jugit.fz-juelich.de/inm7/infrastructure/loony_tools/niiview
niiview file.nii.gz