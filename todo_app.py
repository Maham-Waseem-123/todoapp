import streamlit as st
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Ultimate Todo List",
    page_icon="✅",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling with black text in inputs and task details
st.markdown("""
<style>
    :root {
        --primary: #4a00e0;
        --secondary: #8e2de2;
        --accent: #00c9ff;
        --light: #f5f5f5;
        --dark: #121212;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: var(--light);
        min-height: 100vh;
    }
    
    /* Input fields with black text */
    .stTextInput>div>div>input, 
    .stDateInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: black !important;
        border-radius: 10px !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Placeholder text */
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #555 !important;
    }
    
    /* Active task details text */
    .todo-item, .todo-item * {
        color: black !important;
    }
    
    .task-description {
        color: rgba(0, 0, 0, 0.85) !important;
        margin: 8px 0;
        font-size: 0.95rem;
        line-height: 1.4;
    }
    
    .task-details {
        display: flex;
        gap: 15px;
        margin-top: 8px;
        font-size: 0.9em;
        color: rgba(0, 0, 0, 0.75) !important;
    }
    
    .stButton>button {
        background: linear-gradient(to right, var(--accent), #92fe9d) !important;
        color: var(--dark) !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        padding: 10px 24px !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    .todo-item {
        background: rgba(255, 255, 255, 0.85) !important;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        transition: all 0.3s ease;
        border-left: 4px solid var(--accent);
    }
    
    .todo-item:hover {
        background: rgba(255, 255, 255, 0.95) !important;
        transform: translateX(5px);
    }
    
    .completed {
        opacity: 0.7;
        border-left-color: #00ff00 !important;
    }
    
    .header {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .header h1 {
        font-size: 3rem;
        background: linear-gradient(to right, var(--accent), #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    .priority-high { border-left: 4px solid #ff4b4b !important; }
    .priority-medium { border-left: 4px solid #ffa500 !important; }
    .priority-low { border-left: 4px solid #4ade80 !important; }
    
    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 20px;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
    }
    
    .empty-state {
        text-align: center;
        padding: 40px;
        opacity: 0.7;
        color: rgba(255, 255, 255, 0.8);
    }
    
    .empty-state i {
        font-size: 5rem;
        margin-bottom: 20px;
        opacity: 0.5;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'todos' not in st.session_state:
    st.session_state.todos = []
if 'completed' not in st.session_state:
    st.session_state.completed = []
# Add unique ID counter
if 'next_id' not in st.session_state:
    st.session_state.next_id = 1

# Initialize form fields in session state
if 'new_todo' not in st.session_state:
    st.session_state.new_todo = ""
if 'task_description' not in st.session_state:
    st.session_state.task_description = ""
if 'priority_level' not in st.session_state:
    st.session_state.priority_level = "Medium"
if 'due_date' not in st.session_state:
    st.session_state.due_date = datetime.now().date() + timedelta(days=7)

# Add new todo
def add_todo():
    if st.session_state.new_todo.strip() != "":
        new_task = {
            "id": st.session_state.next_id,
            "task": st.session_state.new_todo,
            "date": st.session_state.due_date,
            "priority": st.session_state.priority_level,
            "created": datetime.now(),
            "completed": False,
            "description": st.session_state.task_description
        }
        st.session_state.todos.append(new_task)
        st.session_state.next_id += 1  # Increment ID for next item
        
        # Reset form fields
        st.session_state.new_todo = ""
        st.session_state.task_description = ""
        st.session_state.priority_level = "Medium"
        st.session_state.due_date = datetime.now().date() + timedelta(days=7)

# Complete todo
def complete_todo(todo_id):
    for todo in st.session_state.todos:
        if todo["id"] == todo_id:
            todo["completed"] = True
            todo["completed_time"] = datetime.now()
            st.session_state.completed.append(todo)
            st.session_state.todos = [t for t in st.session_state.todos if t["id"] != todo_id]
            break

# Delete todo
def delete_todo(todo_id, completed=False):
    if completed:
        st.session_state.completed = [t for t in st.session_state.completed if t["id"] != todo_id]
    else:
        st.session_state.todos = [t for t in st.session_state.todos if t["id"] != todo_id]

# UI Components
st.markdown('<div class="header"><h1>✨ Ultimate Todo List</h1></div>', unsafe_allow_html=True)

# Add new todo form
with st.expander("➕ Add New Task", expanded=True):
    st.text_input("Task Title*", key="new_todo", placeholder="What needs to be done?")
    st.text_area("Description", key="task_description", placeholder="Add details...")
    
    cols = st.columns(3)
    with cols[0]:
        st.date_input("Due Date", 
                     key="due_date", 
                     min_value=datetime.now().date())
    with cols[1]:
        st.selectbox("Priority", ["High", "Medium", "Low"], key="priority_level")
    with cols[2]:
        st.write("")  # For alignment
        st.write("")
        st.button("Add Task", on_click=add_todo, use_container_width=True)

# Display active todos
st.subheader(f"📋 Active Tasks ({len(st.session_state.todos)})")
if not st.session_state.todos:
    st.markdown("""
    <div class="empty-state">
        <div>📭</div>
        <h3>No tasks yet</h3>
        <p>Add your first task to get started!</p>
    </div>
    """, unsafe_allow_html=True)

for todo in st.session_state.todos:
    with st.container():
        col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
        with col1:
            # Create task details
            details_content = f"""
            <div class="todo-item priority-{todo['priority'].lower()}">
                <h4>{todo['task']}</h4>
            """
            
            # Add description if it exists (blank if empty)
            if todo.get('description') and todo['description'].strip() != "":
                details_content += f"""<div class="task-description">{todo['description']}</div>"""
            else:
                details_content += """<div class="task-description" style="color:transparent!important">.</div>"""
            
            # Add task metadata
            priority_icon = "🔴" if todo['priority'] == "High" else "🟡" if todo['priority'] == "Medium" else "🟢"
            due_date_str = f"📅 {todo['date'].strftime('%b %d, %Y')}" if todo['date'] else ""
            
            details_content += f"""
                <div class="task-details">
                    <span>{priority_icon} {todo['priority']}</span>
                    <span>{due_date_str}</span>
                </div>
            </div>
            """
            
            st.markdown(details_content, unsafe_allow_html=True)
        with col2:
            if st.button("✓", key=f"complete_{todo['id']}", help="Mark as complete"):
                complete_todo(todo['id'])
        with col3:
            if st.button("🗑️", key=f"delete_{todo['id']}", help="Delete task"):
                delete_todo(todo['id'])

# Display completed todos
st.subheader(f"✅ Completed Tasks ({len(st.session_state.completed)})")
if not st.session_state.completed:
    st.markdown("""
    <div class="empty-state">
        <div>🎯</div>
        <h3>No completed tasks</h3>
        <p>Complete some tasks to see them here!</p>
    </div>
    """, unsafe_allow_html=True)
    
for todo in st.session_state.completed:
    with st.container():
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            completion_time = todo.get("completed_time", datetime.now())
            time_str = completion_time.strftime("%b %d, %I:%M %p")
            
            details_content = f"""
            <div class="todo-item completed">
                <h4 style="text-decoration: line-through;">{todo['task']}</h4>
            """
            
            # Add description if it exists (blank if empty)
            if todo.get('description') and todo['description'].strip() != "":
                details_content += f"""<div class="task-description" style="text-decoration:line-through">{todo['description']}</div>"""
            else:
                details_content += """<div class="task-description" style="color:transparent!important;text-decoration:line-through">.</div>"""
            
            details_content += f"""
                <div class="task-details">
                    <span>🎉 Completed: {time_str}</span>
                </div>
            </div>
            """
            
            st.markdown(details_content, unsafe_allow_html=True)
        with col2:
            if st.button("🗑️", key=f"del_completed_{todo['id']}", help="Delete task"):
                delete_todo(todo['id'], completed=True)

# Progress stats
total_tasks = len(st.session_state.todos) + len(st.session_state.completed)
completion_rate = (len(st.session_state.completed) / total_tasks) * 100 if total_tasks > 0 else 0

st.divider()
st.subheader("📈 Progress Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Active Tasks", len(st.session_state.todos))
col2.metric("Completed Tasks", len(st.session_state.completed))
col3.metric("Completion Rate", f"{completion_rate:.1f}%")

# Footer
st.markdown("---")
st.markdown(
    '<div class="footer">✨ Stay organized and productive! | Made with Streamlit</div>', 
    unsafe_allow_html=True
)
