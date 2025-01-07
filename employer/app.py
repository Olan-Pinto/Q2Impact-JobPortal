# Importing Libraries
from email.message import EmailMessage
import ssl
import smtplib
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import Flask, render_template, request, redirect, url_for, session,flash,Response
import pandas as pd
import re
from io import BytesIO

load_dotenv()

email_sender='q2impactdemo@gmail.com' #this accounts sends an email to 'admin' to verify the employer
email_password=os.getenv("MY_PASSWORD") #password of q2impactdemo@gmail.com (got from gmail)
ADMIN_USERNAME=os.getenv("ADMIN_USERNAME") #admin username
ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD") #admin password
email_receiver='olanpinto@gmail.com' #change this to suleimans email - or admins email

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Q2Impact.db' #Databse Name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class User(db.Model):
    """
    Represents a user in the database.

    Attributes:
        id (int): The unique identifier for the user, automatically incremented.
        email (str): The user's email address, which must be unique and is required.
        password (str): The user's hashed password, which is required.
        authenticated (bool): Indicates whether the user is authenticated. Defaults to False.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

class JobPosting(db.Model):
    """
    Represents a job posting record in the database.

    # Not adding attribute explanation now incase this changes in the future
    """
    __tablename__ = 'job_posting'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.String(10))
    end_date = db.Column(db.String(10))
    record_date = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    governorate = db.Column(db.String(100))
    district = db.Column(db.String(100))
    registered = db.Column(db.String(10))
    registration_type = db.Column(db.String(100))
    business_name = db.Column(db.String(255))
    economic_sector = db.Column(db.String(100))
    sub_sector = db.Column(db.String(100))
    products_services = db.Column(db.String(255))
    phone_number=db.Column(db.String(255))
    business_phone_number=db.Column(db.String(255))
    enterprize_size=db.Column(db.String(255))
    micro_small_medium_large=db.Column(db.String(255))
    current_available_vacancies=db.Column(db.String(10))
    number_of_vacancies=db.Column(db.Float)
    current_interns=db.Column(db.Float)
    current_seasonal_employees=db.Column(db.Float)
    current_entry_level=db.Column(db.Float)
    current_mid_senior_level=db.Column(db.Float)
    current_senior_management_level=db.Column(db.Float)
    current_customer_service_representatives=db.Column(db.Float)
    current_sales=db.Column(db.Float)
    current_information_technology=db.Column(db.Float)
    current_marketing=db.Column(db.Float)
    current_admin_staff=db.Column(db.Float)
    current_finance=db.Column(db.Float)
    current_operational_staff=db.Column(db.Float)
    current_technical_staff=db.Column(db.Float)
    current_others=db.Column(db.Float)
    current_please_specify=db.Column(db.String(255))
    consider_youth=db.Column(db.String(255))
    need_next_year=db.Column(db.String(255))
    expected_vacancies=db.Column(db.Float)
    future_interns=db.Column(db.Float)
    future_seasonal_employees=db.Column(db.Float)
    future_entry_level=db.Column(db.Float)
    future_mid_senior_level=db.Column(db.Float)
    future_senior_management_level=db.Column(db.Float)
    future_total=db.Column(db.Float)
    future_customer_service_representatives=db.Column(db.Float)
    future_sales=db.Column(db.Float)
    future_information_technology=db.Column(db.Float)
    future_marketing=db.Column(db.Float)
    future_admin_staff=db.Column(db.Float)
    future_finance=db.Column(db.Float)
    future_operational_staff=db.Column(db.Float)
    future_technical_staff=db.Column(db.Float)
    future_others=db.Column(db.Float)
    future_please_specify=db.Column(db.String(255))


with app.app_context():
    db.create_all()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handles the user signup process.

    This function performs the following steps:
    1. Validates the form inputs:
       - Ensures passwords match.
       - Checks password strength to meet security requirements.
       - Verifies email uniqueness.
    2. Hashes the user's password for secure storage.
    3. Creates a new user record in the database.
    4. Sends an email notification to the admin for user approval.
    5. Provides feedback to the user with flash messages.
    6. Redirects to the login page upon successful registration.

    Returns:
        Response: Renders the signup form (GET request) or redirects 
        the user to the appropriate page (POST request).
    """
    if request.method == 'POST':
        # Get the email from the form
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('signup'))
        
        password_regex = re.compile(r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")

        if not password_regex.match(password):
            flash("Password must contain at least 1 uppercase letter, 1 number, 1 symbol, and be at least 8 characters long.", "error")
            return redirect(url_for('signup'))
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("This email is already registered. Please log in or use a different email.", "error")
            return render_template('signup.html')
        hashed_password = generate_password_hash(password)

        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()


        subject='test'
        body=f"""
        Dear Suleiman, please Authenticate {email} from http://127.0.0.1:5000/admin/dashboard!
        """

        em=EmailMessage()
        em['From']=email_sender
        em['To']=email_receiver
        em['Subject']=subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_receiver,em.as_string())
        flash("Signup successful! Please wait for admin approval.", "success")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Fetch user from database
        user = User.query.filter_by(email=email).first()

        # Validate credentials and authentication status
        if user and check_password_hash(user.password, password):
            if user.authenticated:
                session['user_logged_in'] = email  # Save user session
                return redirect(url_for('main_page'))
            else:
                error = "Your account is not authenticated. Please contact admin."
        else:
            error = "Invalid username or password."
        return render_template('login.html', error=error)
    return render_template('login.html')

