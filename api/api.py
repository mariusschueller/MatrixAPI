from flask import Flask
import subprocess
import os


app = Flask(__name__)

def checkSTL(file):
    if file.endswith(".stl"):
        return True
    return False

@app.route('/')
def home():
    result = subprocess.run(
        [
            "/home/marius/Documents/MATRIX/superslicer/superslicer",
            "-g",
            "/home/marius/Documents/MATRIX/test_files/TRUMPETSTENCIL.stl"
        ],
        capture_output=True,
        text=True
    )
    output = result.stdout.split("\n")
    error = result.stderr
    return output

@app.route('/file/<filename>')
def file(filename):
    if checkSTL(filename):
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
    else:
        return "Invalid file format", 400

if __name__ == '__main__':
    app.run(debug=True)