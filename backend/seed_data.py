#!/usr/bin/env python3
"""
Seed script to populate the database with sample data for testing
"""
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
import random

# Create database tables
models.Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    try:
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("Clearing existing data...")
        db.query(models.Visitor).delete()
        db.query(models.Billing).delete()
        db.query(models.Document).delete()
        db.query(models.Medication).delete()
        db.query(models.Checkup).delete()
        db.query(models.Event).delete()
        db.query(models.Resident).delete()
        db.query(models.Bed).delete()
        db.query(models.Staff).delete()
        db.commit()
        
        # Create beds
        print("Creating beds...")
        beds_data = []
        for floor in range(1, 4):  # 3 floors
            for room in range(1, 21):  # 20 rooms per floor
                for bed_num in ['A', 'B']:  # 2 beds per room
                    bed_number = f"{floor}{room:02d}{bed_num}"
                    room_number = f"{floor}{room:02d}"
                    
                    bed = models.Bed(
                        bed_number=bed_number,
                        room_number=room_number,
                        floor=floor,
                        bed_type="single" if bed_num == 'A' else "shared",
                        status=models.BedStatus.VACANT,
                        monthly_rate=random.uniform(800, 1500),
                        amenities="AC, TV, Private Bathroom" if bed_num == 'A' else "AC, TV"
                    )
                    beds_data.append(bed)
        
        db.add_all(beds_data)
        db.commit()
        
        # Get created beds
        beds = db.query(models.Bed).all()
        
        # Create staff
        print("Creating staff...")
        staff_data = [
            models.Staff(
                name="Dr. Sarah Johnson",
                email="sarah.johnson@oldagehome.com",
                phone="555-0101",
                role="doctor",
                department="Medical",
                hire_date=date(2020, 1, 15),
                shift="morning",
                qualifications="MD, Geriatrics Specialist"
            ),
            models.Staff(
                name="Nurse Mary Wilson",
                email="mary.wilson@oldagehome.com",
                phone="555-0102",
                role="nurse",
                department="Medical",
                hire_date=date(2021, 3, 10),
                shift="morning",
                qualifications="RN, 10 years experience"
            ),
            models.Staff(
                name="Admin John Smith",
                email="john.smith@oldagehome.com",
                phone="555-0103",
                role="admin",
                department="Administration",
                hire_date=date(2019, 6, 1),
                shift="morning",
                qualifications="MBA, Healthcare Management"
            ),
            models.Staff(
                name="Caregiver Lisa Brown",
                email="lisa.brown@oldagehome.com",
                phone="555-0104",
                role="caregiver",
                department="Care",
                hire_date=date(2022, 2, 20),
                shift="evening",
                qualifications="CNA Certified"
            )
        ]
        
        db.add_all(staff_data)
        db.commit()
        
        # Create residents
        print("Creating residents...")
        residents_data = [
            {
                "name": "Eleanor Thompson",
                "age": 78,
                "date_of_birth": date(1945, 3, 15),
                "gender": "Female",
                "phone": "555-1001",
                "emergency_contact": "Margaret Thompson (Daughter)",
                "emergency_phone": "555-1002",
                "address": "123 Oak Street, Springfield",
                "medical_conditions": "Diabetes, Hypertension",
                "allergies": "Penicillin",
                "admission_date": date(2023, 1, 10),
                "status": models.ResidentStatus.ACTIVE,
                "notes": "Enjoys reading and gardening activities"
            },
            {
                "name": "Robert Martinez",
                "age": 82,
                "date_of_birth": date(1941, 7, 22),
                "gender": "Male",
                "phone": "555-1003",
                "emergency_contact": "Carlos Martinez (Son)",
                "emergency_phone": "555-1004",
                "address": "456 Pine Avenue, Springfield",
                "medical_conditions": "Arthritis, Heart condition",
                "allergies": "None known",
                "admission_date": date(2023, 2, 5),
                "status": models.ResidentStatus.ACTIVE,
                "notes": "Former teacher, loves chess"
            },
            {
                "name": "Dorothy Williams",
                "age": 75,
                "date_of_birth": date(1948, 11, 8),
                "gender": "Female",
                "phone": "555-1005",
                "emergency_contact": "James Williams (Son)",
                "emergency_phone": "555-1006",
                "address": "789 Maple Drive, Springfield",
                "medical_conditions": "Osteoporosis",
                "allergies": "Shellfish",
                "admission_date": date(2023, 3, 12),
                "status": models.ResidentStatus.ACTIVE,
                "notes": "Active in social activities"
            },
            {
                "name": "Frank Anderson",
                "age": 80,
                "date_of_birth": date(1943, 5, 30),
                "gender": "Male",
                "phone": "555-1007",
                "emergency_contact": "Susan Anderson (Daughter)",
                "emergency_phone": "555-1008",
                "address": "321 Elm Street, Springfield",
                "medical_conditions": "Mild dementia, Diabetes",
                "allergies": "Latex",
                "admission_date": date(2023, 4, 18),
                "status": models.ResidentStatus.ACTIVE,
                "notes": "Requires assistance with daily activities"
            },
            {
                "name": "Grace Chen",
                "age": 77,
                "date_of_birth": date(1946, 9, 14),
                "gender": "Female",
                "phone": "555-1009",
                "emergency_contact": "David Chen (Son)",
                "emergency_phone": "555-1010",
                "address": "654 Birch Lane, Springfield",
                "medical_conditions": "Hypertension",
                "allergies": "None known",
                "admission_date": date(2023, 5, 25),
                "status": models.ResidentStatus.ACTIVE,
                "notes": "Bilingual, helps with translation"
            }
        ]
        
        created_residents = []
        for i, resident_data in enumerate(residents_data):
            # Assign a bed to each resident
            available_bed = beds[i]
            available_bed.status = models.BedStatus.OCCUPIED
            
            resident = models.Resident(
                **resident_data,
                bed_id=available_bed.id,
                room_number=available_bed.room_number
            )
            created_residents.append(resident)
        
        db.add_all(created_residents)
        db.commit()
        
        # Get created residents
        residents = db.query(models.Resident).all()
        
        # Create medications
        print("Creating medications...")
        medications_data = [
            models.Medication(
                resident_id=residents[0].id,
                medication_name="Metformin",
                dosage="500mg",
                frequency="twice daily",
                start_date=date(2023, 1, 10),
                prescribed_by="Dr. Sarah Johnson",
                instructions="Take with meals"
            ),
            models.Medication(
                resident_id=residents[0].id,
                medication_name="Lisinopril",
                dosage="10mg",
                frequency="once daily",
                start_date=date(2023, 1, 10),
                prescribed_by="Dr. Sarah Johnson",
                instructions="Take in the morning"
            ),
            models.Medication(
                resident_id=residents[1].id,
                medication_name="Aspirin",
                dosage="81mg",
                frequency="once daily",
                start_date=date(2023, 2, 5),
                prescribed_by="Dr. Sarah Johnson",
                instructions="Take with food"
            ),
            models.Medication(
                resident_id=residents[3].id,
                medication_name="Donepezil",
                dosage="5mg",
                frequency="once daily",
                start_date=date(2023, 4, 18),
                prescribed_by="Dr. Sarah Johnson",
                instructions="Take at bedtime"
            )
        ]
        
        db.add_all(medications_data)
        db.commit()
        
        # Create checkups
        print("Creating checkups...")
        checkups_data = [
            models.Checkup(
                resident_id=residents[0].id,
                checkup_type="routine",
                scheduled_date=datetime.now() + timedelta(days=1),
                doctor_name="Dr. Sarah Johnson",
                location="On-site clinic",
                status=models.CheckupStatus.SCHEDULED,
                notes="Regular diabetes checkup"
            ),
            models.Checkup(
                resident_id=residents[1].id,
                checkup_type="cardiology",
                scheduled_date=datetime.now() + timedelta(days=3),
                doctor_name="Dr. Michael Brown",
                location="Springfield Hospital",
                status=models.CheckupStatus.SCHEDULED,
                notes="Heart condition follow-up"
            ),
            models.Checkup(
                resident_id=residents[2].id,
                checkup_type="routine",
                scheduled_date=datetime.now() + timedelta(days=7),
                doctor_name="Dr. Sarah Johnson",
                location="On-site clinic",
                status=models.CheckupStatus.SCHEDULED,
                notes="Annual physical examination"
            )
        ]
        
        db.add_all(checkups_data)
        db.commit()
        
        # Create events
        print("Creating events...")
        events_data = [
            models.Event(
                title="Morning Exercise Class",
                description="Light exercise and stretching for all residents",
                event_date=datetime.now() + timedelta(days=1, hours=9),
                duration_minutes=60,
                location="Activity Room",
                organizer="Lisa Brown",
                max_participants=20,
                current_participants=8,
                status=models.EventStatus.PLANNED,
                event_type="activity",
                is_recurring=True,
                recurrence_pattern="daily"
            ),
            models.Event(
                title="Birthday Celebration - Eleanor Thompson",
                description="Celebrating Eleanor's 78th birthday",
                event_date=datetime.now() + timedelta(days=5, hours=15),
                duration_minutes=120,
                location="Main Hall",
                organizer="John Smith",
                max_participants=50,
                current_participants=12,
                status=models.EventStatus.PLANNED,
                event_type="birthday"
            ),
            models.Event(
                title="Music Therapy Session",
                description="Relaxing music therapy for mental wellness",
                event_date=datetime.now() + timedelta(days=2, hours=14),
                duration_minutes=90,
                location="Therapy Room",
                organizer="Music Therapist",
                max_participants=15,
                current_participants=6,
                status=models.EventStatus.PLANNED,
                event_type="therapy"
            )
        ]
        
        db.add_all(events_data)
        db.commit()
        
        # Create some sample documents
        print("Creating documents...")
        documents_data = [
            models.Document(
                resident_id=residents[0].id,
                filename="medical_history_eleanor.pdf",
                original_filename="medical_history_eleanor.pdf",
                file_path="uploads/medical/medical_history_eleanor.pdf",
                file_size=1024000,
                mime_type="application/pdf",
                document_type="medical",
                description="Complete medical history",
                uploaded_by="Dr. Sarah Johnson",
                is_confidential=True
            ),
            models.Document(
                resident_id=residents[1].id,
                filename="insurance_robert.pdf",
                original_filename="insurance_robert.pdf",
                file_path="uploads/legal/insurance_robert.pdf",
                file_size=512000,
                mime_type="application/pdf",
                document_type="legal",
                description="Insurance documentation",
                uploaded_by="John Smith",
                is_confidential=False
            )
        ]
        
        db.add_all(documents_data)
        db.commit()
        
        print("Database seeded successfully!")
        print(f"Created {len(beds_data)} beds")
        print(f"Created {len(staff_data)} staff members")
        print(f"Created {len(residents_data)} residents")
        print(f"Created {len(medications_data)} medications")
        print(f"Created {len(checkups_data)} checkups")
        print(f"Created {len(events_data)} events")
        print(f"Created {len(documents_data)} documents")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
