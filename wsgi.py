# Set the path
import os
import sys


project_path = os.path.dirname(os.path.realpath(__file__))
if project_path not in sys.path:
    sys.path.append(project_path)

from application import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
