from main import WORKING_DIR
import os

STATIC_FOLDER = f"{WORKING_DIR}/src/static"
TEMPLATE_FOLDER = f"{WORKING_DIR}/src/templates"

DIST_FOLDER_NAME = "erapor_release"
DIST_DEST = f"{WORKING_DIR}../../{DIST_FOLDER_NAME}"

# RUN BUILD COMMAND
try:
    # development build
    os.system(
        f'pyinstaller --onefile --add-data "{STATIC_FOLDER}:src/testing_modules" --add-data "{STATIC_FOLDER}:src/modules" --add-data "{STATIC_FOLDER}:src/static" --add-data "{TEMPLATE_FOLDER}:src/templates" main.py --distpath {DIST_DEST}'
    )
except Exception:
    print("Something went wrong.")
    exit()
