from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash, current_app, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
import pandas as pd
import os
import tempfile
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect
from algoandpdf1 import assign_students_to_rooms, generate_pdf

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Generate a secure random key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = None  # No time limit for CSRF tokens

# Ensure the upload directory exists
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

csrf = CSRFProtect(app)
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Increased length for hash
    lt_count = db.Column(db.Integer, default=0)
    lt_rows = db.Column(db.Integer, default=0)
    lt_cols = db.Column(db.Integer, default=0)
    cr_count = db.Column(db.Integer, default=0)
    cr_rows = db.Column(db.Integer, default=0)
    cr_cols = db.Column(db.Integer, default=0)
    exam_date = db.Column(db.String(50))
    exam_subject = db.Column(db.String(100))
    timing = db.Column(db.String(50))
    shift = db.Column(db.String(50))
    exam_type = db.Column(db.String(50))

# Create tables
with app.app_context():
    db.create_all()

def clean_text(text):
    return text.replace("\u2013", "-").replace("–", "-") if isinstance(text, str) else text

def validate_room_data(form_data):
    try:
        for field in ['lt_count', 'lt_rows', 'lt_cols', 'cr_count', 'cr_rows', 'cr_cols']:
            value = int(form_data[field])
            if value < 0:
                raise ValueError(f"{field} cannot be negative")
        return True
    except (ValueError, KeyError) as e:
        flash(f"Invalid input: {str(e)}", "danger")
        return False

class EmptyForm(FlaskForm):
    pass

