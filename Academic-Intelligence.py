import pandas as pd
from db_connection import get_connection 
import matplotlib.pyplot as plt
import seaborn as sns

  

def load_Students():
    conn = None
    try:
        df = pd.read_excel(r"C:\Users\aadis\OneDrive\Documents\Students.xlsx")
        conn = get_connection()
        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO Students (Name, Age, Course) VALUES (%s, %s, %s)",
                (row['Name'], row['Age'], row['Course'])
            )

        conn.commit()
        print("✅ Students data inserted")

    except Exception as e:
        print("❌ Students error:", e)

    finally:
        if conn:
         conn.close()


def load_Marks():
    conn = None
    try:
        df = pd.read_excel(r"C:\Users\aadis\OneDrive\Documents\Marks.xlsx")
        conn = get_connection()
        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO Marks (Student_ID, Subject, Marks, Semester) VALUES (%s, %s, %s, %s)",
                (row['Student_ID'], row['Subject'], row['Marks'], row['Semester'])
            )

        conn.commit()
        print("✅ Marks data inserted")

    except Exception as e:
        print("❌ Marks error:", e)

    finally:
        if conn:
         conn.close()



def load_Attendance():
    conn = None
    try:
        df = pd.read_excel(r"C:\Users\aadis\OneDrive\Documents\Attendance.xlsx")
        conn = get_connection()
        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO Attendance (Student_ID, Attendance_percentage, Semester) VALUES (%s, %s, %s)",
                (
                    int(row['Student_ID']),
                    float(row['Attendance_percentage']),
                    int(row['Semester'])
                )
            )

        conn.commit()
        print("✅ Attendance data inserted")

    except Exception as e:
        print("❌ Attendance error:", e)

    finally:
        if conn:
            conn.close()



def load_study_logs():
    conn = None
    try:
        df = pd.read_excel(r"C:\Users\aadis\OneDrive\Documents\Study_logs.xlsx")
        conn = get_connection()
        cursor = conn.cursor()

        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO Study_logs (Student_ID, Study_hours, Log_date) VALUES (%s, %s, %s)",
                (row['Student_ID'], row['Study_hours'], row['Log_date'])
            )

        conn.commit()
        print("✅ Study logs inserted")

    except Exception as e:
        print("❌ Study logs error:", e)

    finally:
        if conn:
         conn.close()



if __name__ == "__main__":
    load_Students()
    load_Marks()
    load_Attendance()
    load_study_logs()


def fetch_Students():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM Students",conn)
    conn.close()
    return df

def fetch_Marks():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM Marks",conn)
    conn.close()
    return df

def fetch_Attendance():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM Attendance",conn)
    conn.close()
    return df

def fetch_logs():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM Study_logs",conn)
    conn.close()
    return df



# ------------------- Subject Analysis ----------------------
def subject_wise_average():
    marks_df = fetch_Marks()
    return marks_df.groupby("Subject")["Marks"].mean().reset_index()

a = subject_wise_average()
print(a)

def student_wise_average():
    students_df = fetch_Marks()
    return students_df.groupby("Student_ID")["Marks"].mean()

b = student_wise_average()
print(b)


# ---------------------- Student Performance Summary ----------------
def student_performance_summary():
    marks_df = fetch_Marks()
    attendance_df = fetch_Attendance()
    study_logs_df = fetch_logs()

    avg_marks = marks_df.groupby("Student_ID")["Marks"].mean()
    avg_attendance = attendance_df.groupby("Student_ID")["Attendance_percentage"].mean()
    avg_study_hours = study_logs_df.groupby("Student_ID")["Study_hours"].mean()

   
    summary = pd.concat([avg_marks, avg_attendance, avg_study_hours],axis=1).reset_index()

    summary.columns = [
        "Student_ID",
        "Avg_marks",
        "Avg_attendance",
        "Avg_hours"
    ]

    return summary

c = student_performance_summary()
print(c)

# ------------------ Consistency Analysis --------------------
def consistency_analysis():
    study_df = fetch_logs()

    consistency = study_df.groupby("Student_ID")["Study_hours"].std().fillna(0)

    return consistency.reset_index(name="Consistency_score")

# ------------------ Final Performance Score -------------------------
def final_performance_score():
    summary = student_performance_summary()

    summary["Performance"] = (
        summary["Avg_marks"] * 0.6 +
        summary["Avg_attendance"] * 0.25 +
        summary["Avg_hours"] * 10 * 0.15
    )

    return summary[["Student_ID", "Performance"]]


e = final_performance_score()
print(e)

# --------------------- Risk Prediction -------------------
def risk_predictor(): 
    df = final_performance_score()

    def risk_level(score):
      if score >= 75 :
        return "safe"
      elif score >=50 and score < 75:
        return "Warning"
      else:
        return "critical"
    
    df["Risk_level"] = df["Performance"].apply(risk_level)
    return df
    

f = risk_predictor()
print(f)


# --------------------- Data Visualization ------------------- 
# 1. Performance Distribution Graph
def performance_distribution():
    df = final_performance_score()

    colour = sns.color_palette("Set2")[3]
    plt.hist(df["Performance"], bins = 5, color=colour, edgecolor = "Black", width=3,label = "Performance")
    plt.title("Performance Score Distribution")
    plt.xlabel("Score")
    plt.ylabel("Number of Students")
    sns.despine()
    plt.legend()
    plt.show()

# 2. Risk Level Count Graph
def risk_level_chart():
    df = risk_predictor()

    counts = df["Risk_Level"].value_counts()

    plt.figure()
    counts.plot(kind="bar")
    plt.title("Student Risk Levels")
    plt.xlabel("Risk Level")
    plt.ylabel("Number of Students")
    plt.show()

# 3. Attendance vs Marks Analysis
def attendance_vs_marks():
    marks_df = fetch_Marks()
    attendance_df = fetch_Attendance()

    avg_marks = marks_df.groupby("Student_ID")["Marks"].mean()
    avg_attendance = attendance_df.groupby("Student_ID")["Attendance_percentage"].mean()

    df = pd.concat([avg_marks, avg_attendance], axis=1)

    plt.figure()
    plt.scatter(df["Attendance_percentage"], df["Marks"])
    plt.xlabel("Attendance %")
    plt.ylabel("Average Marks")
    plt.title("Attendance vs Marks")
    plt.show()