# This dictionary helps for error handling - Ensures the user inputs the content in the Excel file as expected
expected_types = {
    'start_date': ['object'],
    'end_date': ['object'],
    'record_date': ['object'],
    'latitude': ['float64','int64'],
    'longitude': ['float64','int64'],
    'governorate': ['object'],
    'district': ['object'],
    'registered': ['object'],
    'registration_type': ['object'],
    'business_name': ['object'],
    'economic_sector': ['object'],
    'sub_sector': ['object'],
    'products_services': ['object'],
    'phone_number': ['object'],
    'business_phone_number': ['object'],
    'enterprize_size': ['object'],
    'micro_small_medium_large': ['object'],
    'current_available_vacancies': ['object'],
    'number_of_vacancies': ['float64','int64'],
    'current_interns':['float64','int64'],
    'current_seasonal_employees':['float64','int64'],
    'current_entry_level':['float64','int64'],
    'current_mid_senior_level':['float64','int64'],
    'current_senior_management_level':['float64','int64'],
    'current_customer_service_representatives':['float64','int64'],
    'current_sales':['float64','int64'],
    'current_information_technology':['float64','int64'],
    'current_marketing':['float64','int64'],
    'current_admin_staff':['float64','int64'],
    'current_finance':['float64','int64'],
    'current_operational_staff':['float64','int64'],
    'current_technical_staff':['float64','int64'],
    'current_others':['float64','int64'],
    'current_please_specify':['object'],
    'consider_youth':['object'],
    'need_next_year':['object'],
    'expected_vacancies':['float64','int64'],
    'future_interns':['float64','int64'],
    'future_seasonal_employees':['float64','int64'],
    'future_entry_level':['float64','int64'],
    'future_mid_senior_level':['float64','int64'],
    'future_senior_management_level':['float64','int64'],
    'future_total':['float64','int64'],
    'future_customer_service_representatives':['float64','int64'],
    'future_sales':['float64','int64'],
    'future_information_technology':['float64','int64'],
    'future_marketing':['float64','int64'],
    'future_admin_staff':['float64','int64'],
    'future_finance':['float64','int64'],
    'future_operational_staff':['float64','int64'],
    'future_technical_staff':['float64','int64'],
    'future_others':['float64','int64'],
    'future_please_specify':['object'],
}


