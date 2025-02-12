from flask import Flask
import subprocess
import os


app = Flask(__name__)

# Check if the file ends with .stl
def checkSTL(file):
    if file.endswith(".stl"):
        return True
    return False

# change colons to spaces 
def convertOptions(options):
    return options.replace(":", " ").replace(",", " ")

# default call (doesn't allow for dynamic file specification so don't use)
# @app.route('/')
# def home():
#     result = subprocess.run(
#         [
#             "/home/marius/Documents/MATRIX/superslicer/superslicer",
#             "-g",
#             "/home/marius/Documents/MATRIX/test_files/TRUMPETSTENCIL.stl"
#         ],
#         capture_output=True,
#         text=True
#     )
#     output = result.stdout.split("\n")
#     error = result.stderr
#     return output


# This one does use dynamic file specification so plz use
@app.route('/file/<filename>')
def file(filename):
    if not checkSTL(filename):
        return "Invalid file format", 400

    file_path = f"/home/marius/Documents/MATRIX/test_files/{filename}"
    if not os.path.exists(file_path):
        return f"File {filename} does not exist", 404
    
    result = subprocess.run(
        [
            "/home/marius/Documents/MATRIX/superslicer/superslicer",
            "-g",
            f"/home/marius/Documents/MATRIX/test_files/{filename}"
        ],
        capture_output=True,
        text=True
    )
    output = result.stdout.split("\n")
    error = result.stderr
    return output
    

@app.route('/fileOptions/<file>/<options>')
def fileAndOption(file, options):
    if not checkSTL(file):
        return "Invalid file format", 400

    file_path = f"/home/marius/Documents/MATRIX/test_files/{file}"
    if not os.path.exists(file_path):
        return f"File {file} does not exist", 404


    # Now we orient it
    sub = [
    "python3",
    "/home/marius/Documents/MATRIX/Tweaker-3/Tweaker.py",
    "-i",
    file_path,
    "-vb"
    ]

    print("Executing:", sub)
    
    result = subprocess.run(
        sub,
        capture_output=True,
        text=True
    )
    file_path = file_path.replace(".stl", "_tweaked.stl")

    # Now the file should be well oriented

    # Suppose options is "--layer-height 0.2"
    # Manually split it into a list:
    options_list = options.split()  
    print(options_list)
    sub = [
        "/home/marius/Documents/MATRIX/superslicer/superslicer",  # Adjusted path, remove the dot at the beginning if not needed
        "-g",
        file_path
    ] + options_list

    print("Executing:", sub)
    
    result = subprocess.run(
        sub,
        capture_output=True,
        text=True
    )
    
    output = result.stdout.split("\n")
    error = result.stderr
    return error
    



if __name__ == '__main__':
    app.run(debug=True)