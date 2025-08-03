from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
from app.models import ResidentStatus, BedStatus, CheckupStatus, EventStatus

# Base schemas
class ResidentBase(BaseModel):
    name: str
    age: int
    date_of_birth: date
    gender: str
    phone: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    address: Optional[str] = None
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None
    room_number: Optional[str] = None
    admission_date: date
    status: ResidentStatus = ResidentStatus.ACTIVE
    notes: Optional[str] = None

class ResidentCreate(ResidentBase):
    pass

class ResidentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None
    address: Optional[str] = None
    medical_conditions: Optional[str] = None
    allergies: Optional[str] = None
    room_number: Optional[str] = None
    status: Optional[ResidentStatus] = None
    notes: Optional[str] = None

class Resident(ResidentBase):
    id: int
    bed_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ResidentBirthday(BaseModel):
    id: int
    name: str
    date_of_birth: date
    age: int
    room_number: Optional[str] = None
    days_until_birthday: int

    class Config:
        from_attributes = True

# Bed schemas
class BedBase(BaseModel):
    bed_number: str
    room_number: str
    floor: int
    bed_type: Optional[str] = None
    status: BedStatus = BedStatus.VACANT
    monthly_rate: Optional[float] = None
    amenities: Optional[str] = None

class BedCreate(BedBase):
    pass

class Bed(BedBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Medication schemas
class MedicationBase(BaseModel):
    resident_id: int
    medication_name: str
    dosage: str
    frequency: str
    start_date: date
    end_date: Optional[date] = None
    prescribed_by: Optional[str] = None
    instructions: Optional[str] = None
    is_active: bool = True

class MedicationCreate(MedicationBase):
    pass

class Medication(MedicationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Checkup schemas
class CheckupBase(BaseModel):
    resident_id: int
    checkup_type: str
    scheduled_date: datetime
    doctor_name: Optional[str] = None
    location: Optional[str] = None
    status: CheckupStatus = CheckupStatus.SCHEDULED
    notes: Optional[str] = None
    results: Optional[str] = None
    follow_up_required: bool = False
    follow_up_date: Optional[date] = None

class CheckupCreate(CheckupBase):
    pass

class Checkup(CheckupBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Event schemas
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    event_date: datetime
    duration_minutes: Optional[int] = None
    location: Optional[str] = None
    organizer: Optional[str] = None
    max_participants: Optional[int] = None
    current_participants: int = 0
    status: EventStatus = EventStatus.PLANNED
    event_type: Optional[str] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Document schemas
class DocumentBase(BaseModel):
    resident_id: Optional[int] = None
    filename: str
    file_path: str
    document_type: str
    description: Optional[str] = None
    uploaded_by: Optional[str] = None
    is_confidential: bool = False

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    original_filename: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Staff schemas
class StaffBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    role: str
    department: Optional[str] = None
    hire_date: date
    is_active: bool = True
    shift: Optional[str] = None
    qualifications: Optional[str] = None
    emergency_contact: Optional[str] = None
    emergency_phone: Optional[str] = None

class StaffCreate(StaffBase):
    pass

class Staff(StaffBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Visitor schemas
class VisitorBase(BaseModel):
    resident_id: int
    visitor_name: str
    relationship: Optional[str] = None
    phone: Optional[str] = None
    visit_date: datetime
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    purpose: Optional[str] = None
    notes: Optional[str] = None
    approved_by: Optional[str] = None

class VisitorCreate(VisitorBase):
    pass

class Visitor(VisitorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Billing schemas
class BillingBase(BaseModel):
    resident_id: int
    billing_period_start: date
    billing_period_end: date
    accommodation_charges: float = 0.0
    medical_charges: float = 0.0
    food_charges: float = 0.0
    other_charges: float = 0.0
    total_amount: float
    amount_paid: float = 0.0
    balance: float = 0.0
    due_date: date
    payment_status: str = "pending"
    payment_method: Optional[str] = None
    payment_date: Optional[date] = None
    notes: Optional[str] = None

class BillingCreate(BillingBase):
    pass

class Billing(BillingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Dashboard schemas
class DashboardStats(BaseModel):
    total_residents: int
    under_medication: int
    vacant_beds: int
    upcoming_birthdays: int

class TodaySchedule(BaseModel):
    checkups: List[Checkup]
    events: List[Event]
    birthdays: List[ResidentBirthday]

# Search and filter schemas
class ResidentSearch(BaseModel):
    query: str
    status: Optional[ResidentStatus] = None
    room_number: Optional[str] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None

# Response schemas
class MessageResponse(BaseModel):
    message: str
    success: bool = True

class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    per_page: int
    pages: int
