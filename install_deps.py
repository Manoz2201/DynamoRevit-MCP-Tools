# install_deps.py
# This script uses the pyRevit API to install necessary libraries.
import os
from pyrevit.coreutils import extensions
from pyrevit.coreutils.depstools import install_package

# --- Configuration ---
# The name of the package we need to install
PACKAGE_TO_INSTALL = "requests"
# The name of the extension folder (must match the .extension folder name)
EXTENSION_NAME = "MCP-PyRevit"
# --- End Configuration ---

# Find the extension based on the current script's location
# This assumes the script is run from the root of the repository
print("Searching for extension '{}'...".format(EXTENSION_NAME))
ext_path = os.path.join(os.path.dirname(__file__), EXTENSION_NAME + ".extension")

if os.path.exists(ext_path):
    print("Found extension at: {}".format(ext_path))
    lib_dir = os.path.join(ext_path, 'lib')
    
    # Ensure the 'lib' directory exists
    if not os.path.exists(lib_dir):
        os.makedirs(lib_dir)

    print("Installing '{}' into '{}'...".format(PACKAGE_TO_INSTALL, lib_dir))
    
    # Install the package into the extension's lib directory
    result = install_package(PACKAGE_TO_INSTALL, target_dir=lib_dir)
    
    if result:
        print("\nInstallation successful!")
        print("You can now close this window and test the pushbutton in Revit.")
    else:
        print("\nInstallation failed. Please check any error messages above.")
else:
    print("\nError: Could not find the extension directory at the expected path.")
    print("Please ensure this script is in the same directory as the 'MCP-PyRevit.extension' folder.") 