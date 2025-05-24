import os
import sys

# Ensure src directory is in sys.path for module resolution
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