@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    """
    Handles the file upload and processing for job postings.

    This function allows users to upload an Excel file (.xlsx) containing job posting data.
    It performs the following steps:
    
    1. Checks if a file is uploaded and validates the file extension.
    2. Reads the Excel file using pandas, ensuring all date and other columns are appropriately formatted.
    3. Validates the uploaded data:
       - Ensures all required columns are present.
       - Verifies that column data types match the expected types.
       - Fills missing values with default values based on the column type.
    4. Creates `JobPosting` instances for each row in the file and inserts them into the database.
    5. Handles any errors during file reading, validation, or database insertion, and provides feedback to the user.

    Returns:
        Response: Renders the main page with appropriate success or error messages, depending on the result of the file processing.
    """
    if request.method == 'POST':
        file = request.files.get('file')

        # Check if a file is uploaded
        if not file:
            return render_template('main_page.html', success="No file uploaded.")

        # Validate file extension
        if not file.filename.lower().endswith('.xlsx'):
            return render_template('main_page.html', success="Please upload a valid XLSX file.")

        try:
            df = pd.read_excel(file,engine='openpyxl')
            date_columns = ['start_date', 'end_date', 'record_date']
            for col in date_columns:
                if col in df.columns:
                    df[col] = df[col].astype(str)
            for col in df.columns:
                df[col]=df[col].astype(expected_types[col][0])
                if(expected_types[col][0]=='float64'):
                    df[col].fillna(0,inplace=True)
                else:
                    df[col].fillna('No Input',inplace=True)
                if(df[col].dtypes not in expected_types[col]):
                    return render_template('main_page.html', success=f"Data in the column '{col}' is not in the right format. Please reupload a correct Excel file")
            
            required_columns = [
                'start_date', 'end_date', 'record_date', 'latitude', 'longitude',
                'governorate', 'district', 'registered', 'registration_type', 'business_name',
                'economic_sector', 'sub_sector', 'products_services', 'phone_number',
                'business_phone_number', 'enterprize_size', 'micro_small_medium_large',
                'current_available_vacancies', 'number_of_vacancies', 'current_interns',
                'current_seasonal_employees', 'current_entry_level', 'current_mid_senior_level',
                'current_senior_management_level', 'current_customer_service_representatives',
                'current_sales', 'current_information_technology', 'current_marketing',
                'current_admin_staff', 'current_finance', 'current_operational_staff',
                'current_technical_staff', 'current_others', 'current_please_specify',
                'consider_youth', 'need_next_year', 'expected_vacancies', 'future_interns',
                'future_seasonal_employees', 'future_entry_level', 'future_mid_senior_level',
                'future_senior_management_level', 'future_total', 'future_customer_service_representatives',
                'future_sales', 'future_information_technology', 'future_marketing', 'future_admin_staff',
                'future_finance', 'future_operational_staff', 'future_technical_staff',
                'future_others', 'future_please_specify'
            ]
            if not all(col in df.columns for col in required_columns):
                missing_cols = [col for col in required_columns if col not in df.columns]
                return render_template('main_page.html', success=f"Missing columns in CSV: {', '.join(missing_cols)}")
            # Create JobPosting instances from DataFrame
            job_postings = [
                JobPosting(
                    start_date=str(row['start_date']),
                    end_date=str(row['end_date']),
                    record_date=str(row['record_date']),
                    latitude=row['latitude'],
                    longitude=row['longitude'],
                    governorate=row['governorate'],
                    district=row['district'],
                    registered=row['registered'],
                    registration_type=row['registration_type'],
                    business_name=row['business_name'],
                    economic_sector=row['economic_sector'],
                    sub_sector=row['sub_sector'],
                    products_services=row['products_services'],
                    phone_number=row['phone_number'],
                    business_phone_number=row['business_phone_number'],
                    enterprize_size=row['enterprize_size'],
                    micro_small_medium_large=row['micro_small_medium_large'],
                    current_available_vacancies=row['current_available_vacancies'],
                    number_of_vacancies=row['number_of_vacancies'],
                    current_interns=row['current_interns'],
                    current_seasonal_employees=row['current_seasonal_employees'],
                    current_entry_level=row['current_entry_level'],
                    current_mid_senior_level=row['current_mid_senior_level'],
                    current_senior_management_level=row['current_senior_management_level'],
                    current_customer_service_representatives=row['current_customer_service_representatives'],
                    current_sales=row['current_sales'],
                    current_information_technology=row['current_information_technology'],
                    current_marketing=row['current_marketing'],
                    current_admin_staff=row['current_admin_staff'],
                    current_finance=row['current_finance'],
                    current_operational_staff=row['current_operational_staff'],
                    current_technical_staff=row['current_technical_staff'],
                    current_others=row['current_others'],
                    current_please_specify=row['current_please_specify'],
                    consider_youth=row['consider_youth'],
                    need_next_year=row['need_next_year'],
                    expected_vacancies=row['expected_vacancies'],
                    future_interns=row['future_interns'],
                    future_seasonal_employees=row['future_seasonal_employees'],
                    future_entry_level=row['future_entry_level'],
                    future_mid_senior_level=row['future_mid_senior_level'],
                    future_senior_management_level=row['future_senior_management_level'],
                    future_total=row['future_total'],
                    future_customer_service_representatives=row['future_customer_service_representatives'],
                    future_sales=row['future_sales'],
                    future_information_technology=row['future_information_technology'],
                    future_marketing=row['future_marketing'],
                    future_admin_staff=row['future_admin_staff'],
                    future_finance=row['future_finance'],
                    future_operational_staff=row['future_operational_staff'],
                    future_technical_staff=row['future_technical_staff'],
                    future_others=row['future_others'],
                    future_please_specify=row['future_please_specify']
                )
                for _, row in df.iterrows()
            ]
            # Add all rows to the session
            db.session.bulk_save_objects(job_postings)
            db.session.commit()
            success = "CSV uploaded and data inserted successfully!"

        except Exception as e:
            
            db.session.rollback()
            success = f"Please check your Excel file once again and ensure the data matches the column name"

        return render_template('main_page.html', success=success)

    return render_template('main_page.html')


