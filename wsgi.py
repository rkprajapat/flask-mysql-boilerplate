# Set the path
import os
import sys
import traceback
from flask import render_template


sys.setrecursionlimit(10000)
project_path = os.path.dirname(os.path.realpath(__file__))
if project_path not in sys.path:
    sys.path.append(project_path)

from application import create_app
app = create_app()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('src/index.html')


if __name__ == "__main__":
    try:
        app.run(debug=True)

    except Exception as e:
        app.logger.error(e)
        # app.logger.error(traceback.format_exc())
