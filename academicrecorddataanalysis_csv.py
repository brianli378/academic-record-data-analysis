import numpy as np
import pandas as pd
# - CSV functions:
    # - use average gpa of all students combined and avg gpa of each student to classify each student into into groups of
        # - above average (4.0 < gpa < avggpa+0.1), average (avggpa+0.1 < gpa < avggpa-0.1), below average (gpa < avggpa-0.1)
    # - gpa trend of each student (going up or down)
    # - gpa consistency of each student (calculated using variance)
    # - how many quarters until graduation, calculated with the UC Davis average of 16 units/quarter
    # - as an extension for the function above, is the student on track to graduate or not (meeting avg 16 units/quarter or no)
    # - detect students with non-consecutive quarters and calculate avg gpa to see if breaks from academics affects gpa


def load_csv(csv_filename):
    csv_data = pd.read_csv(csv_filename)
    return csv_data

def group_students_by_gpa(csv_data):
    avg_gpa_all_students = csv_data[[f'Q{i}_Overall_GPA' for i in range(1, 6)]].mean().mean()
    gpa_groups = []
    for _, row in csv_data.iterrows():
        student_avg_gpa = round(row[[f'Q{i}_Overall_GPA' for i in range(1, 6)]].mean(), 2)

        if student_avg_gpa > avg_gpa_all_students + 0.1:
            group = 'Above Average'
        elif avg_gpa_all_students - 0.1 <= student_avg_gpa <= avg_gpa_all_students + 0.1:
            group = 'Average'
        else:
            group = 'Below Average'

        gpa_groups.append({
            'StudentID': row['StudentID'],
            'Average GPA': student_avg_gpa,
            'Group': group
        })

    df_gpa_groups = pd.DataFrame(gpa_groups)
    return df_gpa_groups[['StudentID', 'Average GPA', 'Group']]


def gpa_trend(csv_data):
    trends = []

    for _, row in csv_data.iterrows():
        gpas = row[[f'Q{i}_Overall_GPA' for i in range(1, 6)]].dropna().values


        differences = np.diff(gpas)
        if np.all(differences > 0):
            trend = 'Increasing'
        elif np.all(differences < 0):
            trend = 'Decreasing'
        else:
            trend = 'Both'

        trends.append({
            'StudentID': row['StudentID'],
            'GPA Trend': trend
        })

    df_trends = pd.DataFrame(trends)
    return df_trends[['StudentID', 'GPA Trend']]


def gpa_variance(csv_data):
    variance_data = []

    for _, row in csv_data.iterrows():
        gpas = row[[f'Q{i}_Overall_GPA' for i in range(1, 6)]].dropna().values

        variance = round(np.var(gpas), 2)

        variance_data.append({
            'StudentID': row['StudentID'],
            'GPA Variance': variance
        })

    df_variance = pd.DataFrame(variance_data)
    return df_variance[['StudentID', 'GPA Variance']]


def quarters_until_graduation(csv_data, required_units=180, avg_units_per_quarter=16):
    quarters_left = []

    for _, row in csv_data.iterrows():
        total_units_taken = row[[f'Q{i}_Total_Units' for i in range(1, 6)]].sum()
        remaining_units = required_units - total_units_taken
        remaining_quarters = np.ceil(remaining_units / avg_units_per_quarter)

        quarters_left.append({
            'StudentID': row['StudentID'],
            'Quarters Until Graduation': int(remaining_quarters)
        })

    df_quarters_left = pd.DataFrame(quarters_left)
    return df_quarters_left[['StudentID', 'Quarters Until Graduation']]


def graduation_on_track(csv_data, rec_units_per_quarter=16):
    on_track = []
    for _, row in csv_data.iterrows():
        total_units_taken = row[[f'Q{i}_Total_Units' for i in range(1, 6)]].sum()
        quarters_taken = row[[f'Q{i}_Total_Units' for i in range(1, 6)]].count()

        avg_units = total_units_taken / quarters_taken
        track_status = 'On Track' if avg_units >= rec_units_per_quarter else 'Not On Track'

        on_track.append({
            'StudentID': row['StudentID'],
            'Graduation on Track?': track_status
        })

    df_on_track = pd.DataFrame(on_track)
    return df_on_track[['StudentID', 'Graduation on Track?']]


def detect_breaks_analyze_gpa(csv_data):
    break_info = []
    for _, row in csv_data.iterrows():
        timestamps = row[[f'Q{i}_Timestamp' for i in range(1, 6)]].dropna().astype(str).values
        gpas = row[[f'Q{i}_Overall_GPA' for i in range(1, 6)]].dropna().values
        has_break = False
        gpa_before_break, gpa_after_break = None, None

        for i in range(len(timestamps) - 1):
            current_quarter = int(timestamps[i][4:6])
            next_quarter = int(timestamps[i + 1][4:6])
            if not is_consecutive_quarter(current_quarter, next_quarter):
                has_break = True
                gpa_before_break = gpas[i]
                gpa_after_break = gpas[i + 1]
                break

        if has_break and gpa_before_break is not None and gpa_after_break is not None:
            gpa_change = round(gpa_after_break - gpa_before_break, 2)
        else:
            gpa_before_break = gpa_after_break = gpa_change = 'N/A'

        break_info.append({
            'StudentID': row['StudentID'],
            'Had Break': 'Yes' if has_break else 'No',
            'GPA Pre-Break': gpa_before_break,
            'GPA Post-Break': gpa_after_break,
            'GPA Change': gpa_change
        })

    return pd.DataFrame(break_info)[['StudentID', 'Had Break', 'GPA Pre-Break', 'GPA Post-Break', 'GPA Change']]

def is_consecutive_quarter(current_quarter, next_quarter):
    quarter_order = [1, 3, 8]
    current = quarter_order.index(current_quarter)
    next = quarter_order.index(next_quarter)
    return (next - current == 1) or (current == 2 and next == 0)

def write_to_csv(csv_data, output_csv_file):
    df_gpa_class = group_students_by_gpa(csv_data)
    df_gpa_trend = gpa_trend(csv_data)
    df_gpa_variance = gpa_variance(csv_data)
    df_quarters_left = quarters_until_graduation(csv_data)
    df_on_track = graduation_on_track(csv_data)
    df_breaks = detect_breaks_analyze_gpa(csv_data)

    merged_data = pd.merge(csv_data[['StudentID']], df_gpa_class, on='StudentID')
    merged_data = pd.merge(merged_data, df_gpa_trend, on='StudentID')
    merged_data = pd.merge(merged_data, df_gpa_variance, on='StudentID')
    merged_data = pd.merge(merged_data, df_quarters_left, on='StudentID')
    merged_data = pd.merge(merged_data, df_on_track, on='StudentID')
    merged_data = pd.merge(merged_data, df_breaks, on='StudentID')
    merged_data.to_csv(output_csv_file, index=False)


def main():
    input_csv = 'fake_student_records.csv'
    output_csv = 'csv_analysis.csv'
    csv_data = load_csv(input_csv)
    write_to_csv(csv_data, output_csv)


if __name__ == '__main__':
    main()