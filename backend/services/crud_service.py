"""
CRUD (Create, Read, Update, Delete) operations for the ERP system
"""
import sys, os

# Insert the project’s root (backend/) into sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from models.user_models import Batch, Employee, Batch, Batch, Product, Department, BatchTracking
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc
from models import *
from typing import List, Optional
from datetime import date


# =============================================================================
# BATCH OPERATIONS
# =============================================================================

def get_batch_by_code(db: Session, batch_code: str) -> Optional[Batch]:
    """
    Get a batch by its batch code
    Returns the batch with all related data loaded
    """
    return db.query(Batch).options(
        joinedload(Batch.product),
        joinedload(Batch.creator).joinedload(Employee.department),
        joinedload(Batch.tracking_records).joinedload(Batch.handler)
    ).filter(Batch.batch_code == batch_code).first()


def get_batch_by_id(db: Session, batch_id: int) -> Optional[Batch]:
    """Get a batch by its ID"""
    return db.query(Batch).options(
        joinedload(Batch.product),
        joinedload(Batch.creator),
        joinedload(Batch.tracking_records)
    ).filter(Batch.id == batch_id).first()


def get_batches_by_status(db: Session, status: Batch) -> List[Batch]:
    # Subquery to get the latest tracking record for each batch
    latest_tracking = db.query(
        Batch.batch_id,
        Batch.status
    ).distinct(Batch.batch_id).order_by(
        Batch.batch_id,
        desc(Batch.timestamp)
    ).subquery()

    return db.query(Batch).join(
        latest_tracking,
        Batch.id == latest_tracking.c.batch_id
    ).filter(
        latest_tracking.c.status == status
    ).options(
        joinedload(Batch.product),
        joinedload(Batch.tracking_records)
    ).all()


def get_batches_by_product(db: Session, product_name: str) -> List[Batch]:
    """Get all batches for a specific product"""
    return db.query(Batch).join(Product).filter(
        Product.name.ilike(f"%{product_name}%")
    ).options(
        joinedload(Batch.product),
        joinedload(Batch.tracking_records)
    ).all()


def search_batches(db: Session, search_term: str) -> List[Batch]:
    """
    Search batches by batch code, product name, or location
    """
    return db.query(Batch).join(Product).join(Batch).filter(
        or_(
            Batch.batch_code.ilike(f"%{search_term}%"),
            Product.name.ilike(f"%{search_term}%"),
            Batch.location.ilike(f"%{search_term}%")
        )
    ).options(
        joinedload(Batch.product),
        joinedload(Batch.tracking_records)
    ).distinct().all()


# =============================================================================
# BATCH TRACKING OPERATIONS
# =============================================================================

def get_batch_by_code(db: Session, batch_code: str) -> Optional[Batch]:
    """
    Get a batch by its batch code
    Returns the batch with all related data loaded
    """
    return db.query(Batch).options(
        joinedload(Batch.product),
        joinedload(Batch.creator).joinedload(Employee.department),
        joinedload(Batch.tracking_records).joinedload(BatchTracking.handler)
    ).filter(Batch.batch_code == batch_code).first()


def get_batch_by_id(db: Session, batch_id: int) -> Optional[Batch]:
    """Get a batch by its ID"""
    return db.query(Batch).options(
        joinedload(Batch.product),
        joinedload(Batch.creator),
        joinedload(Batch.tracking_records)).filter(Batch.id == batch_id).first()


def get_batches_by_status(db: Session, status: Batch) -> List[Batch]:
    """
    Get all batches with a specific current status
    """
    # Subquery to get the latest tracking record for each batch
    latest_tracking = db.query(
        Batch.batch_id,
        Batch.status
    ).distinct(Batch.batch_id).order_by(
        Batch.batch_id,
        desc(Batch.timestamp)
    ).subquery()

    return db.query(Batch).join(
        latest_tracking,
        Batch.id == latest_tracking.c.batch_id
    ).filter(
        latest_tracking.c.status == status
    ).options(
        joinedload(Batch.product),
        joinedload(Batch.tracking_records)
    ).all()


def get_batches_by_product(db: Session, product_name: str) -> List[Batch]:
    """Get all batches for a specific product"""
    return db.query(Batch).join(Product).filter(
        Product.name.ilike(f"%{product_name}%")
    ).options(
        joinedload(Batch.product),
        joinedload(Batch.tracking_records)
    ).all()


