# labcourse_with_elabftw

This repository contains a collection of Python (JupyterNotebook) scripts for the script-based setup of eLabFTW for the use in lab courses (in physics).

## labcourse_setup_elabftw_eln.ipynb

This JupyterNotebook prepares a fresh team in eLabFTW for the lab course:
- Lab course experiments are defined in a yaml file.
- Templates can be defined in json files (export from an existing template in eLabFTW and modify ad lib).
- Student registrations and tutors are read from a csv file.

The JupyterNotebook does the following steps:
- Create all users (students and tutors) and assign student groups and a tutor group.
- Create categories and statuses in eLabFTW as defined in the yaml file.
- Create templates as defined in the yaml file (together with details from the json definition).
- Create all experiments according to the definition in the yaml file and assign user rights (read/write for the respective student group, read-only for the tutors)

## labcourse_preparation_excerpts.ipynb

This JupyterNotebook creates excerpts of the preparation documentation of the students. 

The preparation to the lab course experiments is documented in each related experiment.
This enables the students to have their preparation notes at hand when doing the experiment, data acquisition and data evaluation.
All notes, data and metadata related to one experiment is together at the same place.

This script summarizes the preparation work across all experiments of a student group into one document, which is displayed in the webbrowser. Figures, etc. are automatically included.
The excerpts help tutors to get a quick overview on the preparation status of the students without having to navigate through each and every experiment.
