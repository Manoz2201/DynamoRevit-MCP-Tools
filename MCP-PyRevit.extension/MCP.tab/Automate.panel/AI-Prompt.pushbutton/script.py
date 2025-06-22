# -*- coding: utf-8 -*-
import clr
import os
import sys
import json
import subprocess
from pyrevit import script

# NOTE: You must install the 'requests' library into your extension's 'lib' folder
# using the command: pyrevit extend lib --name requests --dest "MCP-PyRevit.extension"
try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Please install it using the PyRevit CLI.")
    sys.exit()

# Add the script's directory to the system path to find the XAML file
script_dir = os.path.dirname(__file__)
CONFIG_SECTION = 'MCP_AI_PROMPT_TOOL' # Unique name for our settings
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

        # Find UI elements from the loaded XAML
        self.prompt_textbox = self.ui.FindName("prompt_textbox")
        self.browse_button = self.ui.FindName("browse_button")
        self.files_label = self.ui.FindName("files_label")
        self.api_key_box = self.ui.FindName("api_key_box")
        self.mcp_user_box = self.ui.FindName("mcp_user_box")
        self.mcp_pass_box = self.ui.FindName("mcp_pass_box")
        self.run_button = self.ui.FindName("run_button")

        # Load saved settings
        self.load_settings()

        # Connect UI elements to methods
        self.browse_button.Click += self.browse_for_files
        self.run_button.Click += self.run_automation
        
        # Store selected files
        self.selected_files = []

    def load_settings(self):
        """Loads API key from the config file and populates the UI."""
        print("Loading saved settings...")
        saved_api_key = script.get_config(CONFIG_SECTION).get_option('api_key', '')
        if saved_api_key:
            self.api_key_box.Text = saved_api_key
            print("API Key loaded from config.")

    def save_settings(self):
        """Saves the current API key to the config file."""
        print("Saving settings...")
        cfg = script.get_config(CONFIG_SECTION)
        cfg.api_key = self.api_key_box.Text
        script.save_config()
        print("API Key saved.")

    def browse_for_files(self, sender, args):
        """Opens a file dialog to select reference files."""
        dialog = System.Windows.Forms.OpenFileDialog()
        dialog.Multiselect = True
        dialog.Title = "Select Reference Files"
        
        if dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK:
            self.selected_files = list(dialog.FileNames)
            self.files_label.Text = "{} files selected".format(len(self.selected_files))
            print("Selected files: " + ", ".join(self.selected_files))

    def run_automation(self, sender, args):
        """Processes the user prompt, calls the AI, and executes the correct MCP tool."""
        # Save the current settings first
        self.save_settings()

        prompt = self.prompt_textbox.Text
        api_key = self.api_key_box.Text
        # MCP credentials are not used in this version but are collected for future use
        # mcp_user = self.mcp_user_box.Text
        # mcp_pass = self.mcp_pass_box.Password

        if not api_key:
            print("Error: OpenRouter API Key is required.")
            return

        print("--- Calling AI Model ---")
        try:
            # 1. Call the OpenRouter API
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": "Bearer {}".format(api_key)
                },
                data=json.dumps({
                    "model": "google/gemini-flash-1.5", # TODO: Replace with your preferred model
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant that determines which tool to use based on a prompt. Respond with only a JSON object in the format: { \"tool\": \"<tool_name>\", \"file_path\": \"<path_to_file>\" }"},
                        {"role": "user", "content": prompt}
                    ]
                })
            )
            response.raise_for_status() # Raises an exception for bad status codes
            ai_response = response.json()
            
            # Extract the tool and file path from the AI's response
            message_content = ai_response['choices'][0]['message']['content']
            command_data = json.loads(message_content)
            tool_to_use = command_data.get("tool")
            file_to_process = command_data.get("file_path")

            print("AI recommends using tool: {} on file: {}".format(tool_to_use, file_to_process))

            # 2. Execute the appropriate MCP Tool
            self.execute_mcp_tool(tool_to_use, file_to_process)

        except requests.exceptions.RequestException as e:
            print("Error calling API: {}".format(e))
        except (KeyError, IndexError, ValueError) as e:
            print("Error parsing AI response: {}".format(e))
            print("Raw response: " + response.text)
        
        self.ui.Close()

    def execute_mcp_tool(self, tool_name, file_path):
        """Finds and executes the specified MCP tool with the given file path."""
        if not tool_name or not file_path:
            print("Error: AI response did not specify a tool or file path.")
            return

        # Assumes the script is running from the .pushbutton directory
        # and navigates up to the repository root
        repo_root = os.path.abspath(os.path.join(script_dir, "..", "..", "..", ".."))
        
        # NOTE: You may need to change 'Debug' to 'Release' depending on your build configuration
        tool_exe_path = os.path.join(repo_root, "mcp_tools", tool_name, "bin", "Debug", tool_name + ".exe")

        if not os.path.exists(tool_exe_path):
            print("Error: Could not find MCP tool executable at: {}".format(tool_exe_path))
            print("Please ensure you have built the C# solution.")
            return

        print("--- Executing MCP Tool: {} ---".format(tool_name))
        try:
            # Use subprocess to call the C# tool
            process = subprocess.Popen([tool_exe_path, file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = process.communicate()
            
            if stdout:
                print("Tool Output:\n" + stdout.decode('utf-8'))
            if stderr:
                print("Tool Error:\n" + stderr.decode('utf-8'))
        except Exception as e:
            print("An error occurred while running the MCP tool: {}".format(e))

if __name__ == "__main__":
    xaml_file_path = os.path.join(script_dir, "ui.xaml")
    if os.path.exists(xaml_file_path):
        ui = MCP_UI(xaml_file_path)
        ui.ui.ShowDialog()
    else:
        print("Could not find ui.xaml. Please ensure it is in the same directory as script.py.") 