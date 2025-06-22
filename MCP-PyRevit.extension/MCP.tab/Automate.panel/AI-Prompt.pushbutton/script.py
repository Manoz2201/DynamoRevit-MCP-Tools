# -*- coding: utf-8 -*-
import clr
import os
import sys

# Add the script's directory to the system path to find the XAML file
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.append(script_dir)

# Load .NET assemblies
clr.AddReference("PresentationFramework")
clr.AddReference("System.Windows.Forms")
from System.Windows import Application, Window
from System.Windows.Markup import XamlReader
from System.IO import File

class MCP_UI(Window):
    def __init__(self, xaml_file):
        """Initializes the UI window by loading it from a XAML file."""
        try:
            with File.OpenRead(xaml_file) as f:
                self.ui = XamlReader.Load(f)
        except Exception as e:
            print("Error loading XAML file: {}".format(e))
            return

        # Connect UI elements to methods
        self.ui.browse_button.Click += self.browse_for_files
        self.ui.run_button.Click += self.run_automation
        
        # Store selected files
        self.selected_files = []

    def browse_for_files(self, sender, args):
        """Opens a file dialog to select reference files."""
        dialog = System.Windows.Forms.OpenFileDialog()
        dialog.Multiselect = True
        dialog.Title = "Select Reference Files"
        
        if dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK:
            self.selected_files = list(dialog.FileNames)
            self.ui.files_label.Text = "{} files selected".format(len(self.selected_files))
            print("Selected files: " + ", ".join(self.selected_files))

    def run_automation(self, sender, args):
        """Placeholder for running the automation."""
        prompt = self.ui.prompt_textbox.Text
        api_key = self.ui.api_key_box.Text
        mcp_user = self.ui.mcp_user_box.Text
        mcp_pass = self.ui.mcp_pass_box.Password

        print("--- Running MCP Automation ---")
        print("Prompt: " + prompt)
        print("API Key set: " + str(bool(api_key)))
        print("MCP User: " + mcp_user)
        print("MCP Password set: " + str(bool(mcp_pass)))
        print("Reference Files: " + ", ".join(self.selected_files))
        
        # In the next phase, we will add logic here to:
        # 1. Call the OpenRouter API with the prompt.
        # 2. Authenticate with the MCP.
        # 3. Use the MCP tools to interact with Dynamo.
        
        self.ui.Close()

if __name__ == "__main__":
    xaml_file_path = os.path.join(script_dir, "ui.xaml")
    if os.path.exists(xaml_file_path):
        ui = MCP_UI(xaml_file_path)
        ui.ui.ShowDialog()
    else:
        print("Could not find ui.xaml. Please ensure it is in the same directory as script.py.") 