def search_batches(db: Session, search_term: str) -> List[Batch]:
    """
    Search batches by batch code, product name, or location
    """
    return db.query(Batch).join(Product).join(Batch).filter(
        or_(
            Batch.batch_code.ilike(f"%{search_term}%"),
            Product.name.ilike(f"%{search_term}%"),
            Batch.location.ilike(f"%{search_term}%")
        )
    ).options(
        joinedload(Batch.product),
        joinedload(Batch.tracking_records)
    ).distinct().all()


# =============================================================================
# BATCH TRACKING OPERATIONS
# =============================================================================

def get_batch_tracking_history(db: Session, batch_code: str) -> List[Batch]:
    """
    Get complete tracking history for a batch
    Ordered by timestamp (oldest first)
    """
    return db.query(Batch).join(Batch).filter(
        Batch.batch_code == batch_code
    ).options(
        joinedload(Batch.handler).joinedload(Employee.department)
    ).order_by(Batch.timestamp).all()


def get_current_batch_location(db: Session, batch_code: str) -> Optional[str]:
    """Get the current location of a batch"""
    latest_record = db.query(Batch).join(Batch).filter(
        Batch.batch_code == batch_code
    ).order_by(desc(Batch.timestamp)).first()

    return latest_record.location if latest_record else None


def get_batch_current_status(db: Session, batch_code: str) -> Optional[Batch]:
    """Get the current status of a batch"""
    latest_record = db.query(Batch).join(Batch).filter(
        Batch.batch_code == batch_code
    ).order_by(desc(Batch.timestamp)).first()

    return latest_record.status if latest_record else None


# =============================================================================
# EMPLOYEE OPERATIONS
# =============================================================================

def get_employee_by_id(db: Session, employee_id: str) -> Optional[Employee]:
    """Get employee by ID"""
    return db.query(Employee).options(
        joinedload(Employee.department)
    ).filter(Employee.id == employee_id).first()


def get_employee_by_email(db: Session, email: str) -> Optional[Employee]:
    """Get employee by email"""
    return db.query(Employee).options(
        joinedload(Employee.department)
    ).filter(Employee.email == email).first()


def get_employees_by_department(db: Session, department_name: str) -> List[Employee]:
    """Get all employees in a department"""
    return db.query(Employee).join(Department).filter(
        Department.name.ilike(f"%{department_name}%")
    ).options(joinedload(Employee.department)).all()


def get_batch_handlers(db: Session, batch_code: str) -> List[Employee]:
    """Get all employees who have handled a specific batch"""
    return db.query(Employee).join(Batch).join(Batch).filter(
        Batch.batch_code == batch_code
    ).options(joinedload(Employee.department)).distinct().all()


# =============================================================================
# PRODUCT OPERATIONS
# =============================================================================

def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    """Get product by ID"""
    return db.query(Product).filter(Product.id == product_id).first()


def get_products_by_category(db: Session, category: str) -> List[Product]:
    """Get all products in a category"""
    return db.query(Product).filter(
        Product.category.ilike(f"%{category}%")
    ).all()


def search_products(db: Session, search_term: str) -> List[Product]:
    """Search products by name or category"""
    return db.query(Product).filter(
        or_(
            Product.name.ilike(f"%{search_term}%"),
            Product.category.ilike(f"%{search_term}%")
        )
    ).all()


# =============================================================================
# DEPARTMENT OPERATIONS
# =============================================================================

def get_department_by_id(db: Session, dept_id: str) -> Optional[Department]:
    """Get department by ID"""
    return db.query(Department).options(
        joinedload(Department.employees),
        joinedload(Department.head)
    ).filter(Department.id == dept_id).first()


def get_department_by_name(db: Session, name: str) -> Optional[Department]:
    """Get department by name"""
    return db.query(Department).options(
        joinedload(Department.employees)
    ).filter(Department.name.ilike(f"%{name}%")).first()


# =============================================================================
# ANALYTICS & REPORTING FUNCTIONS
# =============================================================================

def get_batch_statistics(db: Session) -> dict:
    """Get overall batch statistics"""
    total_batches = db.query(Batch).count()

    # Count by status
    manufactured = len(get_batches_by_status(db, Batch.MANUFACTURED))
    in_transit = len(get_batches_by_status(db, Batch.IN_TRANSIT))
    delivered = len(get_batches_by_status(db, Batch.DELIVERED))

    return {
        "total_batches": total_batches,
        "manufactured": manufactured,
        "in_transit": in_transit,
        "delivered": delivered
    }


def get_batches_by_date_range(db: Session, start_date: date, end_date: date) -> List[Batch]:
    return db.query(Batch).filter(
        and_(
            Batch.manufactured_date >= start_date,
            Batch.manufactured_date <= end_date
        )
    ).options(
        joinedload(Batch.product),
        joinedload(Batch.tracking_records)
    ).all()
