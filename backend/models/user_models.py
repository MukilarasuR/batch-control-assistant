"""
SQLAlchemy models for the ERP Chatbot system
"""
import sys, os

# Insert the project’s root (backend/) into sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))            # .../backend/models
parent_dir = os.path.dirname(current_dir)                           # .../backend
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)



from sqlalchemy import Column, Integer, String, DateTime, Date, Numeric, ForeignKey, Enum
from decimal import Decimal
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base
import uuid
import enum


# Enums for better data integrity
class BatchStatus(enum.Enum):
    MANUFACTURED = "Manufactured"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"



# MODEL 1: Department
class Department(Base):
    __tablename__ = "departments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    head_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    employees = relationship("Employee", back_populates="department", foreign_keys="Employee.department_id")
    head = relationship("Employee", foreign_keys=[head_id], post_update=True)

    def __repr__(self):
        return f"<Department(name='{self.name}')>"


# MODEL 2: Employee

class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id"), nullable=False)
    designation = Column(String(100), nullable=False)
    date_joined = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    department = relationship("Department", back_populates="employees", foreign_keys=[department_id])
    created_batches = relationship("Batch", back_populates="creator")
    handled_trackings = relationship("BatchTracking", back_populates="handler")

    def __repr__(self):
        return f"<Employee(name='{self.name}', designation='{self.designation}')>"


# MODEL 3: Product

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    batches = relationship("Batch", back_populates="product")

    def __repr__(self):
        return f"<Product(name='{self.name}', category='{self.category}')>"


# MODEL 4: Batch

class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    batch_code = Column(String(50), nullable=False, unique=True, index=True)
    quantity = Column(Integer, nullable=False)
    manufactured_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="batches")
    creator = relationship("Employee", back_populates="created_batches")
    tracking_records = relationship("BatchTracking", back_populates="batch", order_by="BatchTracking.timestamp")
    def __repr__(self):
        return f"<Batch(batch_code='{self.batch_code}', quantity={self.quantity})>"

    @property
    def current_status(self):
        """Get the current status of the batch"""
        if self.tracking_records:
            return self.tracking_records[-1].status
        return None

    @property
    def current_location(self):
        """Get the current location of the batch"""
        if self.tracking_records:
            return self.tracking_records[-1].location
        return None


# MODEL 5: BatchTracking

class BatchTracking(Base):
    __tablename__ = "batch_tracking"

    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    location = Column(String(200), nullable=False)
    status = Column(Enum(BatchStatus), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    handled_by = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    notes = Column(String(500), nullable=True)  # Optional field for additional info

    # Relationships
    batch = relationship("Batch", back_populates="tracking_records")
    handler = relationship("Employee", back_populates="handled_trackings")

    def __repr__(self):
        return f"<BatchTracking(batch_id={self.batch_id}, status='{self.status.value}', location='{self.location}')>"