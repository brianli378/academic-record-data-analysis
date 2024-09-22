import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Screening Test: Perform data analysis and plotting on dataset of fake student records.
    # Shows the records of 50 CS students, spanning 6 quarters. For each quarter, we know its timestamp
    # (YYYYMM format where YYYY01 is Winter Quarter, YYYY03 is Spring Quarter, and YYYY08 is Fall Quarter),
    # the CS and overall GPA of the students, and the number of CS/overall units they were enrolled in.
    # Note that quarters are not always consecutive as students may sometimes take a leave of absence
    # (eg for an internship).

# SW Design
# Take in data which will be from the csv file
# Perform data analysis and plotting with numpy pandas and matplotlib
# Function Ideas
    # - read csv function
    # - Plot functions
        # - plot graph with gpa of all students 1-50, also displaying the average gpa. (command line argument to choose a specific quarter or across all quarters combined)
        # - plot graph with all students gpa vs cs credits (command line argument to choose a specific quarter or across all quarters combined)
        # - plot graph with all students gpa vs all credits including non-cs (command line argument to choose a specific quarter or across all quarters combined)
        # - plot graph with students gpa vs units taken (command line argument to choose a specific quarter or across all quarters combined)
        # - plot graph comparing gpa across different quarters

    # - CSV functions:
        # - use average gpa of all students combined and avg gpa of each student to classify each student into into groups of
            # - above average (4.0 < gpa < avggpa+0.5), average (avggpa+0.5 < gpa < avggpa-0.5), below average (gpa < avggpa-0.5)
        # - gpa trend of each student (going up or down)
        # - gpa consistency of each student (calculated using variance)
        # - how many quarters until graduation, calculated with the UC Davis average of 16 units/quarter
            # - as an extension for the function above, is the student on track to graduate or not (meeting avg 16 units/quarter or no)
        # - detect students with non-consecutive quarters and calculate avg gpa to see if breaks from academics affects gpa