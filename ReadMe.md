# MGLite Project
**Project for displaying your images like a slide-show software within any browser that you want with custom configurations!**

## Overview
The ***MGLite*** Project, developed by ***Epixoul***, which includes three main scripts:  
- STPScr: Sets up the initial configurations.  
- HTCT: Launches an internal local browser (Windows OS only) to display slides from the "Slides" folder.
- SLDCT: Loads file from main root of driver or USB drive.
## Setup Guide

1. Browser Configuration  
   - Add a browser path that you don't use for daily activities.  
   - Disable "restore default or past session tabs" and any other pup-ups to prevent high RAM usage or ensure proper script functionality.

2. Slide Preparation  
   - Copy your slides in the format **"Slides/sld{numeric slide's order}.png"** into the **"/Slides"** folder.  
   - Optionally, you can add a USB flash drive or internal folder with the **"Slides"** folder in the root directory, e.g., *E:/Slides* or *C:/Slides*. In that case, script will load and replace all the images in that directory to the local **Slides** folder.

3. Running Scripts
   - Install python and the required packages from requirements.txt with **pip install -r requirements.txt** command.
   - Execute the setup file with **STPScr.py**. Run this script again, even if you encounter any issues.
   - Run **HTCT.py** to copy the slides and run the program, if there is as USB drive then you can safely eject or remove it. 

4. Auto Startup Configuration  
   - If you select "Yes" for **auto_run_startup**, the setup will run automatically after reboot.  
   - For manual operation, set "No" for **auto_run_startup**, and you will need to run **HTCT.py** each time after reboot.
5. Hazard!
   - Do not change format of script-tags with **"img-data"** and **"json-data"** Id on Html file!
6. Troubleshooting  
   - Check **log_stp.txt** and **log_launch.txt** for any errors.  
   - If issues persist, comment on GitHub repo [MGLite-SlideShow](https://github.com/epixoul/MGLite-SlideShow) or contact Epixoul support.
## Further development
1. Introduce incoming **auto_run_startup** config.
2. Auto check for the valid **Slides** path inside any directories.
3. Add lookup table to recognize uncommon browsers like **Microsoft Edge**, **DuckDuckGo**, **Tor**, etc.
5. Add **GUI MGGM**(MGLite GUI Manager) for better control over program.
6. Colorful-terminal would be re-added into the project, after it fixed.
7. Make the program scripts lite and more compact.
## At the end
I hope you find this project useful! For more information, visit my GitHub page [Epixoul.Github](https://github.com/epixoul).
<br/>*Copyright (c) 2025-2026, Epixoul All Rights Reserved*
