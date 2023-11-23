import subprocess
import os
import time


def clone_repo():
    from git import Repo
    dirs = os.listdir(".")
    if "yolov5" not in dirs:
        Repo.clone_from("https://github.com/ultralytics/yolov5", "yolov5")


def init_s3_connection():
    import boto3
    key_id = os.environ.get("AWS_ACCESS_KEY_ID", "minio")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "minio123")
    endpoint = os.environ.get("AWS_S3_ENDPOINT", "http://minio-pipelines-definition.fedora-detection:9000")
    s3_client = boto3.client("s3", aws_access_key_id=key_id, aws_secret_access_key=secret_key, endpoint_url=endpoint)
    return s3_client


def get_last_exp():
    nb_exp = len(os.listdir("yolov5/runs/train"))
    if nb_exp == 1:
        return "exp"
    else:
        return f"exp{nb_exp}"


if __name__ == "__main__":
    print(os.environ)
    req = "pip install -r requirements.txt"
    subprocess.run(req.split())
    clone_repo()
    sed = "sed -i s/opencv-python/opencv-python-headless/ yolov5/requirements.txt"
    pip_install = "pip install -r yolov5/requirements.txt"
    pip_uninstall = "pip uninstall -qy opencv-python opencv-python-headless"
    pip_headless = "pip install -q opencv-python-headless"
    cmd = "python yolov5/train.py --data configuration.yaml --weights yolov5s.pt --epochs " + os.environ.get("nb_epochs", "1") + " --batch 16 --freeze 10 --cache disk"
    subprocess.run(sed.split())
    subprocess.run(pip_install.split())
    subprocess.run(pip_uninstall.split())
    subprocess.run(pip_headless.split())
    subprocess.run(cmd.split())
    exp = get_last_exp()
    #pip_uninstall = "pip uninstall -qy opencv-python opencv-python-headless"
    #pip_headless = "pip install -q opencv-python-headless"
    export = "python yolov5/export.py --weights yolov5/runs/train/" + exp + "/weights/best.pt --include onnx --imgsz 640 --opset 16"
    subprocess.run(export.split())
    model = "yolov5/runs/train/" + exp + "/weights/best.onnx"
    s3_path = "models/demos/fedora.onnx"
    s3_con = init_s3_connection()
    bucket_name = os.environ.get("AWS_S3_BUCKET", "fedora")
    tar = "tar -czf run.tar.gz yolov5/runs/train/"
    subprocess.run(tar.split())
    s3_con.upload_file(model, bucket_name, s3_path)