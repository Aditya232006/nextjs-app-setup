from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, Text, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class ResidentStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCHARGED = "discharged"
    DECEASED = "deceased"

class BedStatus(enum.Enum):
    OCCUPIED = "occupied"
    VACANT = "vacant"
    MAINTENANCE = "maintenance"

class CheckupStatus(enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class EventStatus(enum.Enum):
    PLANNED = "planned"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Resident(Base):
    __tablename__ = "residents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    age = Column(Integer, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    phone = Column(String(20))
    emergency_contact = Column(String(100))
    emergency_phone = Column(String(20))
    address = Column(Text)
    medical_conditions = Column(Text)
    allergies = Column(Text)
    room_number = Column(String(10))
    bed_id = Column(Integer, ForeignKey("beds.id"))
    admission_date = Column(Date, nullable=False)
    status = Column(Enum(ResidentStatus), default=ResidentStatus.ACTIVE)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    bed = relationship("Bed", back_populates="resident")
    medications = relationship("Medication", back_populates="resident")
    checkups = relationship("Checkup", back_populates="resident")
    documents = relationship("Document", back_populates="resident")

class Bed(Base):
    __tablename__ = "beds"

    id = Column(Integer, primary_key=True, index=True)
    bed_number = Column(String(10), unique=True, nullable=False, index=True)
    room_number = Column(String(10), nullable=False)
    floor = Column(Integer, nullable=False)
    bed_type = Column(String(50))  # single, shared, etc.
    status = Column(Enum(BedStatus), default=BedStatus.VACANT)
    monthly_rate = Column(Float)
    amenities = Column(Text)  # JSON string of amenities
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    resident = relationship("Resident", back_populates="bed", uselist=False)

class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=False)
    medication_name = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50), nullable=False)  # daily, twice daily, etc.
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    prescribed_by = Column(String(100))
    instructions = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    resident = relationship("Resident", back_populates="medications")

class Checkup(Base):
    __tablename__ = "checkups"

    id = Column(Integer, primary_key=True, index=True)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=False)
    checkup_type = Column(String(50), nullable=False)  # routine, emergency, specialist
    scheduled_date = Column(DateTime, nullable=False)
    doctor_name = Column(String(100))
    location = Column(String(100))  # clinic, hospital, on-site
    status = Column(Enum(CheckupStatus), default=CheckupStatus.SCHEDULED)
    notes = Column(Text)
    results = Column(Text)
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    resident = relationship("Resident", back_populates="checkups")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    event_date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer)
    location = Column(String(100))
    organizer = Column(String(100))
    max_participants = Column(Integer)
    current_participants = Column(Integer, default=0)
    status = Column(Enum(EventStatus), default=EventStatus.PLANNED)
    event_type = Column(String(50))  # birthday, activity, medical, social
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String(50))  # weekly, monthly, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    resident_id = Column(Integer, ForeignKey("residents.id"))
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String(100))
    document_type = Column(String(50), nullable=False)  # medical, legal, personal, etc.
    description = Column(Text)
    uploaded_by = Column(String(100))
    is_confidential = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    resident = relationship("Resident", back_populates="documents")

class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    role = Column(String(50), nullable=False)  # admin, nurse, doctor, caregiver
    department = Column(String(50))
    hire_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)
    shift = Column(String(20))  # morning, evening, night
    qualifications = Column(Text)
    emergency_contact = Column(String(100))
    emergency_phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=False)
    visitor_name = Column(String(100), nullable=False)
    relationship = Column(String(50))  # family, friend, etc.
    phone = Column(String(20))
    visit_date = Column(DateTime, nullable=False)
    check_in_time = Column(DateTime)
    check_out_time = Column(DateTime)
    purpose = Column(String(200))
    notes = Column(Text)
    approved_by = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Billing(Base):
    __tablename__ = "billing"

    id = Column(Integer, primary_key=True, index=True)
    resident_id = Column(Integer, ForeignKey("residents.id"), nullable=False)
    billing_period_start = Column(Date, nullable=False)
    billing_period_end = Column(Date, nullable=False)
    accommodation_charges = Column(Float, default=0.0)
    medical_charges = Column(Float, default=0.0)
    food_charges = Column(Float, default=0.0)
    other_charges = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    amount_paid = Column(Float, default=0.0)
    balance = Column(Float, default=0.0)
    due_date = Column(Date, nullable=False)
    payment_status = Column(String(20), default="pending")  # pending, paid, overdue
    payment_method = Column(String(50))
    payment_date = Column(Date)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
