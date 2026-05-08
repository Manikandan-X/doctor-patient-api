import time

# ✅ Example task 1: Logging
def log_appointment_creation(doctor_id: int):
    time.sleep(2)  # simulate delay
    print(f"Appointment created for doctor {doctor_id}")


# ✅ Example task 2: Email simulation
def send_email_notification(email: str):
    time.sleep(3)
    print(f"Email sent to {email}")


# ✅ Example task 3: File processing
def process_uploaded_file(filename: str):
    time.sleep(2)
    print(f"File processed: {filename}")