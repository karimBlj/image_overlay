from jinja2 import Template
from selenium import webdriver
import firebase_admin
from firebase_admin import credentials, storage
import numpy as np
from html2image import Html2Image
from typing import List, Tuple, Dict
import json
import time
import pandas as pd
from glob import glob

cred = credentials.Certificate('/Users/karim/Documents/Sideral/Outreach/automation/ImageMarketing/serviceAccount.json')  # Path to your service account key
firebase_admin.initialize_app(cred, {
    'storageBucket': 'sideral-a95c0.appspot.com'  # Replace with your storage bucket URL
})


Point = Tuple[int, int]

def get_closest_point_index(points : List[Point], new_point : Point) -> int:
    dist_list = []
    np_new_point = np.array(new_point)
    for point in points:
        dist = np.linalg.norm(np.array(point) - np_new_point)
        dist_list.append(dist)
    closes_point_index = np.array(dist_list).argmin()
    return closes_point_index

def sort_pts(points : List[Point]) -> List[Point]:
    sorted_pts = np.zeros((4, 2), dtype="int32")
    s = np.sum(points, axis=1)
    sorted_pts[0] = points[np.argmin(s)]
    sorted_pts[2] = points[np.argmax(s)]

    diff = np.diff(points, axis=1)
    sorted_pts[1] = points[np.argmin(diff)]
    sorted_pts[3] = points[np.argmax(diff)]
    return sorted_pts

def screen_web_page(website_url : str, dest_img : str) -> None:
    # hti = Html2Image(size=(1520, 880))
    # hti.screenshot(url=website_url, save_as=dest_img)
    driver = webdriver.Safari()
    driver.set_window_size(1520, 880)
    driver.get(website_url)
    time.sleep(3)
    driver.save_screenshot(dest_img)
    driver.quit()


def upload_image(image_path : str, storage_path : str) -> str:
    bucket = storage.bucket()
    blob = bucket.blob(storage_path)
    blob.upload_from_filename(image_path)
    blob.make_public()  # Make the file publicly accessible
    return blob.public_url

def read_json_file(file_path : str) -> Dict:
    f = open(file_path)
    data = json.load(f)
    f.close()
    return data

def load_email_content(
    file_path    : str,
    **kwargs
) -> str:
    with open(file_path, 'r') as file:
        email_template = file.read()
    template = Template(email_template)
    email = template.render(**kwargs)
    return email

def load_history_campaigns():
    result = pd.DataFrame({})
    folders = glob("./campaigns/*")
    for folder in folders:
        try:
            folder_hist = pd.read_csv(folder + "/report.csv", sep="|")
            result  = pd.concat([result, folder_hist])
        except Exception:
            pass
    return result