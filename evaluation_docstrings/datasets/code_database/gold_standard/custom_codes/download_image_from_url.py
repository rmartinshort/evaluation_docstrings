import shutil
import requests


def download_image_from_url(url, file_name):
    """

    :param url:
    :param file_name:
    :return:
    """
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(file_name, "wb") as f:
            shutil.copyfileobj(res.raw, f)
        print("Image sucessfully Downloaded: ", file_name)
    else:
        print("Image Couldn't be retrieved")
