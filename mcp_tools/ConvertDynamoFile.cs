using System;

namespace MCP.Tools
{
    class ConvertDynamoFile
    {
        static void Main(string[] args)
        {
            Console.WriteLine("MCP ConvertDynamoFile Tool");

            if (args.Length == 0)
            {
                Console.WriteLine("Please provide the path to the .dyn file to convert.");
                return;
            }

            var dynPath = args[0];
            Console.WriteLine($"Attempting to convert file: {dynPath}");

            try
            {
                var dynamoCLIPath = "DynamoForRevit/DynamoWPFCLI.exe";

                if (!System.IO.File.Exists(dynamoCLIPath))
                {
                    Console.WriteLine("Error: DynamoWPFCLI.exe not found.");
                    return;
                }

                var process = new System.Diagnostics.Process();
                process.StartInfo.FileName = dynamoCLIPath;
                // Use both -o and -x flags as required by the CLI
                process.StartInfo.Arguments = $"-o \"{dynPath}\" -x";
                process.StartInfo.UseShellExecute = false;
                process.StartInfo.RedirectStandardOutput = true;
                process.StartInfo.RedirectStandardError = true;
                process.Start();

                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();

                process.WaitForExit();

                Console.WriteLine("--- Dynamo Output ---");
                Console.WriteLine(output);

                if (!string.IsNullOrEmpty(error))
                {
                    Console.WriteLine("--- Dynamo Errors ---");
                    Console.WriteLine(error);
                }

                Console.WriteLine("--- Conversion Complete ---");

            }
            catch (Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
            }
        }
    }
} 