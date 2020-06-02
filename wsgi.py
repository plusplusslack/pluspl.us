import sys
import os

BASE_DIR = os.path.join(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

sys.path.append("/plusplus")

# give wsgi the "application"
from plusplus import create_app  # noqa: E402
application = create_app()
