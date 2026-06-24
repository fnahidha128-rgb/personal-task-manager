import streamlit as st
import requests
from datetime import date

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Personal Task Manager",
    page_icon="📋",
    layout="wide"
)

# ---------------- SESSION ----------------
if "token" not in st.session_state:
    st.session_state.token = None
if "email" not in st.session_state:
    st.session_state.email = None
if "page" not in st.session_state:
    st.session_state.page = "Login"


# ---------------- API HELPER ----------------
def api_call(method, endpoint, data=None, params=None):
    headers = {}

    if st.session_state.get("token"):
        headers["Authorization"] = f"Bearer {st.session_state.get('token')}"

    try:
        response = requests.request(
            method=method,
            url=f"{API_BASE_URL}{endpoint}",
            json=data,
            params=params,
            headers=headers,
            timeout=5
        )

        try:
            body = response.json()
        except Exception:
            body = {}

        return response.status_code, body

    except requests.exceptions.ConnectionError:
        st.error("Backend server is not running. Start FastAPI first.")
        return 500, {}

    except requests.exceptions.Timeout:
        st.error("Request timed out. Try again.")
        return 500, {}
# ---------------- STYLES ----------------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}
.sub-title {
    text-align: center;
    color: #6b7280;
    font-size: 17px;
    margin-bottom: 35px;
}
.card {
    background: #ffffff;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
    margin-bottom: 18px;
}
.task-card {
    background: #1f2937;
    color: #f9fafb;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #374151;
    margin-bottom: 14px;
}
.task-card h4 {
    color: #ffffff;
}
.task-card p {
    color: #d1d5db;
}
.footer {
    text-align: center;
    color: #6b7280;
    font-size: 13px;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)



# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## Task Manager")
    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.token:
        st.markdown(f"""
        <div style="
            background: #111827;
            border: 1px solid #374151;
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 25px;
        ">
            <div style="font-size: 14px; color: #9ca3af;">Logged in as</div>
            <div style="font-size: 16px; color: #22c55e; font-weight: 600;">
                {st.session_state.email}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### NAVIGATION")

        if st.button("Dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()

        if st.button("Add Task", use_container_width=True):
            st.session_state.page = "Add Task"
            st.rerun()

        if st.button("Profile", use_container_width=True):
            st.session_state.page = "Profile"
            st.rerun()

        if st.button(" Help", use_container_width=True):
            st.session_state.page = "Help"
            st.rerun()

        st.markdown("---")

        if st.button("Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    else:
        st.markdown("""
        <div style="
            background: #111827;
            border: 1px solid #374151;
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 25px;
        ">
            <div style="font-size: 15px; color: #facc15;">
                Not Logged In
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Login", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()

        if st.button("Register", use_container_width=True):
            st.session_state.page = "Register"
            st.rerun()


# ---------------- HEADER ----------------
st.markdown('<div class="main-title"> Personal Task Manager</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Organize your tasks, track progress, and stay productive</div>', unsafe_allow_html=True)


# ---------------- LOGIN ----------------
def login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        
        st.subheader("Login")

        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)

            if submit:
                if not email or not password:
                    st.error("Please enter email and password.")
                else:
                    status, data = api_call("POST", "/auth/login", {
                        "email": email,
                        "password": password
                    })

                    if status == 200:
                        st.session_state.token = data.get("token") or data.get("access_token")
                        st.session_state.email = email
                        st.session_state.page = "Dashboard"
                        st.success("Login successful.")
                        st.rerun()
                    else:
                        st.error(data.get("detail", "Invalid email or password."))

        


