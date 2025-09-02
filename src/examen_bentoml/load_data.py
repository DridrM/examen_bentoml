import subprocess

from params import RAW_DATA_URL, RAW_DATA_PATH


try:
    # Create ouput path from raw data Path
    output_path = str(RAW_DATA_PATH / "admission.csv")
    
    # Curl command to execute
    command = ["curl", "-o", output_path, RAW_DATA_URL]
    
    # Execute in subprocess
    result = subprocess.run(command, check=True, capture_output=True, text=True)  # Capture output for debugging
    print(f"Curl command executed. Output: {result.stdout}") # Print Curl's output to help debug

# Catch exceptions
except subprocess.CalledProcessError as e:
    print(f"Error downloading file: {e}")
    print(f"Curl command error output: {e.stderr}") # Important: Print the error stream from curl

except Exception as e:
    print(f"An unexpected error occurred: {e}")