#!/usr/bin/env python
"""Test the menu system."""

import sys
from sgns import main_menu, demo_sgns, demo_tfidf, demo_comparison

if __name__ == "__main__":
    # Simulate menu choice
    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = '3'  # Default to comparison
    
    print(f"Running demonstration {choice}...")
    print()
    
    if choice == '1':
        demo_sgns()
    elif choice == '2':
        demo_tfidf()
    elif choice == '3':
        demo_comparison()
    else:
        print(f"Unknown choice: {choice}")