# ---------------- REGISTER ----------------
def register_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        
        st.subheader("Create Account")

        with st.form("register_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register", use_container_width=True)

            if submit:
                if not email or not password or not confirm:
                    st.error("All fields are required.")
                elif "@" not in email:
                    st.error("Enter a valid email address.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                else:
                    status, data = api_call("POST", "/auth/register", {
                        "email": email,
                        "password": password
                    })

                    if status in [200, 201]:
                        st.success("Account created successfully. Please login.")
                        st.session_state.page = "Login"
                    else:
                        st.error(data.get("detail", "Registration failed."))

        


# ---------------- DASHBOARD ----------------
def dashboard_page():
    st.subheader("Dashboard")

    st.markdown(
    f"### Welcome back, {st.session_state.email.split('@')[0]} 👋"
    )
    status, all_tasks_data = api_call("GET", "/tasks")

    if status == 200:
        total = len(all_tasks_data)
        pending = len([t for t in all_tasks_data if t.get("status") == "pending"])
        in_progress = len([t for t in all_tasks_data if t.get("status") == "in-progress"])
        done = len([t for t in all_tasks_data if t.get("status") == "done"])
    else:
        total = pending = in_progress = done = 0

    search_text = st.text_input(
    "🔍 Search Tasks",
    placeholder="Search by title..."
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total", total)
    c2.metric("🟡 Pending", pending)
    c3.metric("🔵 Progress", in_progress)
    c4.metric("🟢 Done", done)

    st.markdown("---")

    f1, f2 = st.columns(2)
    with f1:
        status_filter = st.selectbox("Filter by Status", ["All", "pending", "in-progress", "done"])
    with f2:
        priority_filter = st.selectbox("Filter by Priority", ["All", "low", "medium", "high"])

    params = {}
    if status_filter != "All":
        params["status"] = status_filter
    if priority_filter != "All":
        params["priority"] = priority_filter

    status, tasks = api_call("GET", "/tasks", params=params)

    if search_text:
        tasks = [
            task for task in tasks
            if search_text.lower() in task.get("title", "").lower()
        ]
    
    if status != 200:
        st.error("Could not load tasks.")
        return

    if not tasks:
        st.info("No tasks found. Add your first task.")
        return

    st.subheader("Your Tasks")

    for task in tasks:
        task_id = task.get("id")
        title = task.get("title", "Untitled")
        description = task.get("description", "")
        priority = task.get("priority", "low")
        task_status = task.get("status", "pending")
        due_date = task.get("due_date", "No due date")

        with st.container():
            st.markdown(f"""
            <div class="task-card">
                <h4>{title}</h4>
                <p>{description}</p>
                <b>Priority:</b> {priority} &nbsp; | &nbsp;
                <b>Status:</b> {task_status} &nbsp; | &nbsp;
                <b>Due:</b> {due_date}
            </div>
            """, unsafe_allow_html=True)

            a1, a2, a3, a4, a5 = st.columns([1,1,1,1,1])
           

            with a1:
                if st.button("Mark Done", key=f"done_{task_id}"):
                    status, data = api_call("PATCH", f"/tasks/{task_id}/status", {
                        "status": "done"
                    })
                    if status == 200:
                        st.success("Task marked as done.")
                        st.rerun()
                    else:
                        st.error(data.get("detail", "Could not update task."))

            with a2:
                if st.button("In Progress", key=f"progress_{task_id}"):
                    status, data = api_call("PATCH", f"/tasks/{task_id}/status", {
                        "status": "in-progress"
                    })
                    if status == 200:
                        st.success("Task updated.")
                        st.rerun()
                    else:
                        st.error(data.get("detail", "Could not update task."))

            with a3:
                if st.button("Delete", key=f"delete_{task_id}"):
                    status, data = api_call("DELETE", f"/tasks/{task_id}")
                    if status in [200, 204]:
                        st.warning("Task deleted.")
                        st.rerun()
                    else:
                        st.error(data.get("detail", "Could not delete task."))
            with a4:
                if st.button("Edit", key=f"edit_{task_id}"):
                    st.session_state.edit_task_id = task_id
                    st.session_state.page = "Edit Task"
                    st.rerun()
            with a5:
                if st.button("View", key=f"view_{task_id}"):
                    st.session_state.view_task_id = task_id
                    st.session_state.page = "Task Details"
                    st.rerun()


# ---------------- ADD TASK ----------------
def add_task_page():
    st.subheader("Add New Task")

    with st.form("add_task_form"):
        title = st.text_input("Task Title")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["low", "medium", "high"])
        task_status = st.selectbox("Status", ["pending", "in-progress", "done"])
        due = st.date_input("Due Date", value=date.today())

        submit = st.form_submit_button("Add Task", use_container_width=True)

        if submit:
            if not title.strip():
                st.error("Task title is required.")
            else:
                payload = {
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "status": task_status,
                    "due_date": str(due)
                }

                status, data = api_call("POST", "/tasks", payload)

                if status in [200, 201]:
                    st.success("Task added successfully.")
                    st.session_state.page = "Dashboard"
                    st.rerun()
                else:
                    st.error(data.get("detail", "Could not add task."))



# ------------EDIT PAGE--------------
def edit_task_page():
    st.subheader("Edit Task")

    task_id = st.session_state.get("edit_task_id")

    if not task_id:
        st.error("No task selected.")
        st.session_state.page = "Dashboard"
        st.rerun()

    status, task = api_call("GET", f"/tasks/{task_id}")

    if status != 200:
        st.error(task.get("detail", "Could not load task."))
        if st.button("Back to Dashboard"):
            st.session_state.page = "Dashboard"
            st.rerun()
        return

    with st.form("edit_task_form"):
        title = st.text_input("Task Title", value=task.get("title", ""))
        description = st.text_area("Description", value=task.get("description", ""))
        priority = st.selectbox(
            "Priority",
            ["low", "medium", "high"],
            index=["low", "medium", "high"].index(task.get("priority", "low"))
        )
        task_status = st.selectbox(
            "Status",
            ["pending", "in-progress", "done"],
            index=["pending", "in-progress", "done"].index(task.get("status", "pending"))
        )
        due_date = st.text_input("Due Date", value=task.get("due_date", ""))

        submit = st.form_submit_button("Update Task", use_container_width=True)

        if submit:
            if not title.strip():
                st.error("Task title is required.")
            else:
                payload = {
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "status": task_status,
                    "due_date": due_date
                }

                status, data = api_call("PUT", f"/tasks/{task_id}", payload)

                if status == 200:
                    st.success("Task updated successfully.")
                    st.session_state.page = "Dashboard"
                    st.rerun()
                else:
                    st.error(data.get("detail", "Could not update task."))

    if st.button("Cancel"):
        st.session_state.page = "Dashboard"
        st.rerun()

# ------------- TASKDETAILS -------------
def task_details_page():
    st.subheader("Task Details")

    task_id = st.session_state.get("view_task_id")

    if not task_id:
        st.error("No task selected.")
        if st.button("Back"):
            st.session_state.page = "Dashboard"
            st.rerun()
        return

    status, task = api_call("GET", f"/tasks/{task_id}")

    if status != 200:
        st.error(task.get("detail", "Could not load task"))
        if st.button("Back"):
            st.session_state.page = "Dashboard"
            st.rerun()
        return

    st.markdown("### " + task.get("title", ""))

    st.write("**Description:**")
    st.write(task.get("description", ""))

    st.write("**Priority:**", task.get("priority", ""))

    st.write("**Status:**", task.get("status", ""))

    st.write("**Due Date:**", task.get("due_date", ""))

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("Edit Task"):
            st.session_state.edit_task_id = task_id
            st.session_state.page = "Edit Task"
            st.rerun()

    with c2:
        if st.button("Delete Task"):
            status, data = api_call("DELETE", f"/tasks/{task_id}")

            if status == 200:
                st.success("Task deleted.")
                st.session_state.page = "Dashboard"
                st.rerun()

    with c3:
        if st.button("Back"):
            st.session_state.page = "Dashboard"
            st.rerun()
# ---------------- PROFILE ----------------
def profile_page():
    st.subheader("Profile")

    status, data = api_call("GET", "/auth/me")
    task_status, tasks = api_call("GET", "/tasks")

    if status == 200:
        total = len(tasks) if task_status == 200 else 0
        pending = len([t for t in tasks if t.get("status") == "pending"]) if task_status == 200 else 0
        completed = len([t for t in tasks if t.get("status") == "done"]) if task_status == 200 else 0

        st.info("👤 User Information")

        c1, c2, c3 = st.columns(3)
        c1.metric("📋 Total Tasks", total)
        c2.metric("⏳ Pending Tasks", pending)
        c3.metric("✅ Completed Tasks", completed)

        st.markdown("---")
        st.write("**Email:**", data.get("email", st.session_state.email))
        st.write("**Account Status:** Active")
        st.write("**Project:** Personal Task Manager")

    else:
        st.error("Could not load profile.")

# ---------------- HELP ----------------
def help_page():
    st.subheader("Help Section")

    st.markdown("""
    ### How to use this app

    **1. Register/Login**  
    Create an account and login securely.

    **2. Add Tasks**  
    Add title, description, priority, status, and due date.

    **3. Manage Tasks**  
    View tasks in dashboard, filter them, mark as done, or delete.

    **4. Track Progress**  
    Dashboard cards show total, pending, in-progress, and completed tasks.

    ### Demo Flow
    Register → Login → Add Task → Filter → Mark Done → Delete → Logout
    """)


# ---------------- PAGE ROUTING ----------------
if st.session_state.page == "Login":
    login_page()
elif st.session_state.page == "Register":
    register_page()
elif st.session_state.page == "Dashboard":
    dashboard_page()
elif st.session_state.page == "Add Task":
    add_task_page()
elif st.session_state.page == "Edit Task":
    edit_task_page()
elif st.session_state.page == "Task Details":
    task_details_page()
elif st.session_state.page == "Profile":
    profile_page()
elif st.session_state.page == "Help":
    help_page()


# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
Personal Task Manager | FastAPI + SQLite + Streamlit
</div>
""", unsafe_allow_html=True)