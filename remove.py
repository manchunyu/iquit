import os
import shutil

if os.path.isdir("./flask_session"):
    shutil.rmtree("./flask_session")
if os.path.isdir("./__pycache__"):
    shutil.rmtree("./__pycache__")