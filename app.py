
import streamlit as st # type: ignore
import pandas as pd # type: ignore
import uuid
import bcrypt # type: ignore
from datetime import datetime
import altair as alt # type: ignore
from pymongo import MongoClient # type: ignore

# Setup page configuration
st.set_page_config(
    page_title="University Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Secret Codes for registration
ADMIN_SECRET = "admin123"
TEACHER_SECRET = "teacher123"

# MongoDB Atlas Connection
def connect_to_mongodb():
    # Replace with your MongoDB Atlas connection string
    connection_string = "mongodb+srv://armeennadeem9:aDHenfVw3sI0gjua@cluster0.fqdwzwn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    # You can also use environment variables for the connection string
    # connection_string = os.environ.get("MONGODB_URI")
    
    try:
        client = MongoClient(connection_string)
        # Test the connection
        client.admin.command('ping')
        db = client.university  # database name
        return db
    except Exception as e:
        st.error(f"Failed to connect to MongoDB: {e}")
        return None

# Initialize MongoDB connection
db = connect_to_mongodb()

# Password hashing functions
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(stored_hash, password):
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

# Create default admin if not exists
def create_default_admin():
    if db.users.count_documents({"role": "Admin"}) == 0:
        admin_id = str(uuid.uuid4())
        hashed_password = hash_password("admin123")
        db.users.insert_one({
            "id": admin_id,
            "username": "admin",
            "password": hashed_password,
            "role": "Admin",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

# Add some sample data if collections are empty
def add_sample_data():
    # Check if departments collection is empty
    if db.departments.count_documents({}) == 0:
        # Add sample departments
        departments = [
            {"id": str(uuid.uuid4()), "name": "Computer Science"},
            {"id": str(uuid.uuid4()), "name": "Mathematics"},
            {"id": str(uuid.uuid4()), "name": "Physics"}
        ]
        db.departments.insert_many(departments)
        
        # Get department IDs for reference
        dept_ids = {dept["name"]: dept["id"] for dept in db.departments.find()}
        
        # Add sample persons who are instructors
        instructors = [
            {
                "id": str(uuid.uuid4()),
                "name": "Dr. John Smith",
                "age": 45,
                "email": "john.smith@university.edu",
                "type": "instructor"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Dr. Jane Doe",
                "age": 38,
                "email": "jane.doe@university.edu",
                "type": "instructor"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Prof. Robert Johnson",
                "age": 55,
                "email": "robert.johnson@university.edu",
                "type": "instructor"
            }
        ]
        db.persons.insert_many(instructors)
        
        # Get instructor IDs for reference
        instructor_ids = []
        for instructor in instructors:
            instructor_ids.append(instructor["id"])
        
        # Add instructor details
        instructor_details = [
            {
                "id": instructor_ids[0],
                "salary": 85000,
                "department_id": dept_ids["Computer Science"],
                "position": "Associate Professor"
            },
            {
                "id": instructor_ids[1],
                "salary": 78000,
                "department_id": dept_ids["Mathematics"],
                "position": "Assistant Professor"
            },
            {
                "id": instructor_ids[2],
                "salary": 95000,
                "department_id": dept_ids["Physics"],
                "position": "Professor"
            }
        ]
        db.instructors.insert_many(instructor_details)
        
        # Add sample courses
        courses = [
            {
                "id": str(uuid.uuid4()),
                "code": "CS101",
                "name": "Introduction to Programming",
                "department_id": dept_ids["Computer Science"],
                "instructor_id": instructor_ids[0],
                "credits": 3,
                "description": "Basic programming concepts using Python",
                "schedule": "Mon/Wed 10:00 AM",
                "classroom": "Room 101"
            },
            {
                "id": str(uuid.uuid4()),
                "code": "MATH101",
                "name": "Calculus I",
                "department_id": dept_ids["Mathematics"],
                "instructor_id": instructor_ids[1],
                "credits": 4,
                "description": "Limits, derivatives, and integrals",
                "schedule": "Tue/Thu 9:00 AM",
                "classroom": "Room 202"
            },
            {
                "id": str(uuid.uuid4()),
                "code": "PHYS101",
                "name": "Classical Mechanics",
                "department_id": dept_ids["Physics"],
                "instructor_id": instructor_ids[2],
                "credits": 4,
                "description": "Newton's laws and classical physics principles",
                "schedule": "Mon/Fri 2:00 PM",
                "classroom": "Room 303"
            }
        ]
        db.courses.insert_many(courses)
        
        # Get course IDs for reference
        course_ids = [course["id"] for course in db.courses.find()]
        
        # Add sample students
        students = [
            {
                "id": str(uuid.uuid4()),
                "name": "Alice Johnson",
                "age": 20,
                "email": "alice.johnson@university.edu",
                "type": "student"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Bob Williams",
                "age": 21,
                "email": "bob.williams@university.edu",
                "type": "student"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Charlie Brown",
                "age": 19,
                "email": "charlie.brown@university.edu",
                "type": "student"
            }
        ]
        db.persons.insert_many(students)
        
        # Get student IDs for reference
        student_ids = []
        for i, student in enumerate(students):
            student_ids.append(student["id"])
        
        # Add student details
        student_details = [
            {
                "id": student_ids[0],
                "roll_number": "CS2023001",
                "entry_year": 2023,
                "program": "BS Computer Science"
            },
            {
                "id": student_ids[1],
                "roll_number": "MA2023002",
                "entry_year": 2023,
                "program": "BS Mathematics"
            },
            {
                "id": student_ids[2],
                "roll_number": "PH2023003",
                "entry_year": 2023,
                "program": "BS Physics"
            }
        ]
        db.students.insert_many(student_details)
        
        # Add enrollments
        enrollments = [
            {
                "student_id": student_ids[0],
                "course_id": course_ids[0],
                "enrollment_date": datetime.now().strftime("%Y-%m-%d"),
                "grade": None
            },
            {
                "student_id": student_ids[0],
                "course_id": course_ids[1],
                "enrollment_date": datetime.now().strftime("%Y-%m-%d"),
                "grade": None
            },
            {
                "student_id": student_ids[1],
                "course_id": course_ids[1],
                "enrollment_date": datetime.now().strftime("%Y-%m-%d"),
                "grade": None
            },
            {
                "student_id": student_ids[2],
                "course_id": course_ids[2],
                "enrollment_date": datetime.now().strftime("%Y-%m-%d"),
                "grade": None
            }
        ]
        db.enrollments.insert_many(enrollments)
        
        # Add users for each person
        for i, student_id in enumerate(student_ids):
            user_id = str(uuid.uuid4())
            username = students[i]["name"].lower().replace(" ", ".")
            hashed_password = hash_password("password123")
            db.users.insert_one({
                "id": user_id,
                "username": username,
                "password": hashed_password,
                "role": "Student",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        for i, instructor_id in enumerate(instructor_ids):
            user_id = str(uuid.uuid4())
            username = instructors[i]["name"].lower().replace(" ", ".")
            username = username.replace("dr.", "").replace("prof.", "").strip()
            hashed_password = hash_password("password123")
            db.users.insert_one({
                "id": user_id,
                "username": username,
                "password": hashed_password,
                "role": "Instructor",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

# Initialize database with default admin and sample data
if db is not None:  # Fixed: Changed from "if db:"
    create_default_admin()
    add_sample_data()

# Utility functions
def get_departments():
    try:
        departments = list(db.departments.find({}, {"_id": 0}))
        return pd.DataFrame(departments)
    except Exception as e:
        st.error(f"Error fetching departments: {e}")
        return pd.DataFrame()

def get_courses():
    try:
        pipeline = [
            {
                "$lookup": {
                    "from": "departments",
                    "localField": "department_id",
                    "foreignField": "id",
                    "as": "department"
                }
            },
            {
                "$lookup": {
                    "from": "persons",
                    "localField": "instructor_id",
                    "foreignField": "id",
                    "as": "instructor"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "id": 1,
                    "code": 1,
                    "name": 1,
                    "department": {"$arrayElemAt": ["$department.name", 0]},
                    "instructor": {"$arrayElemAt": ["$instructor.name", 0]},
                    "credits": 1,
                    "description": 1,
                    "schedule": 1,
                    "classroom": 1
                }
            }
        ]
        courses = list(db.courses.aggregate(pipeline))
        
        # For better mobile display, create a shorter ID version
        for course in courses:
            if 'id' in course:
                course['short_id'] = course['id'][:8] + "..." if len(course['id']) > 8 else course['id']
                
        return pd.DataFrame(courses)
    except Exception as e:
        st.error(f"Error fetching courses: {e}")
        return pd.DataFrame()

def get_students():
    try:
        pipeline = [
            {
                "$match": {"type": "student"}
            },
            {
                "$lookup": {
                    "from": "students",
                    "localField": "id",
                    "foreignField": "id",
                    "as": "student_details"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "id": 1,
                    "name": 1,
                    "age": 1,
                    "email": 1,
                    "roll_number": {"$arrayElemAt": ["$student_details.roll_number", 0]},
                    "entry_year": {"$arrayElemAt": ["$student_details.entry_year", 0]},
                    "program": {"$arrayElemAt": ["$student_details.program", 0]}
                }
            }
        ]
        students = list(db.persons.aggregate(pipeline))
        for student in students:
            student["id"] = truncate_id_for_display(student["id"])
        return pd.DataFrame(students)
    except Exception as e:
        st.error(f"Error fetching students: {e}")
        return pd.DataFrame()

def get_instructors():
    try:
        pipeline = [
            {
                "$match": {"type": "instructor"}
            },
            {
                "$lookup": {
                    "from": "instructors",
                    "localField": "id",
                    "foreignField": "id",
                    "as": "instructor_details"
                }
            },
            {
                "$lookup": {
                    "from": "departments",
                    "localField": "instructor_details.department_id",
                    "foreignField": "id",
                    "as": "department"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "id": 1,
                    "name": 1,
                    "age": 1,
                    "email": 1,
                    "salary": {"$arrayElemAt": ["$instructor_details.salary", 0]},
                    "department": {"$arrayElemAt": ["$department.name", 0]},
                    "position": {"$arrayElemAt": ["$instructor_details.position", 0]}
                }
            }
        ]
        instructors = list(db.persons.aggregate(pipeline))
        for instructor in instructors:
            instructor["id"] = truncate_id_for_display(instructor["id"])
        return pd.DataFrame(instructors)
    except Exception as e:
        st.error(f"Error fetching instructors: {e}")
        return pd.DataFrame()

def get_enrollments():
    try:
        pipeline = [
            {
                "$lookup": {
                    "from": "students",
                    "localField": "student_id",
                    "foreignField": "id",
                    "as": "student"
                }
            },
            {
                "$lookup": {
                    "from": "persons",
                    "localField": "student_id",
                    "foreignField": "id",
                    "as": "person"
                }
            },
            {
                "$lookup": {
                    "from": "courses",
                    "localField": "course_id",
                    "foreignField": "id",
                    "as": "course"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "student_id": 1,
                    "student_name": {"$arrayElemAt": ["$person.name", 0]},
                    "roll_number": {"$arrayElemAt": ["$student.roll_number", 0]},
                    "course_id": 1,
                    "course_name": {"$arrayElemAt": ["$course.name", 0]},
                    "enrollment_date": 1,
                    "grade": 1
                }
            }
        ]
        enrollments = list(db.enrollments.aggregate(pipeline))
        for enrollment in enrollments:
            enrollment["student_id"] = truncate_id_for_display(enrollment["student_id"])
            enrollment["course_id"] = truncate_id_for_display(enrollment["course_id"])
        return pd.DataFrame(enrollments)
    except Exception as e:
        st.error(f"Error fetching enrollments: {e}")
        return pd.DataFrame()

def get_student_courses(student_id):
    try:
        pipeline = [
            {
                "$match": {"student_id": student_id}
            },
            {
                "$lookup": {
                    "from": "courses",
                    "localField": "course_id",
                    "foreignField": "id",
                    "as": "course"
                }
            },
            {
                "$lookup": {
                    "from": "departments",
                    "localField": "course.department_id",
                    "foreignField": "id",
                    "as": "department"
                }
            },
            {
                "$lookup": {
                    "from": "persons",
                    "localField": "course.instructor_id",
                    "foreignField": "id",
                    "as": "instructor"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "id": {"$arrayElemAt": ["$course.id", 0]},
                    "code": {"$arrayElemAt": ["$course.code", 0]},
                    "name": {"$arrayElemAt": ["$course.name", 0]},
                    "department": {"$arrayElemAt": ["$department.name", 0]},
                    "instructor": {"$arrayElemAt": ["$instructor.name", 0]},
                    "credits": {"$arrayElemAt": ["$course.credits", 0]},
                    "enrollment_date": 1,
                    "grade": 1,
                    "schedule": {"$arrayElemAt": ["$course.schedule", 0]},
                    "classroom": {"$arrayElemAt": ["$course.classroom", 0]}
                }
            }
        ]
        courses = list(db.enrollments.aggregate(pipeline))
        for course in courses:
            course["id"] = truncate_id_for_display(course["id"])
        return pd.DataFrame(courses)
    except Exception as e:
        st.error(f"Error fetching student courses: {e}")
        return pd.DataFrame()

def get_instructor_courses(instructor_id):
    try:
        pipeline = [
            {
                "$match": {"instructor_id": instructor_id}
            },
            {
                "$lookup": {
                    "from": "departments",
                    "localField": "department_id",
                    "foreignField": "id",
                    "as": "department"
                }
            },
            {
                "$lookup": {
                    "from": "enrollments",
                    "localField": "id",
                    "foreignField": "course_id",
                    "as": "enrollments"
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "id": 1,
                    "code": 1,
                    "name": 1,
                    "department": {"$arrayElemAt": ["$department.name", 0]},
                    "credits": 1,
                    "description": 1,
                    "schedule": 1,
                    "classroom": 1,
                    "enrolled_students": {"$size": "$enrollments"}
                }
            }
        ]
        courses = list(db.courses.aggregate(pipeline))
        for course in courses:
            course["id"] = truncate_id_for_display(course["id"])
        return pd.DataFrame(courses)
    except Exception as e:
        st.error(f"Error fetching instructor courses: {e}")
        return pd.DataFrame()

def get_person_id_by_username(username, role):
    try:
        # Find the user by username and role
        user = db.users.find_one({"username": username, "role": role})
        if not user:
            return None
        
        # Map role to person type
        type_map = {"Student": "student", "Instructor": "instructor", "Admin": "admin"}
        person_type = type_map.get(role, "").lower()
        
        # Find the person by email pattern matching the username
        person = db.persons.find_one({"email": {"$regex": username, "$options": "i"}, "type": person_type})
        return person["id"] if person else None
    except Exception as e:
        st.error(f"Error finding person by username: {e}")
        return None

def truncate_id_for_display(id_str, length=8):
    """Truncate long IDs for better display on mobile"""
    if id_str and isinstance(id_str, str) and len(id_str) > length:
        return id_str[:length] + "..."
    return id_str

# Custom styling
def apply_custom_styles():
    st.markdown("""
    <style>
/* Global Styles */
.main {
    background-color: #f8f5ff;
    padding: 1rem;
}

.stApp {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Header Styles */
.main-header {
    font-size: 2rem;
    font-weight: bold;
    color: #4B0082;
    text-align: center;
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 3px solid #4B0082;
    text-shadow: 1px 1px 2px rgba(75, 0, 130, 0.1);
}

.section-header {
    font-size: 1.5rem;
    font-weight: bold;
    color: #4B0082;
    margin-top: 1.25rem;
    margin-bottom: 0.75rem;
    padding-left: 0.5rem;
    border-left: 5px solid #4B0082;
}

/* Card Styles */
.card {
    background-color: white;
    border-radius: 0.75rem;
    padding: 1rem;
    box-shadow: 0 0.375rem 1rem rgba(75, 0, 130, 0.1);
    margin-bottom: 1rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-top: 4px solid #4B0082;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 0.625rem 1.25rem rgba(75, 0, 130, 0.15);
}

/* Stat Box Styles */
.stat-box {
    background-color: #f8f4ff;
    border-left: 5px solid #4B0082;
    padding: 0.75rem;
    margin-bottom: 0.75rem;
    border-radius: 0 0.5rem 0.5rem 0;
    transition: background-color 0.3s ease;
}

.stat-box:hover {
    background-color: #f0e6ff;
}

.highlight {
    color: #4B0082;
    font-weight: bold;
    font-size: 1.75rem;
}

/* Tab Styles */
.stTabs [data-baseweb="tab-list"] {
    gap: 1.5rem;
    background-color: #f8f4ff;
    padding: 0.5rem;
    border-radius: 0.625rem 0.625rem 0 0;
    overflow-x: auto;
    flex-wrap: nowrap;
    white-space: nowrap;
}

.stTabs [data-baseweb="tab"] {
    height: 3rem;
    white-space: pre-wrap;
    background-color: #f3eeff;
    border-radius: 0.5rem 0.5rem 0 0;
    padding: 0.5rem 1rem;
    font-weight: 500;
    transition: all 0.2s ease;
    border: none;
    min-width: fit-content;
}

.stTabs [aria-selected="true"] {
    background-color: #4B0082;
    color: white;
    box-shadow: 0 -0.25rem 0.625rem rgba(75, 0, 130, 0.1);
}

.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
    background-color: #e6e0f0;
}

.stTabs [data-baseweb="tab-panel"] {
    background-color: white;
    border-radius: 0 0 0.625rem 0.625rem;
    padding: 1rem;
    box-shadow: 0 0.375rem 1rem rgba(75, 0, 130, 0.1);
}

/* Form Styles */
.stButton>button {
    background-color: #4B0082;
    color: white;
    border-radius: 0.5rem;
    padding: 0.5rem 1.5rem;
    font-weight: 500;
    border: none;
    transition: all 0.3s ease;
    width: 100%;
    max-width: 300px;
    margin: 0 auto;
    display: block;
}

.stButton>button:hover {
    background-color: #5c0099;
    box-shadow: 0 0.25rem 0.5rem rgba(75, 0, 130, 0.2);
    transform: translateY(-2px);
}

.stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
    border-radius: 0.5rem;
    border: 1px solid #d0c0e0;
    padding: 0.625rem 0.75rem;
    font-size: 1rem;
}

.stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
    border-color: #4B0082;
    box-shadow: 0 0 0 2px rgba(75, 0, 130, 0.2);
}

/* Expander Styles */
.streamlit-expanderHeader {
    background-color: #f8f4ff;
    border-radius: 0.5rem;
    padding: 0.625rem 0.9375rem;
    font-weight: 500;
    color: #4B0082;
    border: 1px solid #e0d0ff;
}

.streamlit-expanderContent {
    border: 1px solid #e0d0ff;
    border-top: none;
    border-radius: 0 0 0.5rem 0.5rem;
    padding: 1.25rem;
}

/* Table Styles */
.stDataFrame {
    border-radius: 0.625rem;
    overflow: hidden;
    box-shadow: 0 0.25rem 0.75rem rgba(75, 0, 130, 0.08);
    width: 100%;
    overflow-x: auto;
}

.stDataFrame table {
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
}

.stDataFrame th {
    background-color: #4B0082;
    color: white;
    padding: 0.75rem 0.9375rem;
    font-weight: 500;
    white-space: nowrap;
    position: sticky;
    top: 0;
    z-index: 1;
}

.stDataFrame td {
    padding: 0.625rem 0.9375rem;
    border-bottom: 1px solid #f0e6ff;
    white-space: normal;
    word-break: break-word;
    color: #3a2f45;
}

.stDataFrame tr:nth-child(even) {
    background-color: #f8f4ff;
}

/* Sidebar Styles */
.css-1d391kg, .css-12oz5g7 {
    background-color: #f0e6ff;
}

.sidebar .sidebar-content {
    background-color: #f0e6ff;
}

/* Alert and Info Styles */
.stAlert {
    border-radius: 0.5rem;
    padding: 0.9375rem;
    margin-bottom: 1.25rem;
}

.stAlert>div {
    padding: 0.9375rem;
    border-radius: 0.5rem;
}

/* Success Message */
.element-container:has(div[data-testid="stText"] div[class*="success"]) {
    background-color: #e6ffea;
    padding: 0.9375rem;
    border-radius: 0.5rem;
    border-left: 5px solid #00cc66;
    margin-bottom: 1.25rem;
}

/* Error Message */
.element-container:has(div[data-testid="stText"] div[class*="error"]) {
    background-color: #ffe6e6;
    padding: 0.9375rem;
    border-radius: 0.5rem;
    border-left: 5px solid #ff3333;
    margin-bottom: 1.25rem;
}

/* Info Message */
.element-container:has(div[data-testid="stText"] div[class*="info"]) {
    background-color: #e6f2ff;
    padding: 0.9375rem;
    border-radius: 0.5rem;
    border-left: 5px solid #3399ff;
    margin-bottom: 1.25rem;
}

/* Multiselect */
.stMultiSelect>div>div>div {
    background-color: white;
    border-radius: 0.5rem;
}

/* Checkbox */
.stCheckbox>div>div>label {
    color: #4B0082;
}

/* Radio */
.stRadio>div>div>label {
    color: #4B0082;
}

/* Slider */
.stSlider>div>div>div>div {
    background-color: #4B0082;
}

/* Progress Bar */
.stProgress>div>div>div>div {
    background-color: #4B0082;
}

/* Subheader */
h3 {
    color: #4B0082;
    font-weight: 600;
    margin-top: 1.25rem;
    margin-bottom: 0.625rem;
}

/* Bold text */
strong {
    color: #4B0082;
}

/* Chart Styles */
.stChart > div > div > svg {
    color: #4B0082 !important;
}

.stChart > div > div > svg g path.highcharts-point {
    fill: #4B0082 !important;
}

.stChart > div > div > svg g path.highcharts-graph {
    stroke: #4B0082 !important;
}

.stChart > div > div > svg g rect.highcharts-point {
    fill: #4B0082 !important;
}

/* Streamlit's built-in charts */
.element-container:has(div[data-testid="stChart"]) svg > g > rect {
    fill: #4B0082 !important;
}

/* Line charts */
.element-container:has(div[data-testid="stChart"]) svg > g > path {
    stroke: #4B0082 !important;
}

/* Altair charts */
.element-container:has(div[data-testid="stChart"]) svg .mark-rect > path {
    fill: #4B0082 !important;
}

.element-container:has(div[data-testid="stChart"]) svg .mark-line > path {
    stroke: #4B0082 !important;
}

/* Additional chart elements */
.element-container:has(div[data-testid="stChart"]) svg g.tick text {
    fill: #3a2f45 !important;
}

/* Bar chart specific */
.element-container:has(div[data-testid="stChart"]) svg g > rect.rect {
    fill: #4B0082 !important;
}

/* For vega-lite charts */
.element-container:has(div[data-testid="stVegaLiteChart"]) svg rect.mark-rect {
    fill: #4B0082 !important;
}

.element-container:has(div[data-testid="stVegaLiteChart"]) svg path.mark-line {
    stroke: #4B0082 !important;
}

/* Mobile Responsive Styles */
@media (max-width: 768px) {
    .main {
        padding: 0.5rem;
        background-color: #f8f5ff;
    }
    
    .main-header {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
    }
    
    .section-header {
        font-size: 1.25rem;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .card {
        padding: 0.75rem;
        margin-bottom: 0.75rem;
        background-color: #ffffff;
    }
    
    .highlight {
        font-size: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.375rem 0.75rem;
        height: 2.5rem;
        font-size: 0.875rem;
        background-color: #f3eeff;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding: 0.75rem;
        background-color: #ffffff;
    }
    
    .stButton>button {
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
    }
    
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        padding: 0.5rem;
        font-size: 0.875rem;
        border-color: #d0c0e0;
    }
    
    .stDataFrame th, .stDataFrame td {
        padding: 0.5rem;
        font-size: 0.875rem;
    }
    
    .stDataFrame td {
        color: #3a2f45;
    }
    
    h3 {
        font-size: 1.25rem;
        color: #4B0082;
    }
    
    /* Improve form layout on mobile */
    .stForm > div {
        flex-direction: column;
    }
    
    /* Make columns stack on mobile */
    .row-widget.stHorizontal {
        flex-wrap: wrap;
    }
    
    .row-widget.stHorizontal > div {
        flex: 1 1 100%;
        min-width: 100%;
        margin-bottom: 0.75rem;
    }
    
    /* Adjust sidebar for mobile */
    .css-1d391kg, .css-12oz5g7 {
        width: 100% !important;
        background-color: #f0e6ff;
    }
}

/* Tablet Responsive Styles */
@media (min-width: 769px) and (max-width: 1024px) {
    .main-header {
        font-size: 1.75rem;
    }
    
    .card {
        padding: 0.875rem;
        background-color: #ffffff;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 1rem;
        background-color: #f3eeff;
    }
}

/* Improve touch targets on mobile */
@media (pointer: coarse) {
    .stButton>button, 
    .stSelectbox>div>div>div,
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .streamlit-expanderHeader {
        min-height: 2.75rem;
    }
    
    .stCheckbox>div>div>label,
    .stRadio>div>div>label {
        padding: 0.5rem 0;
        display: block;
    }
}

/* Additional Mobile Optimizations */
@media (max-width: 768px) {
    /* Improve table display on mobile */
    .stDataFrame {
        font-size: 0.75rem;
    }
    
    .stDataFrame table {
        table-layout: fixed;
    }
    
    /* Hide or truncate long IDs on mobile */
    .stDataFrame td:nth-child(1) {
        max-width: 80px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    /* Make sure buttons are properly sized on mobile */
    .stButton>button {
        width: 100%;
        max-width: none;
        padding: 0.75rem 0.5rem;
    }
    
    /* Improve form layout on small screens */
    .stForm {
        padding: 0.5rem;
    }
    
    /* Adjust card padding for mobile */
    .card {
        padding: 0.5rem;
    }
    
    /* Make tabs more touch-friendly */
    .stTabs [data-baseweb="tab"] {
        min-width: 80px;
        padding: 0.5rem;
    }
    
    /* Improve sidebar on mobile */
    .css-1d391kg, .css-12oz5g7 {
        padding: 1rem 0.5rem !important;
    }
}
</style>
    """, unsafe_allow_html=True)

# Apply custom styles
apply_custom_styles()

def is_mobile():
    """Detect if user is on a mobile device based on viewport width"""
    mobile_detector = """
    <script>
    if (window.innerWidth < 768) {
        document.documentElement.classList.add('mobile');
    } else {
        document.documentElement.classList.remove('mobile');
    }
    </script>
    """
    st.markdown(mobile_detector, unsafe_allow_html=True)
    
    # Add CSS for mobile-specific styling
    st.markdown("""
    <style>
    html.mobile .hide-on-mobile {
        display: none !important;
    }
    
    html.mobile .mobile-full-width {
        width: 100% !important;
    }
    
    html.mobile .mobile-smaller-text {
        font-size: 0.8rem !important;
    }
    
    html.mobile .mobile-compact-table td {
        padding: 0.25rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

def create_mobile_friendly_cards(data_list, title_field, fields_to_display):
    """Create mobile-friendly cards instead of tables for small screens"""
    if not data_list:
        return
        
    for item in data_list:
        st.markdown(f"<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h4>{item.get(title_field, 'Item')}</h4>", unsafe_allow_html=True)
        
        for field, label in fields_to_display.items():
            value = item.get(field, "N/A")
            st.markdown(f"<p><strong>{label}:</strong> {value}</p>", unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

# Authentication functions
def signup():
    st.title("Sign Up")
    with st.form("signup_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        full_name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=16, max_value=100, value=20)
        secret_code = st.text_input("Access Code (For admin/instructor)", type="password")
        
        role = "Student"
        if secret_code == ADMIN_SECRET:
            role = "Admin"
        elif secret_code == TEACHER_SECRET:
            role = "Instructor"
        
        if st.form_submit_button("Create Account"):
            if username and password and email and full_name:
                # Check if username already exists
                if db.users.count_documents({"username": username}) > 0:
                    st.error("Username already exists!")
                else:
                    try:
                        # Create user
                        user_id = str(uuid.uuid4())
                        hashed_password = hash_password(password)
                        db.users.insert_one({
                            "id": user_id,
                            "username": username,
                            "password": hashed_password,
                            "role": role,
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        
                        # Create person
                        person_id = str(uuid.uuid4())
                        person_type = role.lower()
                        db.persons.insert_one({
                            "id": person_id,
                            "name": full_name,
                            "age": age,
                            "email": email,
                            "type": person_type
                        })
                        
                        # Create student or instructor record
                        if role == "Student":
                            # Generate roll number
                            current_year = datetime.now().year
                            student_count = db.students.count_documents({}) + 1
                            roll_number = f"S{current_year}{student_count:04d}"
                            
                            db.students.insert_one({
                                "id": person_id,
                                "roll_number": roll_number,
                                "entry_year": current_year,
                                "program": "Not Assigned"
                            })
                        elif role == "Instructor":
                            db.instructors.insert_one({
                                "id": person_id,
                                "salary": 0,
                                "position": "Not Assigned"
                            })
                        
                        st.success("Account created successfully!")
                    except Exception as e:
                        st.error(f"Registration failed: {str(e)}")
            else:
                st.warning("Please fill in all required fields!")

def login():
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            try:
                user = db.users.find_one({"username": username})
                
                if user and check_password(user["password"], password):
                    st.session_state.update({
                        'logged_in': True,
                        'user_id': user["id"],
                        'username': user["username"],
                        'role': user["role"]
                    })
                    st.success(f"Welcome {username}!")
                    st.rerun()  # Changed from st.experimental_rerun()
                else:
                    st.error("Invalid credentials")
            except Exception as e:
                st.error(f"Login failed: {str(e)}")

# Dashboard functions
def admin_dashboard():
    st.markdown("<div class='main-header'>University Management System - Admin Dashboard</div>", unsafe_allow_html=True)
    
    # Overview statistics
    col1, col2, col3, col4 = st.columns(4)
    
    # Get counts for each entity
    student_count = db.students.count_documents({})
    instructor_count = db.instructors.count_documents({})
    course_count = db.courses.count_documents({})
    department_count = db.departments.count_documents({})
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>Students</h3><h2 class='highlight'>{student_count}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>Instructors</h3><h2 class='highlight'>{instructor_count}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>Courses</h3><h2 class='highlight'>{course_count}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>Departments</h3><h2 class='highlight'>{department_count}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Admin tabs
    admin_tabs = st.tabs(["Students", "Instructors", "Courses", "Departments", "Users", "Reports"])

    # Add responsive class to improve mobile display
    st.markdown("""
<style>
@media (max-width: 768px) {
    .main-header {
        font-size: 1.25rem;
    }
    
    /* Hide ID columns on very small screens */
    @media (max-width: 480px) {
        .stDataFrame [data-testid="column_header"]:first-child,
        .stDataFrame [data-testid="cell"]:first-child {
            display: none;
        }
    }
}
</style>
""", unsafe_allow_html=True)
    
    with admin_tabs[0]:
        # Students management
        st.markdown("<div class='section-header'>Student Management</div>", unsafe_allow_html=True)
        students_df = get_students()
        st.dataframe(students_df, use_container_width=True, hide_index=True)
        
        # Add new student
        with st.expander("Add New Student"):
            with st.form("add_student_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Full Name")
                    age = st.number_input("Age", min_value=16, max_value=100, value=18)
                    email = st.text_input("Email")
                
                with col2:
                    roll_number = st.text_input("Roll Number")
                    entry_year = st.number_input("Entry Year", min_value=2000, max_value=datetime.now().year, value=datetime.now().year)
                    program = st.selectbox("Program", ["BS Computer Science", "BS Mathematics", "BS Physics", "BS Chemistry", "BA Economics", "Other"])
                
                if st.form_submit_button("Add Student"):
                    if name and email and roll_number:
                        try:
                            # Check if roll number already exists
                            if db.students.count_documents({"roll_number": roll_number}) > 0:
                                st.error("Roll number already exists!")
                            else:
                                # Create a new student
                                student_id = str(uuid.uuid4())
                                
                                # Insert into persons collection
                                db.persons.insert_one({
                                    "id": student_id,
                                    "name": name,
                                    "age": age,
                                    "email": email,
                                    "type": "student"
                                })
                                
                                # Insert into students collection
                                db.students.insert_one({
                                    "id": student_id,
                                    "roll_number": roll_number,
                                    "entry_year": entry_year,
                                    "program": program
                                })
                                
                                # Create user account
                                user_id = str(uuid.uuid4())
                                username = email.split('@')[0]
                                hashed_password = hash_password("password123")  # Default password
                                
                                db.users.insert_one({
                                    "id": user_id,
                                    "username": username,
                                    "password": hashed_password,
                                    "role": "Student",
                                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                })
                                
                                st.success("Student added successfully!")
                        except Exception as e:
                            st.error(f"Error adding student: {e}")
                    else:
                        st.warning("Please fill in all required fields!")
    
    with admin_tabs[1]:
        # Instructors management
        st.markdown("<div class='section-header'>Instructor Management</div>", unsafe_allow_html=True)
        instructors_df = get_instructors()
        st.dataframe(instructors_df, use_container_width=True, hide_index=True)
        
        # Add new instructor
        with st.expander("Add New Instructor"):
            with st.form("add_instructor_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Full Name")
                    age = st.number_input("Age", min_value=22, max_value=100, value=35)
                    email = st.text_input("Email")
                
                with col2:
                    departments = get_departments()
                    department_options = {row["name"]: row["id"] for _, row in departments.iterrows()}
                    selected_department = st.selectbox("Department", list(department_options.keys()))
                    position = st.selectbox("Position", ["Professor", "Associate Professor", "Assistant Professor", "Lecturer"])
                    salary = st.number_input("Salary", min_value=0, value=75000)
                
                if st.form_submit_button("Add Instructor"):
                    if name and email:
                        try:
                            # Create a new instructor
                            instructor_id = str(uuid.uuid4())
                            department_id = department_options[selected_department]
                            
                            # Insert into persons collection
                            db.persons.insert_one({
                                "id": instructor_id,
                                "name": name,
                                "age": age,
                                "email": email,
                                "type": "instructor"
                            })
                            
                            # Insert into instructors collection
                            db.instructors.insert_one({
                                "id": instructor_id,
                                "salary": salary,
                                "department_id": department_id,
                                "position": position
                            })
                            
                            # Create user account
                            user_id = str(uuid.uuid4())
                            username = email.split('@')[0]
                            hashed_password = hash_password("password123")  # Default password
                            
                            db.users.insert_one({
                                "id": user_id,
                                "username": username,
                                "password": hashed_password,
                                "role": "Instructor",
                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                            
                            st.success("Instructor added successfully!")
                        except Exception as e:
                            st.error(f"Error adding instructor: {e}")
                    else:
                        st.warning("Please fill in all required fields!")
    
    with admin_tabs[2]:
        # Courses management
        st.markdown("<div class='section-header'>Course Management</div>", unsafe_allow_html=True)
        
        # Check if on mobile and adjust display
        is_mobile_view = st.checkbox("Compact view", value=True)
        
        courses_df = get_courses()
        
        if is_mobile_view:
            # Mobile-friendly display with fewer columns
            display_cols = ["code", "name", "department", "credits"]
            st.dataframe(courses_df[display_cols], use_container_width=True, hide_index=True)
        else:
            # Full display for larger screens
            st.dataframe(courses_df, use_container_width=True, hide_index=True)
        
        # Add new course
        with st.expander("Add New Course"):
            with st.form("add_course_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    course_code = st.text_input("Course Code")
                    course_name = st.text_input("Course Name")
                    credits = st.number_input("Credits", min_value=1, max_value=6, value=3)
                    description = st.text_area("Description")
                
                with col2:
                    departments = get_departments()
                    department_options = {row["name"]: row["id"] for _, row in departments.iterrows()}
                    selected_department = st.selectbox("Department", list(department_options.keys()))
                    
                    instructors = get_instructors()
                    instructor_options = {"None": None}
                    instructor_options.update({row["name"]: row["id"] for _, row in instructors.iterrows()})
                    selected_instructor = st.selectbox("Instructor", list(instructor_options.keys()))
                    
                    schedule = st.text_input("Schedule (e.g., Mon/Wed 10:00 AM)")
                    classroom = st.text_input("Classroom")
                
                if st.form_submit_button("Add Course"):
                    if course_code and course_name and credits:
                        try:
                            # Create a new course
                            course_id = str(uuid.uuid4())
                            department_id = department_options[selected_department]
                            instructor_id = instructor_options[selected_instructor]
                            
                            # Insert into courses collection
                            db.courses.insert_one({
                                "id": course_id,
                                "code": course_code,
                                "name": course_name,
                                "department_id": department_id,
                                "instructor_id": instructor_id,
                                "credits": credits,
                                "description": description,
                                "schedule": schedule,
                                "classroom": classroom
                            })
                            
                            st.success("Course added successfully!")
                        except Exception as e:
                            st.error(f"Error adding course: {e}")
                    else:
                        st.warning("Please fill in all required fields!")
    
    with admin_tabs[3]:
        # Departments management
        st.markdown("<div class='section-header'>Department Management</div>", unsafe_allow_html=True)
        departments_df = get_departments()
        st.dataframe(departments_df, use_container_width=True, hide_index=True)
        
        # Add new department
        with st.expander("Add New Department"):
            with st.form("add_department_form"):
                department_name = st.text_input("Department Name")
                
                if st.form_submit_button("Add Department"):
                    if department_name:
                        try:
                            # Create a new department
                            department_id = str(uuid.uuid4())
                            
                            # Insert into departments collection
                            db.departments.insert_one({
                                "id": department_id,
                                "name": department_name
                            })
                            
                            st.success("Department added successfully!")
                        except Exception as e:
                            st.error(f"Error adding department: {e}")
                    else:
                        st.warning("Please enter a department name!")
    
    with admin_tabs[4]:
        # Users management
        st.markdown("<div class='section-header'>User Management</div>", unsafe_allow_html=True)
        
        # Get all users
        users = list(db.users.find({}, {"_id": 0, "id": 1, "username": 1, "role": 1, "created_at": 1}))
        users_df = pd.DataFrame(users)
        st.dataframe(users_df, use_container_width=True, hide_index=True)
        
        # Reset password
        with st.expander("Reset User Password"):
            usernames = [user["username"] for user in users]
            selected_user = st.selectbox("Select User", usernames)
            new_password = st.text_input("New Password", type="password")
            
            if st.button("Reset Password") and new_password:
                try:
                    hashed_password = hash_password(new_password)
                    db.users.update_one(
                        {"username": selected_user},
                        {"$set": {"password": hashed_password}}
                    )
                    st.success(f"Password reset for {selected_user}")
                except Exception as e:
                    st.error(f"Error resetting password: {e}")
    
    with admin_tabs[5]:
        # Reports
        st.markdown("<div class='section-header'>System Reports</div>", unsafe_allow_html=True)
        
        # Report options
        report_options = {
            "Student Demographics": "Analyze student age distribution and programs",
            "Instructor Salary Analysis": "View salary distribution by department and position",
            "Course Popularity": "See which courses are most popular",
            "Department Comparison": "Compare departments by various metrics"
        }
        
        selected_report = st.selectbox("Select Report", list(report_options.keys()))
        
        if selected_report == "Student Demographics":
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Student Demographics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Age distribution
                students = get_students()
                st.bar_chart(students["age"].value_counts().sort_index(), use_container_width=True)
                st.caption("Student Age Distribution")
            
            with col2:
                # Program distribution
                program_counts = students["program"].value_counts()
                st.bar_chart(program_counts, use_container_width=True)
                st.caption("Student Program Distribution")
            
            # Entry year analysis
            st.subheader("Entry Year Analysis")
            entry_year_counts = students["entry_year"].value_counts().sort_index()
            st.line_chart(entry_year_counts, use_container_width=True)
            st.caption("Students by Entry Year")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        elif selected_report == "Instructor Salary Analysis":
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Instructor Salary Analysis")
            
            # Salary by position
            instructors = get_instructors()
            salary_by_position = instructors.groupby("position")["salary"].mean().sort_values(ascending=False)
            st.bar_chart(salary_by_position, use_container_width=True)
            st.caption("Average Salary by Position")
            
            # Salary by department
            salary_by_dept = instructors.groupby("department")["salary"].mean().sort_values(ascending=False)
            st.bar_chart(salary_by_dept, use_container_width=True)
            st.caption("Average Salary by Department")
            
            # Salary distribution
            st.subheader("Salary Distribution")
            st.altair_chart(alt.Chart(instructors).mark_bar().encode(
                alt.X("salary:Q", bin=True),
                y='count()',
            ), use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        elif selected_report == "Course Popularity":
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Course Popularity")
            
            # Get course enrollments
            pipeline = [
                {
                    "$lookup": {
                        "from": "courses",
                        "localField": "course_id",
                        "foreignField": "id",
                        "as": "course"
                    }
                },
                {
                    "$lookup": {
                        "from": "departments",
                        "localField": "course.department_id",
                        "foreignField": "id",
                        "as": "department"
                    }
                },
                {
                    "$group": {
                        "_id": {
                            "course_name": {"$arrayElemAt": ["$course.name", 0]},
                            "department_name": {"$arrayElemAt": ["$department.name", 0]}
                        },
                        "enrollments": {"$sum": 1}
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "Course": "$_id.course_name",
                        "Department": "$_id.department_name",
                        "Enrollments": "$enrollments"
                    }
                },
                {
                    "$sort": {"Enrollments": -1}
                }
            ]
            
            course_popularity = list(db.enrollments.aggregate(pipeline))
            
            if course_popularity:
                popularity_df = pd.DataFrame(course_popularity)
                
                # Top 10 courses
                st.subheader("Top 10 Courses by Enrollment")
                top_10 = popularity_df.head(10)
                st.bar_chart(top_10.set_index("Course"))
                
                # By department
                st.subheader("Enrollments by Department")
                dept_enrollments = popularity_df.groupby("Department")["Enrollments"].sum().sort_values(ascending=False)
                st.bar_chart(dept_enrollments)
            else:
                st.info("No enrollment data available")
            
            st.markdown("</div>", unsafe_allow_html=True)

def instructor_dashboard():
    st.markdown("<div class='main-header'>University Management System - Instructor Dashboard</div>", unsafe_allow_html=True)
    
    # Get instructor ID
    instructor_id = get_person_id_by_username(st.session_state['username'], "Instructor")
    
    if not instructor_id:
        st.warning("Instructor profile not found. Please contact an administrator.")
        return
    
    # Get instructor details
    try:
        pipeline = [
            {
                "$match": {"id": instructor_id}
            },
            {
                "$lookup": {
                    "from": "instructors",
                    "localField": "id",
                    "foreignField": "id",
                    "as": "instructor_details"
                }
            },
            {
                "$lookup": {
                    "from": "departments",
                    "localField": "instructor_details.department_id",
                    "foreignField": "id",
                    "as": "department"
                }
            },
            {
                "$project": {
                    "name": 1,
                    "age": 1,
                    "email": 1,
                    "position": {"$arrayElemAt": ["$instructor_details.position", 0]},
                    "department": {"$arrayElemAt": ["$department.name", 0]},
                    "salary": {"$arrayElemAt": ["$instructor_details.salary", 0]}
                }
            }
        ]
        
        instructor_result = list(db.persons.aggregate(pipeline))
        
        if not instructor_result:
            st.warning("Instructor details not found. Please contact an administrator.")
            return
        
        instructor = instructor_result[0]
        
        # Display instructor info
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Instructor Information")
            st.write(f"**Name:** {instructor['name']}")
            
            # Safely access position with a fallback
            position = instructor.get('position', 'Not Assigned')
            st.write(f"**Position:** {position}")
            
            # Fix for the KeyError: 'department'
            # Safely access department with a fallback
            department = instructor.get('department', 'Not Assigned')
            st.write(f"**Department:** {department}")
            
            st.write(f"**Email:** {instructor['email']}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Get instructor courses
        instructor_courses = get_instructor_courses(instructor_id)
        
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Teaching Summary")
            st.write(f"**Courses Teaching:** {len(instructor_courses)}")
            
            if not instructor_courses.empty:
                total_students = instructor_courses['enrolled_students'].sum()
                st.write(f"**Total Students:** {total_students}")
                st.write(f"**Total Credits:** {instructor_courses['credits'].sum()}")
            else:
                st.write("**Total Students:** 0")
                st.write("**Total Credits:** 0")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Instructor tabs
        instructor_tabs = st.tabs(["My Courses", "Grade Management", "Student List"])
        
        with instructor_tabs[0]:
            st.markdown("<div class='section-header'>My Courses</div>", unsafe_allow_html=True)
            
            if not instructor_courses.empty:
                # Add toggle for mobile view
                use_card_view = st.checkbox("Card view (better for mobile)", value=True)
                
                if use_card_view:
                    # Convert DataFrame to list of dicts for card display
                    courses_list = instructor_courses.to_dict('records')
                    fields_to_display = {
                        "code": "Code",
                        "name": "Name",
                        "department": "Department",
                        "credits": "Credits",
                        "enrolled_students": "Students"
                    }
                    create_mobile_friendly_cards(courses_list, "name", fields_to_display)
                else:
                    st.dataframe(instructor_courses, use_container_width=True, hide_index=True)
            else:
                st.info("You are not teaching any courses yet.")
        
        with instructor_tabs[1]:
            st.markdown("<div class='section-header'>Grade Management</div>", unsafe_allow_html=True)
            
            if not instructor_courses.empty:
                # Select course
                course_options = {row["name"]: row["id"] for _, row in instructor_courses.iterrows()}
                selected_course = st.selectbox("Select Course", list(course_options.keys()))
                course_id = course_options[selected_course]
                
                # Get enrolled students
                pipeline = [
                    {
                        "$match": {"course_id": course_id}
                    },
                    {
                        "$lookup": {
                            "from": "students",
                            "localField": "student_id",
                            "foreignField": "id",
                            "as": "student"
                        }
                    },
                    {
                        "$lookup": {
                            "from": "persons",
                            "localField": "student_id",
                            "foreignField": "id",
                            "as": "person"
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "student_id": 1,
                            "name": {"$arrayElemAt": ["$person.name", 0]},
                            "roll_number": {"$arrayElemAt": ["$student.roll_number", 0]},
                            "grade": 1
                        }
                    }
                ]
                
                enrolled_students = list(db.enrollments.aggregate(pipeline))
                
                if enrolled_students:
                    st.subheader("Enrolled Students")
                    
                    # Create a dataframe for display
                    enrolled_df = pd.DataFrame(enrolled_students)
                    st.dataframe(enrolled_df, use_container_width=True, hide_index=True)
                    
                    # Grade update form
                    st.subheader("Update Grades")
                    
                    with st.form("update_grades_form"):
                        student_options = {student["name"]: student["student_id"] for student in enrolled_students}
                        selected_student = st.selectbox("Select Student", list(student_options.keys()))
                        student_id = student_options[selected_student]
                        
                        # Get current grade
                        current_grade = None
                        for student in enrolled_students:
                            if student["student_id"] == student_id:
                                current_grade = student.get("grade")
                                break
                        
                        grade_options = ["A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F", None]
                        selected_grade = st.selectbox(
                            "Select Grade", 
                            grade_options, 
                            index=grade_options.index(current_grade) if current_grade in grade_options else len(grade_options)-1
                        )
                        
                        if st.form_submit_button("Update Grade"):
                            try:
                                db.enrollments.update_one(
                                    {"student_id": student_id, "course_id": course_id},
                                    {"$set": {"grade": selected_grade}}
                                )
                                st.success(f"Grade updated for {selected_student}!")
                            except Exception as e:
                                st.error(f"Error updating grade: {e}")
                else:
                    st.info("No students enrolled in this course")
            else:
                st.info("You are not teaching any courses yet.")
        
        with instructor_tabs[2]:
            st.markdown("<div class='section-header'>Student List</div>", unsafe_allow_html=True)
            
            if not instructor_courses.empty:
                # Get all students in instructor's courses
                course_ids = instructor_courses["id"].tolist()
                
                pipeline = [
                    {
                        "$match": {"course_id": {"$in": course_ids}}
                    },
                    {
                        "$lookup": {
                            "from": "students",
                            "localField": "student_id",
                            "foreignField": "id",
                            "as": "student"
                        }
                    },
                    {
                        "$lookup": {
                            "from": "persons",
                            "localField": "student_id",
                            "foreignField": "id",
                            "as": "person"
                        }
                    },
                    {
                        "$group": {
                            "_id": "$student_id",
                            "name": {"$first": {"$arrayElemAt": ["$person.name", 0]}},
                            "roll_number": {"$first": {"$arrayElemAt": ["$student.roll_number", 0]}},
                            "program": {"$first": {"$arrayElemAt": ["$student.program", 0]}},
                            "email": {"$first": {"$arrayElemAt": ["$person.email", 0]}}
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "name": 1,
                            "roll_number": 1,
                            "program": 1,
                            "email": 1
                        }
                    },
                    {
                        "$sort": {"name": 1}
                    }
                ]
                
                students = list(db.enrollments.aggregate(pipeline))
                students_df = pd.DataFrame(students)
                
                if not students_df.empty:
                    st.dataframe(students_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No students enrolled in your courses")
            else:
                st.info("You are not teaching any courses yet.")
    except Exception as e:
        st.error(f"Error loading instructor dashboard: {e}")

def student_dashboard():
    st.markdown("<div class='main-header'>University Management System - Student Dashboard</div>", unsafe_allow_html=True)
    
    # Get student ID
    student_id = get_person_id_by_username(st.session_state['username'], "Student")
    
    if not student_id:
        st.warning("Student profile not found. Please contact an administrator.")
        return
    
    try:
        # Get student details
        pipeline = [
            {
                "$match": {"id": student_id}
            },
            {
                "$lookup": {
                    "from": "students",
                    "localField": "id",
                    "foreignField": "id",
                    "as": "student_details"
                }
            },
            {
                "$project": {
                    "name": 1,
                    "age": 1,
                    "email": 1,
                    "roll_number": {"$arrayElemAt": ["$student_details.roll_number", 0]},
                    "entry_year": {"$arrayElemAt": ["$student_details.entry_year", 0]},
                    "program": {"$arrayElemAt": ["$student_details.program", 0]}
                }
            }
        ]
        
        student_result = list(db.persons.aggregate(pipeline))
        
        if not student_result:
            st.warning("Student details not found. Please contact an administrator.")
            return
        
        student = student_result[0]
        
        # Display student info
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Student Information")
            st.write(f"**Name:** {student['name']}")
            st.write(f"**Roll Number:** {student.get('roll_number', 'Not Assigned')}")
            st.write(f"**Program:** {student.get('program', 'Not Assigned')}")
            st.write(f"**Entry Year:** {student.get('entry_year', 'Not Available')}")
            st.write(f"**Email:** {student['email']}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Get student courses
        student_courses = get_student_courses(student_id)
        
        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Academic Summary")
            
            if not student_courses.empty:
                total_credits = student_courses['credits'].sum()
                completed_courses = student_courses[student_courses['grade'].notna()]
                
                st.write(f"**Enrolled Courses:** {len(student_courses)}")
                st.write(f"**Total Credits:** {total_credits}")
                
                if not completed_courses.empty:
                    # Calculate GPA (simplified)
                    grade_points = {
                        'A': 4.0, 'A-': 3.7,
                        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
                        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
                        'D+': 1.3, 'D': 1.0, 'F': 0.0
                    }
                    
                    total_points = 0
                    total_graded_credits = 0
                    
                    for _, course in completed_courses.iterrows():
                        if course['grade'] in grade_points:
                            total_points += grade_points[course['grade']] * course['credits']
                            total_graded_credits += course['credits']
                    
                    if total_graded_credits > 0:
                        gpa = total_points / total_graded_credits
                        st.write(f"**GPA:** {gpa:.2f}")
                    else:
                        st.write("**GPA:** N/A")
                else:
                    st.write("**GPA:** N/A")
            else:
                st.write("**Enrolled Courses:** 0")
                st.write("**Total Credits:** 0")
                st.write("**GPA:** N/A")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Student tabs
        student_tabs = st.tabs(["My Courses", "Course Registration", "Grades"])
        
        with student_tabs[0]:
            st.markdown("<div class='section-header'>My Courses</div>", unsafe_allow_html=True)
            
            if not student_courses.empty:
                # Add toggle for mobile view
                use_card_view = st.checkbox("Card view (better for mobile)", value=True)
                
                if use_card_view:
                    # Convert DataFrame to list of dicts for card display
                    courses_list = student_courses.to_dict('records')
                    fields_to_display = {
                        "code": "Code",
                        "name": "Name",
                        "department": "Department",
                        "instructor": "Instructor",
                        "credits": "Credits",
                        "grade": "Grade"
                    }
                    create_mobile_friendly_cards(courses_list, "name", fields_to_display)
                else:
                    # Original display with cards
                    for _, course in student_courses.iterrows():
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.subheader(f"{course['code']} - {course['name']}")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Department:** {course.get('department', 'Not Available')}")
                            st.write(f"**Instructor:** {course.get('instructor', 'Not Assigned')}")
                            st.write(f"**Credits:** {course['credits']}")
                        
                        with col2:
                            st.write(f"**Schedule:** {course.get('schedule', 'Not Available')}")
                            st.write(f"**Classroom:** {course.get('classroom', 'Not Available')}")
                            if pd.notna(course['grade']):
                                st.write(f"**Grade:** {course['grade']}")
                            else:
                                st.write("**Grade:** Not graded yet")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("You are not enrolled in any courses yet.")
        
        with student_tabs[1]:
            st.markdown("<div class='section-header'>Course Registration</div>", unsafe_allow_html=True)
            
            # Get available courses (not already enrolled)
            pipeline = [
                {
                    "$lookup": {
                        "from": "enrollments",
                        "let": {"course_id": "$id"},
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {
                                        "$and": [
                                            {"$eq": ["$course_id", "$$course_id"]},
                                            {"$eq": ["$student_id", student_id]}
                                        ]
                                    }
                                }
                            }
                        ],
                        "as": "enrollment"
                    }
                },
                {
                    "$match": {"enrollment": {"$size": 0}}
                },
                {
                    "$lookup": {
                        "from": "departments",
                        "localField": "department_id",
                        "foreignField": "id",
                        "as": "department"
                    }
                },
                {
                    "$lookup": {
                        "from": "persons",
                        "localField": "instructor_id",
                        "foreignField": "id",
                        "as": "instructor"
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "id": 1,
                        "code": 1,
                        "name": 1,
                        "department": {"$arrayElemAt": ["$department.name", 0]},
                        "instructor": {"$arrayElemAt": ["$instructor.name", 0]},
                        "credits": 1,
                        "schedule": 1,
                        "classroom": 1
                    }
                }
            ]
            
            available_courses = list(db.courses.aggregate(pipeline))
            
            if available_courses:
                available_df = pd.DataFrame(available_courses)
                
                st.dataframe(available_df[["code", "name", "department", "instructor", "credits", "schedule"]], 
                            use_container_width=True, hide_index=True)
                
                # Registration form
                with st.form("course_registration_form"):
                    course_options = {f"{course['code']} - {course['name']}": course['id'] for course in available_courses}
                    selected_courses = st.multiselect("Select Courses to Register", list(course_options.keys()))
                    
                    if st.form_submit_button("Register for Courses"):
                        if selected_courses:
                            try:
                                enrollments = []
                                for course in selected_courses:
                                    course_id = course_options[course]
                                    enrollments.append({
                                        "student_id": student_id,
                                        "course_id": course_id,
                                        "enrollment_date": datetime.now().strftime("%Y-%m-%d"),
                                        "grade": None
                                    })
                                
                                if enrollments:
                                    db.enrollments.insert_many(enrollments)
                                    st.success(f"Successfully registered for {len(selected_courses)} courses!")
                                    st.rerun()  # Changed from st.experimental_rerun()
                            except Exception as e:
                                st.error(f"Error registering for courses: {e}")
                        else:
                            st.warning("Please select at least one course")
            else:
                st.info("No available courses to register")
        
        with student_tabs[2]:
            st.markdown("<div class='section-header'>My Grades</div>", unsafe_allow_html=True)
            
            if not student_courses.empty:
                # Filter to only show courses with grades
                graded_courses = student_courses[['code', 'name', 'credits', 'grade']].copy()
                graded_courses = graded_courses.fillna({'grade': 'Not Graded'})
                
                st.dataframe(graded_courses, use_container_width=True, hide_index=True)
                
                # Grade distribution chart
                grade_counts = graded_courses['grade'].value_counts()
                if len(grade_counts) > 1:  # Only show chart if there are actual grades
                    st.subheader("Grade Distribution")
                    st.bar_chart(grade_counts)
            else:
                st.info("You are not enrolled in any courses yet.")
    except Exception as e:
        st.error(f"Error loading student dashboard: {e}")

def main():
    # Check if user is on mobile and apply appropriate styles
    is_mobile()
    
    st.sidebar.title("🏫 University Management System")
    st.sidebar.markdown("---")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        menu = st.sidebar.radio("Menu", ["Login", "Sign Up"])
        if menu == "Login":
            login()
        else:
            signup()
    else:
        st.sidebar.write(f"Logged in as: **{st.session_state['username']}** ({st.session_state['role']})")
        st.sidebar.markdown("---")
        
        # Role-specific sidebar menu
        if st.session_state['role'] == "Admin":
            menu_options = ["Dashboard", "Students", "Instructors", "Courses", "Departments", "Users", "Reports"]
            selected = st.sidebar.selectbox("Navigation", menu_options)
            # Admin always sees the dashboard for now
        elif st.session_state['role'] == "Instructor":
            menu_options = ["Dashboard", "My Courses", "Grade Management", "Student List"]
            selected = st.sidebar.selectbox("Navigation", menu_options)
            # Instructor always sees the dashboard for now
        else:  # Student
            menu_options = ["Dashboard", "My Courses", "Course Registration", "Grades"]
            selected = st.sidebar.selectbox("Navigation", menu_options)
            # Student always sees the dashboard for now
        
        if st.sidebar.button("🔒 Logout"):
            st.session_state.clear()
            st.rerun()  # Changed from st.experimental_rerun()
        
        # Display appropriate dashboard based on role
        if st.session_state['role'] == "Admin":
            admin_dashboard()
        elif st.session_state['role'] == "Instructor":
            instructor_dashboard()
        else:
            student_dashboard()

    st.sidebar.markdown("---")
    st.sidebar.markdown("© 2025 University Management System")

if __name__ == "__main__":
    main()
