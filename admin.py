from database import Database

class Admin:
    def __init__(self):
        self.db = Database()
    
    def view_all_patients(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, age, gender, contact, email FROM patients')
        patients = cursor.fetchall()
        conn.close()
        
        if patients:
            print("\n=== All Patients ===")
            for p in patients:
                print(f"ID: {p[0]}, Name: {p[1]}, Age: {p[2]}, Gender: {p[3]}, Contact: {p[4]}, Email: {p[5]}")
        else:
            print("No patients found.")
    
    def view_all_doctors(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, specialty, contact FROM doctors')
        doctors = cursor.fetchall()
        conn.close()
        
        if doctors:
            print("\n=== All Doctors ===")
            for d in doctors:
                print(f"ID: {d[0]}, Name: {d[1]}, Email: {d[2]}, Specialty: {d[3]}, Contact: {d[4]}")
        else:
            print("No doctors found.")
    
    def add_doctor(self):
        print("\n=== Add Doctor ===")
        name = input("Name: ")
        email = input("Email: ")
        password = input("Password: ")
        specialty = input("Specialty: ")
        contact = input("Contact: ")
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        hashed_password = self.db.hash_password(password)
        
        try:
            cursor.execute('INSERT INTO doctors (name, email, password, specialty, contact) VALUES (?, ?, ?, ?, ?)',
                          (name, email, hashed_password, specialty, contact))
            conn.commit()
            print("Doctor added successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()
    
    def view_appointments(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''SELECT a.id, p.name, d.name, a.date, a.time, a.status 
                         FROM appointments a 
                         JOIN patients p ON a.patient_id = p.id 
                         JOIN doctors d ON a.doctor_id = d.id''')
        appointments = cursor.fetchall()
        conn.close()
        
        if appointments:
            print("\n=== All Appointments ===")
            for a in appointments:
                print(f"ID: {a[0]}, Patient: {a[1]}, Doctor: {a[2]}, Date: {a[3]}, Time: {a[4]}, Status: {a[5]}")
        else:
            print("No appointments found.")
    
    def delete_patient(self):
        patient_id = input("Enter Patient ID to delete: ")
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
        if cursor.rowcount > 0:
            conn.commit()
            print("Patient deleted successfully!")
        else:
            print("Patient not found.")
        conn.close()
    
    def delete_doctor(self):
        doctor_id = input("Enter Doctor ID to delete: ")
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM doctors WHERE id = ?', (doctor_id,))
        if cursor.rowcount > 0:
            conn.commit()
            print("Doctor deleted successfully!")
        else:
            print("Doctor not found.")
        conn.close()