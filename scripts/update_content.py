#!/usr/bin/env python3
"""
Script to update all site content and push to GitHub
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from offnet.core import update_all_content

if __name__ == "__main__":
    print("Updating OffNet content...")
    update_all_content()
    print("Update complete!")
