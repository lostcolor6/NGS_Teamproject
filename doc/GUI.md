# Graphical User Interface

**NGS PyQt Application**
==========================

Welcome to the NGS PyQt Application, a tool for working with Variant Call Format (VCF) files. This application provides a user-friendly interface for loading, filtering, and analyzing VCF data.

**Getting Started**
---------------
To get started with the application, simply open a VCF or CSV file using the "File" menu. The application will load the data into a table, where you can customize the columns, filter the data, and perform various actions.

**Basic Usage**
-------------

### Table

The table displays the data loaded from the VCF file. Each row represents a single variant, and the columns display various attributes of the variant. You can customize the table by:

* Right-clicking to show or hide columns, drag them around, and resize them.
* Left-clicking a header column to sort by ascending or descending order.
* Left-clicking a vertical header to display certain information about that entry on the bottom right of the GUI.

### Filtering

The filtering options allow you to narrow down the variants displayed in the table based on various criteria. You can:

* Choose to hide certain filter categories.
* Use the Apply Default Filter button to reset the filters to a default value based on user settings/ini file.
* Use the Annotate Variant button to annotate a entry.
* Enter a Profile Name and Notes below that also get saved to the ini file.
* Save and Load the filter settings using the buttons at the end of the Filter Section.

### Toolbar

The toolbar is draggable to either side or bottom/top. You can use the following functions:

* Quicksave: Save the current visible table.
* Refresh: Reload the table and make all columns visible again.
* Show Raw Data: Open a window where all of the VCF as a raw text format gets loaded up (this takes long for big VCF files).
* Show Lookup Table: Open up a search query for you to lookup meaning of certain headers and their type.

### Taskbar

The taskbar provides access to various functions:

* On File:
    + Open a VCF (Variant Call Format) or CSV (Comma Separated Value) file into the table.
    + Save in the file formats: CSV, TXT, JSON, and HTML.
    + Exit: Close the application.
* On Help:
    + Find the repositories of this project as well as further documentation.
* On Settings:
    + See the current information about connections such as APIs.
    + Select a dark theme for less eye strain.
    + In the Quality Settings:
        - Choose max/min quality values to get saved into the ini file.
        - Set the respective Spinbox ranges for the filters.
        - Set a quality cutoff so only entries over a certain value get displayed initially.
    + All of these settings get saved in the gui.ini file.

### General

On the bottom left, your opened VCF header gets displayed for easy access and lookup.

**Setup**
--------------

Download the latest version for Windows
Download Python 3.12.3
under https://www.python.org/downloads/

- paste and run in command prompt:
  "pip install PyQt5" (https://pypi.org/project/PyQt5/)


(It seems like the pip command is not recognized in your command prompt?
This typically happens when Python is not added to your system's PATH environment variable during installation.

To fix this issue, you can follow these steps:

- Find the Path to Python Scripts:
  First, find out where Python is installed on your system. You can usually find it in C:\PythonXX (where XX is the version number) or C:\Users\<YourUsername>\AppData\Local\Programs\Python\PythonXX.
- Look for the Scripts directory within the Python installation directory. This directory contains the pip executable.
- Add Python Scripts to PATH:
1) Copy the path to the Scripts directory.
2) Open the Control Panel and search for "environment variables".
3) Click on "Edit the system environment variables".
4) In the System Properties window, click on the "Environment Variables..." button.
5) In the Environment Variables window, under "System variables", find the "Path" variable and select it. Then click "Edit...".
6) Click "New" and paste the path to the Scripts directory.
7) Click "OK" on all windows to save your changes.
8) Restart Your Command Prompt:
   Close and reopen your command prompt. Now, the pip command should be recognized.)