# Route to log out
@app.route('/logout')
def logout():
    session.pop('user_logged_in', None)  # Clear user session
    return redirect(url_for('login'))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """
    Handles the login process for the admin user.

    This function verifies the admin's credentials and manages the admin session:
    
    1. Checks if the request method is POST.
    2. Retrieves the `username` and `password` from the submitted form.
    3. Validates the credentials against predefined constants (`ADMIN_USERNAME` and `ADMIN_PASSWORD`).
       - If the credentials are valid, sets a session flag (`admin_logged_in`) to indicate the admin is logged in and redirects to the admin dashboard.
       - If invalid, displays an error message on the login page.
    4. If the request method is not POST, renders the admin login page.

    Returns:
        Response: Renders the admin login page with or without an error message, 
        or redirects the admin to the dashboard upon successful login.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True  # Set admin session
            return redirect(url_for('admin_dashboard'))
        else:
            error = "Invalid username or password."
        return render_template('admin_login.html',error=error)
    return render_template('admin_login.html')

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    """
    Manages the admin dashboard functionality, including user authentication and deletion.

    This function handles GET and POST requests for the admin dashboard:
    
    1. **Authentication:**
       - Checks if the admin is logged in by verifying the `admin_logged_in` session flag.
       - If the admin is not logged in, redirects to the admin login page.
       - Handles POST requests where selected user IDs are authenticated:
         - Authenticates the selected users and commits the changes to the database.
         - Displays a success flash message with the number of authenticated users.
       
    2. **Deletion:**
       - Handles POST requests for user deletion:
         - Accepts a comma-separated list of user IDs to be deleted.
         - Deletes the corresponding job postings from the database.
         - Displays a success flash message with the number of deleted users, or an error message for invalid input.

    3. **Display:**
       - For GET requests, fetches all users with `authenticated=False` and renders the admin dashboard page.

    Returns:
        Response: Renders the admin dashboard page with a list of unauthenticated users 
        or redirects to the admin login page if the admin is not logged in.
    """
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    print(request.form)
    # Handle Authentication
    if request.method == 'POST' and 'user_ids' in request.form:
        user_ids = request.form.getlist('user_ids')  # Get selected user IDs
        for user_id in user_ids:
            user = User.query.get(user_id)
            if user:
                user.authenticated = True
                db.session.commit()
        flash(f"Authenticated {len(user_ids)} user(s).", 'success')
        return redirect(url_for('admin_dashboard'))  # Redirect to show the flash message

    # Handle Deletion
    if request.method == 'POST' and 'delete' in request.form:
        delete_input = request.form['delete']
        try:
            delete_ids = [int(id.strip()) for id in delete_input.split(',')]
            deleted_users = JobPosting.query.filter(JobPosting.id.in_(delete_ids)).all()
            for user in deleted_users:
                db.session.delete(user)
            db.session.commit()
            flash(f"Deleted {len(deleted_users)} user(s).", 'success')
        except ValueError:
            flash("Invalid input! Please provide comma-separated user IDs (e.g., 1, 2, 3).", 'error')
        return redirect(url_for('admin_dashboard'))  # Redirect to show the flash message

    # Get users with authenticated=False
    users_to_authenticate = User.query.filter_by(authenticated=False).all()
    return render_template('admin_dashboard.html', users=users_to_authenticate)


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)  # Remove admin session
    return redirect(url_for('admin_login'))

@app.route('/listings', methods=['GET'])
def listings():
    """
    Exports job postings data to an Excel file.

    This function retrieves all job postings from the database, converts them into a DataFrame, 
    and generates an Excel file for download:

    1. Queries all records from the `JobPosting` table in the database.
    2. Converts each record into a dictionary where keys are column names, and values are the respective data.
    3. Constructs a Pandas DataFrame from the list of dictionaries.
    4. Writes the DataFrame to an in-memory Excel file using the `xlsxwriter` engine.
    5. Prepares an HTTP response to serve the Excel file as a downloadable attachment.

    Returns:
        Response: An HTTP response containing the generated Excel file as an attachment with the filename `JobPostings.xlsx`.
    """
    query = db.session.query(JobPosting).all()
    job_list = [
        {
            column.name: getattr(job, column.name)
            for column in JobPosting.__table__.columns
        }
        for job in query
    ]
    df = pd.DataFrame(job_list)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Job Postings')

    output.seek(0)
    response = Response(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response.headers['Content-Disposition'] = 'attachment; filename=JobPostings.xlsx'
    return response


@app.context_processor
def utility_processor():
    return dict(getattr=getattr)

if __name__ == '__main__':
    app.run(debug=True)