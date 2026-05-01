import os.path
import random
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FOR_COMPLAINT_PICTURE = PROJECT_ROOT / 'tests' / 'tests_frontend' / 'pictures' / 'for_complaint.png'
DUMMY_IMAGE = PROJECT_ROOT / 'tests' / 'tests_frontend' / 'pictures' / 'dummy_image.png'
PROFILE_PICTURE = PROJECT_ROOT / 'tests' / 'tests_frontend' / 'pictures' / 'profile_picture.jpg'
COMPLAINT_FILE = PROJECT_ROOT / 'tests' / 'tests_frontend' / 'pictures' / 'complaint.pdf'
LARGE_PICTURE = PROJECT_ROOT / 'tests' / 'tests_frontend' / 'pictures' / 'large_profile_picture.jpg'
RECEIPT_PATH = PROJECT_ROOT / 'tests' / 'tests_frontend' / 'downloads' / f'receipt_{random.randint(1, 1000)}.pdf'
SENSITIVE_PATH = PROJECT_ROOT / '.private'

