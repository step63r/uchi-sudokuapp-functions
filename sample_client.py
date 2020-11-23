import json
import urllib.parse
import urllib.request


URL = "http://localhost:7071/api/DetectSudokuFrame"
IMAGE_PATH = r"C:\Users\step6\Desktop\Workspace\TestSudokuImage.png"

with open(IMAGE_PATH, "rb") as f:
    reqbody = f.read()

req = urllib.request(
    url,
    reqbody,
    method="POST",
    headers={
        "Content-Type": "application/octet-stream"
    }
)
