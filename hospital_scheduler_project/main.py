import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os

# -------------------------------
# Classes
# -------------------------------
class Doctor:
    def __init__(self, name, specialization, available_times):
        self.name = name
        self.specialization = specialization
        self.available_times = available_times
        self.patients = []

class Patient:
    def __init__(self, name, specialization, priority, appointment_time):
        self.name = name
        self.specialization = specialization
        self.priority = priority
        self.appointment_time = appointment_time

# -------------------------------
# GUI Application
# -------------------------------
class HospitalSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Resource Scheduler Pro")
        self.root.geometry("900x600")
        self.root.configure(bg="#f2f2f2")

        self.doctors = []
        self.patients = []
        self.time_slots = self.generate_time_slots()

        self.create_ui()
        self.load_data()
        self.update_clock()

    # Generate realistic time slots (3-hour intervals)
    def generate_time_slots(self):
        slots = []
        for hour in range(0, 24, 3):
            end_hour = (hour + 3) % 24
            slots.append(f"{hour:02}:00 - {end_hour:02}:00")
        return slots

    # Clock updater
    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    # UI setup
    def create_ui(self):
        title = tk.Label(self.root, text="Hospital Resource Scheduler Pro",
                         font=("Helvetica", 20, "bold"), bg="#f2f2f2", fg="#006d77")
        title.pack(pady=10)

        self.clock_label = tk.Label(self.root, font=("Helvetica", 12), bg="#f2f2f2", fg="#444")
        self.clock_label.pack()

        notebook = ttk.Notebook(self.root)
        notebook.pack(padx=10, pady=10, fill="both", expand=True)

        self.doctor_frame = ttk.Frame(notebook)
        self.patient_frame = ttk.Frame(notebook)
        self.dashboard_frame = ttk.Frame(notebook)

        notebook.add(self.doctor_frame, text="Add Doctor")
        notebook.add(self.patient_frame, text="Add Patient")
        notebook.add(self.dashboard_frame, text="Dashboard")

        self.create_doctor_tab()
        self.create_patient_tab()
        self.create_dashboard_tab()

        # Buttons under the notebook
        btn_frame = tk.Frame(self.root, bg="#f2f2f2")
        btn_frame.pack(pady=10)

        report_btn = tk.Button(btn_frame, text="View Report", command=self.show_report,
                               bg="#83c5be", fg="black", font=("Helvetica", 11, "bold"),
                               relief="raised", cursor="hand2", width=15)
        report_btn.grid(row=0, column=0, padx=10)
        report_btn.bind("<Enter>", lambda e: report_btn.config(bg="#4cbbb9"))
        report_btn.bind("<Leave>", lambda e: report_btn.config(bg="#83c5be"))

        reset_btn = tk.Button(btn_frame, text="Reset Assignments", command=self.reset_assignments,
                              bg="#ef476f", fg="white", font=("Helvetica", 11, "bold"),
                              relief="raised", cursor="hand2", width=18)
        reset_btn.grid(row=0, column=1, padx=10)
        reset_btn.bind("<Enter>", lambda e: reset_btn.config(bg="#d72638"))
        reset_btn.bind("<Leave>", lambda e: reset_btn.config(bg="#ef476f"))

    # Doctor tab
    def create_doctor_tab(self):
        tk.Label(self.doctor_frame, text="Doctor Name:", font=("Helvetica", 11)).grid(row=0, column=0, pady=10, sticky="e")
        tk.Label(self.doctor_frame, text="Specialization:", font=("Helvetica", 11)).grid(row=1, column=0, pady=10, sticky="e")
        tk.Label(self.doctor_frame, text="Available Time:", font=("Helvetica", 11)).grid(row=2, column=0, pady=10, sticky="e")

        self.doc_name = tk.Entry(self.doctor_frame, width=30)
        self.doc_name.grid(row=0, column=1)

        self.doc_specialization = ttk.Combobox(self.doctor_frame,
                                               values=["Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Emergency"],
                                               state="readonly")
        self.doc_specialization.grid(row=1, column=1)
        self.doc_specialization.current(0)

        self.doc_time = ttk.Combobox(self.doctor_frame, values=self.time_slots, state="readonly")
        self.doc_time.grid(row=2, column=1)
        self.doc_time.current(0)

        add_btn = tk.Button(self.doctor_frame, text="Add Doctor", command=self.add_doctor, bg="#006d77", fg="white",
                            font=("Helvetica", 11, "bold"), relief="raised", cursor="hand2")
        add_btn.grid(row=3, column=0, columnspan=2, pady=20)
        add_btn.bind("<Enter>", lambda e: add_btn.config(bg="#004f52"))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg="#006d77"))

    # Patient tab
    def create_patient_tab(self):
        tk.Label(self.patient_frame, text="Patient Name:", font=("Helvetica", 11)).grid(row=0, column=0, pady=10, sticky="e")
        tk.Label(self.patient_frame, text="Specialization Needed:", font=("Helvetica", 11)).grid(row=1, column=0, pady=10, sticky="e")
        tk.Label(self.patient_frame, text="Priority (1-5):", font=("Helvetica", 11)).grid(row=2, column=0, pady=10, sticky="e")
        tk.Label(self.patient_frame, text="Preferred Time:", font=("Helvetica", 11)).grid(row=3, column=0, pady=10, sticky="e")

        self.pat_name = tk.Entry(self.patient_frame, width=30)
        self.pat_name.grid(row=0, column=1)

        self.pat_specialization = ttk.Combobox(self.patient_frame,
                                               values=["Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Emergency"],
                                               state="readonly")
        self.pat_specialization.grid(row=1, column=1)
        self.pat_specialization.current(0)

        self.pat_priority = ttk.Combobox(self.patient_frame, values=["1", "2", "3", "4", "5"], state="readonly")
        self.pat_priority.grid(row=2, column=1)
        self.pat_priority.current(2)

        self.pat_time = ttk.Combobox(self.patient_frame, values=self.time_slots, state="readonly")
        self.pat_time.grid(row=3, column=1)
        self.pat_time.current(0)

        add_btn = tk.Button(self.patient_frame, text="Assign Doctor", command=self.assign_doctor,
                            bg="#118ab2", fg="white", font=("Helvetica", 11, "bold"), relief="raised", cursor="hand2")
        add_btn.grid(row=4, column=0, columnspan=2, pady=20)
        add_btn.bind("<Enter>", lambda e: add_btn.config(bg="#0b6985"))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg="#118ab2"))

    # Dashboard tab
    def create_dashboard_tab(self):
        self.tree = ttk.Treeview(self.dashboard_frame, columns=("Specialization", "Patients"), show="headings")
        self.tree.heading("Specialization", text="Specialization")
        self.tree.heading("Patients", text="Assigned Patients")
        self.tree.pack(fill="both", expand=True, pady=10)
        self.update_dashboard()

    # Add doctor
    def add_doctor(self):
        name = self.doc_name.get()
        spec = self.doc_specialization.get()
        time = self.doc_time.get()

        if not name:
            messagebox.showwarning("Warning", "Doctor name cannot be empty.")
            return

        # Allow same doctor multiple times
        self.doctors.append(Doctor(name, spec, [time]))
        self.save_data()
        self.update_dashboard()
        messagebox.showinfo("Success", f"Doctor {name} added successfully!")

    # Assign doctor
    def assign_doctor(self):
        name = self.pat_name.get()
        spec = self.pat_specialization.get()
        priority = int(self.pat_priority.get())
        time = self.pat_time.get()

        if not name:
            messagebox.showwarning("Warning", "Patient name cannot be empty.")
            return

        available_doctors = [d for d in self.doctors if d.specialization == spec]
        if not available_doctors:
            messagebox.showerror("Error", f"No available doctor for {spec}.")
            return

        doctor = min(available_doctors, key=lambda d: len(d.patients))
        patient = Patient(name, spec, priority, time)
        doctor.patients.append(patient)
        self.patients.append(patient)
        self.save_data()
        self.update_dashboard()
        messagebox.showinfo("Assigned", f"Patient {name} assigned to Dr. {doctor.name} ({spec})")

    # Dashboard update
    def update_dashboard(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for doc in self.doctors:
            patient_names = ', '.join([p.name for p in doc.patients]) if doc.patients else "No Patients"
            self.tree.insert("", "end", values=(doc.specialization, f"Dr. {doc.name} ({len(doc.patients)}): {patient_names}"))

    # Reset all patient assignments (keep doctors/patients)
    def reset_assignments(self):
        for doc in self.doctors:
            doc.patients.clear()
        self.save_data(clear_assignments=True)
        self.update_dashboard()
        messagebox.showinfo("Reset", "All doctor-patient assignments have been cleared.")

    # Report popup
    def show_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Doctor Report")
        report_window.geometry("500x400")
        report_window.configure(bg="#f8f9fa")

        tk.Label(report_window, text="Hospital Schedule Report", font=("Helvetica", 16, "bold"), bg="#f8f9fa", fg="#006d77").pack(pady=10)

        report_text = tk.Text(report_window, wrap="word", width=60, height=20)
        report_text.pack(padx=10, pady=10)

        for doc in self.doctors:
            report_text.insert("end", f"Dr. {doc.name} ({doc.specialization})\n")
            if not doc.patients:
                report_text.insert("end", "   No patients assigned yet.\n\n")
            else:
                for p in doc.patients:
                    report_text.insert("end", f"   - {p.name} | Priority: {p.priority} | Time: {p.appointment_time}\n")
                report_text.insert("end", "\n")
        report_text.config(state="disabled")

    # Save & load
    def save_data(self, clear_assignments=False):
        with open("hospital_data.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Doctor", "Specialization", "Patient", "Priority", "Time"])
            if not clear_assignments:
                for doc in self.doctors:
                    for p in doc.patients:
                        writer.writerow([doc.name, doc.specialization, p.name, p.priority, p.appointment_time])

    def load_data(self):
        if not os.path.exists("hospital_data.csv"):
            return
        with open("hospital_data.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                doc = Doctor(row["Doctor"], row["Specialization"], [])
                if doc not in self.doctors:
                    self.doctors.append(doc)
                if row["Patient"]:
                    patient = Patient(row["Patient"], row["Specialization"], int(row["Priority"]), row["Time"])
                    doc.patients.append(patient)
                    self.patients.append(patient)
        self.update_dashboard()

# -------------------------------
# Run App
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalSchedulerApp(root)
    root.mainloop()
