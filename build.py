from main import WORKING_DIR
from platform import system
import os

STATIC_FOLDER = f"{WORKING_DIR}/src/static"
TEMPLATE_FOLDER = f"{WORKING_DIR}/src/templates"

DIST_FOLDER_NAME = "erapor_release"
DIST_DEST = f"{WORKING_DIR}/../{DIST_FOLDER_NAME}"

# RUN BUILD COMMAND
try:
    # development build
    if system() == "Linux":
        add_data = [
            f'--add-data "{STATIC_FOLDER}:src/testing_modules"',
            f'--add-data "{STATIC_FOLDER}:src/modules"',
            f'--add-data "{STATIC_FOLDER}:src/static"',
            f'--add-data "{TEMPLATE_FOLDER}:src/templates"',
        ]
        os.system(
            f"pyinstaller --noconfirm --onedir --console {' '.join(add_data)} main.py --distpath {DIST_DEST}"
        )
    elif system() == "Windows":
        add_data = [
            f'--add-data "{STATIC_FOLDER};src/testing_modules"',
            f'--add-data "{STATIC_FOLDER};src/modules"',
            f'--add-data "{STATIC_FOLDER};src/static"',
            f'--add-data "{TEMPLATE_FOLDER};src/templates"',
        ]
        os.system(
            f"pyinstaller --noconfirm --onedir --console {' '.join(add_data)} main.py --distpath {DIST_DEST}"
        )
    else:
        NotImplementedError("OS other than windows and linux are not supported.")
except Exception as e:
    print("Something went wrong. ", e)
    exit()
