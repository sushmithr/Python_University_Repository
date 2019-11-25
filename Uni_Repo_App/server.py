"""
    Testing Flask Installation
"""

import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/instructors')
def instructors_summary():
    dbpath = r'C:\Sushmith Ramesh\SSW_810_Python\Py_Uni_Repo_Proj\Python_University_Repository\Uni_Repo_App\810_startup.db'

    try:
        db = sqlite3.connect(dbpath)
    except sqlite3.OperationalError:
        return f"Error: Unable to open database at {dbpath}"
    else:
        query = """ SELECT I.CWID, I.Name, I.Dept, G.Course, count(G.StudentCWID) Students
                    FROM instructors I
                    JOIN grades G on I.CWID = G.InstructorCWID
                    GROUP BY I.CWID, I.Name, I.Dept, G.Course """

        data = [{'cwid': CWID, 'name': Name, 'dept': Dept, 'course': Course, 'students': Students}
                for CWID, Name, Dept, Course, Students in db.execute(query)]

        db.close()

    return render_template(
                    'instructor_info.html', 
                    title="University Manager",
                    page_header="Stevens Repository", 
                    table_title="Courses and student counts",
                    instructors=data)

app.run(debug=True)
