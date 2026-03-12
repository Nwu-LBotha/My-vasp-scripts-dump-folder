I am not too proffecient at programing and these scripts are a method for me to learn and deepen my programming experience. 

File processing for VASP can take time, evenmore so if there are alot of files to process. I have created some python scripts that can be run in a HPC enviornment. These scripts are not perfect and can be improved, however, I just them to check small things while doing my calculations. 

1) The scripts that I mostly use is to check the convergence after runs for those runs that do not finish even after multiple runs. This enables me to determine if the calculation is stuck between energies and wont converge. The other useful file is to save time from correcting the bader charges.
2) The Bader charges should be corrected to correspond with the ZVal of the atoms, which this script automatically does.
3) NEBs are a pain to do and even after determining the correct pathway, the Transition State can still be tricky to find. Instead of running the same calculations for NEBs, I have a script that creates a midpoint between selected images. After you check the highest saddle point, which does not show any imaginary values, you can use the script to calculate midpoints between the highest saddle point and the images next to the saddle point. This script interpolates the pathway to find a midpoint. Run a small TS optimisation on these midpoints and then run a frequency calculation.

I hope to complete more scripts in the future as I start moving towards machine learning techniques. 

Dr Louise M Botha
