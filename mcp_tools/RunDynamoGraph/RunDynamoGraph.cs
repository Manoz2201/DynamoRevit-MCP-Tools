using System;

namespace MCP.Tools
{
    class RunDynamoGraph
    {
        static void Main(string[] args)
        {
            Console.WriteLine("MCP RunDynamoGraph Tool");

            if (args.Length == 0)
            {
                Console.WriteLine("Please provide the path to a .dyn file.");
                return;
            }

            var dynPath = args[0];
            Console.WriteLine($"Attempting to run: {dynPath}");

            // In the next step, we will add the logic 
            // to call the DynamoWPFCLI.exe with this path.
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
                process.StartInfo.Arguments = $"-o \"{dynPath}\"";
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

                Console.WriteLine("--- Execution Complete ---");

            }
            catch (Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
            }
        }
    }
} 