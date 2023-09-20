## EXPERIMENTING WITH USER AUTHENTICATION AND SESSION STATES

## REGISTER AND AUTH APPROACH 1

import streamlit as st
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# Initialize an empty dictionary to store user credentials
user_credentials = {}

def main():
    st.title('User Login and Registration')

    # Add a registration form
    st.header('User Registration')
    new_username = st.text_input('New Username')
    new_password = st.text_input('New Password', type='password')

    if st.button('Register'):
        if new_username and new_password:
            # Check if the username already exists
            if new_username in user_credentials:
                st.error('Username already exists. Please choose a different one.')
            else:
                # Hash and store the new user's password
                hashed_password = hash_password(new_password)
                user_credentials[new_username] = hashed_password
                st.success(f'User "{new_username}" registered successfully. You can now log in.')

                # Print the updated user_credentials dictionary for debugging
                print("Updated user_credentials:", user_credentials)

    # Add a login form
    st.header('User Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if username in user_credentials:
            stored_hash = user_credentials[username]
            print(stored_hash)
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                st.success(f'Welcome, {username}!')
            else:
                st.error('Incorrect password')
        else:
            st.error('User not found')


if __name__ == '__main__':
    main()






## Approach 1

# import streamlit as st
# import bcrypt
#
# def hash_password(password):
#     salt = bcrypt.gensalt()
#     hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
#     return hashed
#
# user_credentials = {
#     'Will': hash_password('WillUTS'),
#     'Aks': hash_password('AksUTS'),
#     'Shali': hash_password('ShaliUTS'),
#     'Dee': hash_password('DeeUTS')
# }
#
# def main():
#     st.title('User Login')
#
#     username = st.text_input('Username')
#     password = st.text_input('Password', type='password')
#
#     if st.button('Login'):
#         if username in user_credentials:
#             stored_hash = user_credentials[username]
#             if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
#                 st.success(f'Welcome, {username}!')
#             else:
#                 st.error('Incorrect password')
#         else:
#             st.error('User not found')
#
# if __name__ == '__main__':
#     main()

## Approach 2

# # pip install streamlit-authenticator
# import streamlit as st
# import streamlit_authenticator as stauth
# import datetime
# import re
#
# def sign_uo():
#     with st.form(key = "signup", clear_on_submit=True):
#         st.subheader(":green[Sign up]")
#         email = st.text_input("Email", placeholder="Enter your email")
#         username = st.text_input("Username", placeholder="Enter your username")
#         password1 = st.text_input("Password", placeholder="Enter your password", type="password")
#         password2 = st.text_input("Confirm Password", placeholder="Confirm your password", type="password")
#
#     # Store credentials in cloud database Deta Space

## Approach 3
# import yaml
# import streamlit as st
# from yaml.loader import SafeLoader
# import streamlit.components.v1 as components
# import streamlit_authenticator as stauth
#
# def login():
#     names = ['Join Prime', 'Join Walmart plus']
#     usernames = ['amazon', 'walmart']
#     passwords = ['amazonpay', 'phonepe']
#     hashed_passwords = stauth.hasher(passwords).generate()
#     authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'some_cookie_name', 'some_signature_key',
#                                         cookie_expiry_days=30)
#     name, authentication_status, username = authenticator.login('Login', 'main')
#
#     if st.session_state["authentication_status"]:
#         test = authenticator.logout('Logout', 'main')
#         st.write(f'Welcome *{st.session_state["name"]}*')
#         st.title('Some content')
#     elif st.session_state["authentication_status"] == False:
#         st.error('Username/password is incorrect')
#     elif st.session_state["authentication_status"] == None:
#         st.warning('Please enter your username and password')
#
# def main():
#     login()
#
# if __name__ == "__main__":
#     main()

