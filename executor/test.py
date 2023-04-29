import os

cs_file = 'problem.exe'
os.chmod(cs_file, 0o755)  # add executable permissions to the file

# Run the compiled program and capture its output
output = os.popen('./problem.exe').read()

print(output)