@app.route('/')
def home():
    return redirect(url_for('login' if 'username' not in session else 'index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = EmptyForm()
    if request.method == 'POST':
        try:
            username = request.form['username'].strip()
            password = request.form['password']
            
            if not username or not password:
                flash("Username and password are required!", "danger")
                return redirect(url_for('register'))
            
            if User.query.filter_by(username=username).first():
                flash("Username already exists!", "danger")
                return redirect(url_for('register'))
            
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Registration failed: {str(e)}", "danger")
            return redirect(url_for('register'))
            
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = EmptyForm()
    if request.method == 'POST':
        try:
            username = request.form['username'].strip()
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password, password):
                session.permanent = True
                session['username'] = username
                return redirect(url_for('index'))
            
            flash("Invalid credentials!", "danger")
        except Exception as e:
            flash(f"Login failed: {str(e)}", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        flash("Please login first", "danger")
        return redirect(url_for('login'))
    
    try:
        user = User.query.filter_by(username=session['username']).first()
        if not user:
            session.clear()
            flash("User not found", "danger")
            return redirect(url_for('login'))
        
        form = EmptyForm()
        
        if request.method == 'POST':
            print("POST request received")  # Debug log
            
            if not form.validate_on_submit():
                print("Form validation failed")  # Debug log
                flash("Form validation failed. Please try again.", "danger")
                return render_template('index.html', user=user, form=form, skip_splash=True)
            
            print("Form validation successful")  # Debug log
                
            if not validate_room_data(request.form):
                return render_template('index.html', user=user, form=form, skip_splash=True)
            
            # Update user data with form values
            try:
                user.lt_count = int(request.form['lt_count'])
                user.lt_rows = int(request.form['lt_rows'])
                user.lt_cols = int(request.form['lt_cols'])
                user.cr_count = int(request.form['cr_count'])
                user.cr_rows = int(request.form['cr_rows'])
                user.cr_cols = int(request.form['cr_cols'])
                user.exam_date = clean_text(request.form['exam_date'])
                user.exam_subject = clean_text(request.form['exam_subject'])
                user.exam_type = request.form.get('examType', '')
                user.shift = clean_text(request.form.get('shift', ''))
                user.timing = clean_text(request.form.get('duration', ''))
                
                db.session.commit()
                print("User data updated successfully")  # Debug log
            except Exception as e:
                print(f"Error updating user data: {str(e)}")  # Debug log
                db.session.rollback()
                flash("Error saving form data", "danger")
                return render_template('index.html', user=user, form=form, skip_splash=True)
            
            # File handling and PDF generation
            if 'file' not in request.files:
                print("No file in request")  # Debug log
                flash("No file uploaded", "danger")
                return render_template('index.html', user=user, form=form, skip_splash=True)
                
            file = request.files['file']
            if not file or file.filename == '':
                print("No file selected")  # Debug log
                flash("No file selected", "danger")
                return render_template('index.html', user=user, form=form, skip_splash=True)
                
            if not allowed_file(file.filename):
                print("Invalid file type")  # Debug log
                flash("Invalid file type. Please upload an Excel file.", "danger")
                return render_template('index.html', user=user, form=form, skip_splash=True)
            
            try:
                # Create a temporary file for the uploaded Excel
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_excel:
                    file.save(tmp_excel.name)
                    print(f"Excel file saved to {tmp_excel.name}")  # Debug log
                    
                    # Process Excel file
                    df = None
                    try:
                        df = pd.read_excel(tmp_excel.name)
                    except Exception as e:
                        os.unlink(tmp_excel.name)  # Delete the temp file if read fails
                        flash("Error reading Excel file: " + str(e), "danger")
                        return render_template('index.html', user=user, form=form, skip_splash=True)
                        
                    if df.empty:
                        os.unlink(tmp_excel.name)  # Delete the temp file if empty
                        flash("Excel file is empty", "danger")
                        return render_template('index.html', user=user, form=form, skip_splash=True)
                        
                    print("Excel file processed successfully")  # Debug log
                    
                    students = df.to_dict(orient='records')
                    students_dict = {i: student for i, student in enumerate(students)}
                    
                    # Clean up Excel file as we don't need it anymore
                    try:
                        os.unlink(tmp_excel.name)
                    except Exception as e:
                        print(f"Warning: Could not delete temp Excel file: {str(e)}")
                    
                    # Check seating capacity before generating arrangement
                    total_capacity = (user.lt_count * user.lt_rows * user.lt_cols) + (user.cr_count * user.cr_rows * user.cr_cols)
                    if len(students) > total_capacity:
                        flash(f"Not enough seats available. Need {len(students)} seats but only have {total_capacity} seats.", "danger")
                        return render_template('index.html', user=user, form=form, skip_splash=True)

                    # Generate seating arrangement
                    try:
                        rooms, student_lookup = assign_students_to_rooms(
                            students_dict, user.lt_count, user.cr_count, 
                            user.lt_rows, user.lt_cols, user.cr_rows, user.cr_cols
                        )
                        print("Seating arrangement generated")  # Debug log
                    except Exception as e:
                        flash(f"Error generating seating arrangement: {str(e)}", "danger")
                        return render_template('index.html', user=user, form=form, skip_splash=True)
                    
                    # Create a temporary file for the PDF
                    pdf_path = None
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
                            pdf_path = tmp_pdf.name
                        
                        # Generate PDF
                        generate_pdf(
                            rooms, student_lookup, "GRAPHIC ERA HILL UNIVERSITY",
                            user.exam_subject, user.exam_date, user.timing, user.shift, pdf_path
                        )
                        print(f"PDF generated at {pdf_path}")  # Debug log
                        
                        if not os.path.exists(pdf_path):
                            raise ValueError("PDF generation failed - file not found")
                        
                        print("Preparing to send file")  # Debug log
                        
                        # Read the PDF file
                        with open(pdf_path, 'rb') as pdf_file:
                            pdf_data = pdf_file.read()
                        
                        # Clean up PDF file
                        try:
                            os.unlink(pdf_path)
                        except Exception as e:
                            print(f"Warning: Could not delete temp PDF file: {str(e)}")
                        
                        # Create response with PDF data
                        response = make_response(pdf_data)
                        response.headers['Content-Type'] = 'application/pdf'
                        response.headers['Content-Disposition'] = f'attachment; filename=Seating_Arrangement_{user.exam_subject}.pdf'
                        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
                        response.headers["Pragma"] = "no-cache"
                        response.headers["Expires"] = "0"
                        
                        flash("PDF generated successfully!", "success")
                        return response
                        
                    except Exception as e:
                        # Clean up PDF file if it exists
                        if pdf_path and os.path.exists(pdf_path):
                            try:
                                os.unlink(pdf_path)
                            except:
                                pass
                        flash(f"Error generating PDF: {str(e)}", "danger")
                        return render_template('index.html', user=user, form=form, skip_splash=True)
                    
            except Exception as e:
                print(f"Error in PDF generation: {str(e)}")  # Debug log
                flash(f"Error generating PDF: {str(e)}", "danger")
                return render_template('index.html', user=user, form=form, skip_splash=True)
                    
        return render_template('index.html', user=user, form=form)
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debug log
        flash(f"An error occurred: {str(e)}", "danger")
        return render_template('index.html', user=user, form=form)

if __name__ == "__main__":
    app.run(debug=True)  # Set debug=False for production