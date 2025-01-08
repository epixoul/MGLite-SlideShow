import os
import win32api
from pathlib import Path
import shutil

#You don't need to call this script manually by terminal!
#This code will search for existing "Slides" path in main root of any drive that represented as physical drive
#And it will import and replace all existing images with "sld{number}.png" name and extension format.
def import_imgs():
    """This will import slides from ``Slides-folder`` in main root ``Like:X:/Slides`` of any physical driver or USB-stick.

    Return:
        If your local ``Slides-folder`` was empty, it will raise a corruption error.
    """
    log_val = []
    try:
        dev_dir=""
        drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
        log_val.append(f"Drives found -> {drives}")
        for device in drives:

            path= Path(f"{device}Slides")
            if Path.exists(path) and os.listdir(path):
                dev_dir= f"{device}Slides"
                break
        ct=0
        if dev_dir:
            for entry in os.listdir("Slides"):
                os.remove(f"Slides/{entry}")
            for entry in os.listdir(dev_dir):
                full_path = os.path.join(dev_dir, entry)
                shutil.copyfile(full_path, f"Slides/sld{ct}.png")
                ct+=1
            log_val.append(f"Slides load from driver -> Successfully {len(os.listdir(dev_dir))} slides imported.")
        else:   log_val.append(f"Slides load from drive err -> Path/driver doesn't exist or Null. -> To import slides, please install driver or declare proper slides-path in main root.")
    except Exception as err:
        log_val.append(f"Drivers import err -> {err}")
    return log_val