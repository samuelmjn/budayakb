from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

DEFAULT_TAG = "tp4"

def upload_file(filename: str):
    res = upload(filename, tags=DEFAULT_TAG)
    url, _ = cloudinary_url(res['public_id'], format=res['format'])
    return url