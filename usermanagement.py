import streamlit as st
from db_userm import fetch_all_data, delete_record

def display_user_management():
    st.markdown("""
        <style>
        .data-row {
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
            background-color: #f9f9f9;
            color: #333;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .delete-icon {
            cursor: pointer;
            transition: transform 0.2s;
        }
        .delete-icon:hover {
            transform: scale(1.2);
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("User Data Management")

    # Fetch all data from the database
    data = fetch_all_data()

    # Display the data in a table format
    if data:
        st.write("### User Data")
        for row in data:
            st.markdown(f"""
                <div class="data-row">
                    <div>
                        <p><strong>ID:</strong> {row['id']}</p>
                        <p><strong>Name:</strong> {row['name']}</p>
                        <p><strong>Username:</strong> {row['username']}</p>
                        <p><strong>Password:</strong> {row['password']}</p>
                        <p><strong>Contact:</strong> {row['contact']}</p>
                        <p><strong>Gender:</strong> {row['gender']}</p>
                    </div>
                    <img src="https://img.icons8.com/material-outlined/24/000000/trash.png" 
                         class="delete-icon" 
                         alt="Delete icon" 
                         onclick="document.getElementById('delete-{row['id']}').click();">
                    <form id="delete-{row['id']}" method="post" style="display:none;">
                        <input type="hidden" name="record_id" value="{row['id']}">
                    </form>
                </div>
                """, unsafe_allow_html=True)

            # When the delete icon is clicked, ask for confirmation
            if st.session_state.get(f"confirm_delete_{row['id']}", False):
                st.write(f"Do you really want to delete {row['name']}?")
                if st.button(f"Yes, delete {row['name']}", key=f"confirm_yes_{row['id']}"):
                    delete_record(row['id'])
                    st.success(f"Deleted record with ID: {row['id']}")
                    
                    # Instead of st.experimental_rerun(), we use session state to trigger a refresh
                    st.session_state['refresh'] = True
                    
                if st.button(f"No", key=f"confirm_no_{row['id']}"):
                    st.session_state[f"confirm_delete_{row['id']}"] = False

            if st.button(f"Delete {row['name']}", key=f"delete_button_{row['id']}"):
                st.session_state[f"confirm_delete_{row['id']}"] = True

    else:
        st.write("No data available.")
    
    # Handle page refresh
    if 'refresh' in st.session_state and st.session_state['refresh']:
        st.session_state['refresh'] = False
        # Re-fetch data to refresh the displayed information
        data = fetch_all_data()  # Refresh data

    # Logout button
    if st.button("Logout", key="logout_button"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("You are logged out safely!")

# Ensure to use the latest Streamlit version
if __name__ == "__main__":
    display_user_management()
