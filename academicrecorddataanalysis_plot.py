import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse

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
        # - plot graph comparing gpa across different quarters

# Plot function naming convention: plot_target_xaxis_yaxis


def load_csv(csv_filename):
    csv_data = pd.read_csv(csv_filename)
    return csv_data

def get_quarter_data(csv_data, quarter, data_type='Overall_GPA'):
    quarter_map = {
        'WQ': '01',
        'SQ': '03',
        'FQ': '08'
    }

    quarter_month = quarter_map.get(quarter)

    data_list = []
    for i in range(1, 6):
        timestamp_col = f'Q{i}_Timestamp'
        data_col = f'Q{i}_{data_type}'

        if timestamp_col in csv_data.columns and data_col in csv_data.columns:
            matching_rows = csv_data[timestamp_col].astype(str).str[4:6] == quarter_month
            data_list.append(csv_data.loc[matching_rows, data_col].values)

    return np.concatenate(data_list)

def get_all_quarters_data(csv_data, data_type='Overall_GPA'):
    all_data = []
    for i in range(1, 6):
        data_col = f'Q{i}_{data_type}'
        if data_col in csv_data.columns:
            all_data.append(csv_data[data_col].dropna().values)

    return np.concatenate(all_data)


def plot_all_student_gpa(csv_data, quarter=None):
    if quarter:
        gpa = get_quarter_data(csv_data, quarter, data_type='Overall_GPA')
    else:
        gpa = get_all_quarters_data(csv_data, data_type='Overall_GPA')

    avg_gpa = np.mean(gpa)

    plt.plot(gpa, label="Student GPA")
    plt.axhline(y=avg_gpa, color='r', linestyle='--', label=f"Average GPA: {avg_gpa:.2f}")
    plt.title(f'All Students GPA {"(Quarter " + str(quarter) + ")" if quarter else "(All Quarters)"}')
    plt.xlabel('Student')
    plt.ylabel('GPA')
    plt.legend()
    filename = f'all_student_gpa_{quarter if quarter else "all_quarters"}.png'
    plt.savefig(filename)
    plt.close()


def plot_all_gpa_cscredits(csv_data, quarter=None):
    if quarter:
        gpa = get_quarter_data(csv_data, quarter, data_type='Overall_GPA')
        cs_credits = get_quarter_data(csv_data, quarter, data_type='CS_Units')
    else:
        gpa = get_all_quarters_data(csv_data, data_type='Overall_GPA')
        cs_credits = get_all_quarters_data(csv_data, data_type='CS_Units')

    plt.scatter(cs_credits, gpa)
    plt.title(f'GPA vs CS Credits {"(Quarter " + str(quarter) + ")" if quarter else "(All Quarters)"}')
    plt.xlabel('CS Credits')
    plt.ylabel('GPA')
    filename = f'gpa_vs_cs_credits_{quarter if quarter else "all_quarters"}.png'
    plt.savefig(filename)
    plt.close()

def plot_all_gpa_allcredits(csv_data, quarter=None):
    if quarter:
        gpa = get_quarter_data(csv_data, quarter, data_type='Overall_GPA')
        total_credits = get_quarter_data(csv_data, quarter, data_type='Total_Units')
    else:
        gpa = get_all_quarters_data(csv_data, data_type='Overall_GPA')
        total_credits = get_all_quarters_data(csv_data, data_type='Total_Units')

    plt.scatter(total_credits, gpa)
    plt.title(f'GPA vs All Credits {"(Quarter " + str(quarter) + ")" if quarter else "(All Quarters)"}')
    plt.xlabel('Total Credits')
    plt.ylabel('GPA')
    filename = f'gpa_vs_all_credits_{quarter if quarter else "all_quarters"}.png'
    plt.savefig(filename)
    plt.close()

def plot_avggpa_allquarters(csv_data):
    quarter_map = {
        '01': 'WQ',
        '03': 'SQ',
        '08': 'FQ'
    }

    results = {}

    for i in range(1, 6):
        timestamp_col = f'Q{i}_Timestamp'
        gpa_col = f'Q{i}_Overall_GPA'

        if timestamp_col in csv_data.columns and gpa_col in csv_data.columns:
            csv_data[timestamp_col] = csv_data[timestamp_col].astype(str)
            filtered_data = csv_data[csv_data[timestamp_col].str.len() == 6]
            filtered_data = filtered_data[filtered_data[timestamp_col].str[4:6].isin(quarter_map.keys())]

            for index, row in filtered_data.iterrows():
                year = row[timestamp_col][:4]
                quarter_code = row[timestamp_col][4:6]
                quarter_key = f"{year}{quarter_map[quarter_code]}"
                if quarter_key not in results:
                    results[quarter_key] = []
                results[quarter_key].append(row[gpa_col])

    average_gpas = {key: np.mean(values) for key, values in results.items() if values}


    sorted_quarters = sorted(average_gpas.items())

    timestamps, gpas = zip(*sorted_quarters) if sorted_quarters else ([], [])

    # Plot
    plt.figure(figsize=(10, 5))
    if timestamps:
        plt.plot(timestamps, gpas, marker='o')
        plt.title('Average GPA Over Time')
        plt.xlabel('Time (YearQuarter)')
        plt.ylabel('Average GPA')
        plt.xticks(rotation=33)
        plt.grid(True)
    else:
        plt.text(0.5, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center')
    filename = 'Output/gpa_average_over_time.png'
    plt.savefig(filename)
    plt.close()



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file', type=str)
    parser.add_argument('--quarter', type=str)
    parser.add_argument('--plot', type=str)

    args = parser.parse_args()

    csv_data = load_csv(args.csv_file)

    if args.plot == 'gpa_vs_cs_credits':
        plot_all_gpa_cscredits(csv_data, quarter=args.quarter)
    elif args.plot == 'gpa_vs_all_credits':
        plot_all_gpa_allcredits(csv_data, quarter=args.quarter)
    elif args.plot == 'gpa_average_allquarters':
        plot_avggpa_allquarters(csv_data)
    else:
        plot_all_student_gpa(csv_data, quarter=args.quarter)

if __name__ == '__main__':
    main()