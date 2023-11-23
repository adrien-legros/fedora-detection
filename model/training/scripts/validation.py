import subprocess
import os
import tarfile

def clone_repo():
    from git import Repo
    dirs = os.listdir(".")
    if "yolov5" not in dirs:
        Repo.clone_from("https://github.com/ultralytics/yolov5", "yolov5")

def get_last_exp():
    nb_exp = len(os.listdir("yolov5/runs/train"))
    if nb_exp == 1:
        return "exp"
    else:
        return f"exp{nb_exp}"


if __name__ == "__main__":
    req = "pip install -r requirements.txt"
    subprocess.run(req.split())
    clone_repo()
    tar = tarfile.open("run.tar.gz")
    tar.extractall()
    tar.close()
    pip_uninstall = "pip uninstall -qy opencv-python opencv-python-headless"
    pip_install = "pip install -r yolov5/requirements.txt"
    pip_headless = "pip install -q opencv-python-headless"
    subprocess.run(pip_install.split())
    subprocess.run(pip_uninstall.split())
    subprocess.run(pip_headless.split())
    exp = get_last_exp()
    cmd = "python yolov5/val.py --task test --save-txt --data configuration.yaml --weights yolov5/runs/train/" + exp + "/weights/best.pt"
    subprocess.run(cmd.split())