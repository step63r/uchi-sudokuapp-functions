import json
import urllib.parse
import urllib.request

FILE_PATH = r"C:\Users\step6\Desktop\Workspace\TestSudokuImage.png"
URL = "http://localhost:7071/api/DetectSudokuFrame"

with open(FILE_PATH, "rb") as f:
    img = f.read()

if not img:
    raise ValueError("read error")

req = urllib.request.Request(
    URL,
    img,
    method="POST",
    headers={"Content-Type": "applicaiton/octet-stream"},
)

with urllib.request.urlopen(req) as res:
    objJson = json.loads(res.read())

if objJson:
    with open("out.json", "w") as f:
        json.dump(objJson, f, indent=4)
    print("Success!!")
else:
    print("Failed...")
