FileOrganizer

Overview

FileOrganizer was created to solve the problem of disorganized files and simplify file management. 
It automatically sorts files into categories, 
helping users keep their folders organized and making files easier to find.

Features

- SHA-256 hashing — calculates file hashes to identify duplicate files.
- Dry-run mode — previews file movements without actually moving files.
- Undo functionality — allows users to reverse the sorting operation.

Installation

To use FileOrganizer, you need to install Python and the PyInputPlus library.

pip install pyinputplus

Usage

First, enter the path to the folder you want to organize. 
The program will then create necessary log and history files to track file movements. 
If a file cannot be moved, the program will display its name and path.

Dry-run

To perform a test run, add the "--dry-run" argument when running the program. 
You will receive a preview of the planned file movements without actually moving any files.

Undo

To undo file movements, run the "UNDO.py" script. 
It will attempt to return all previously moved files to their original directories.

Note

We apologize in advance for any errors or issues you may encounter. Thank you for your understanding!
