from flask import Flask
import subprocess


app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)