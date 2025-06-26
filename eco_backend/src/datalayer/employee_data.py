from sqlalchemy.orm import Session
from src.models.db import SessionLocal
from src.errors.general_errors import DataFetchError
from src.models.user_model import EmployeeORM, EmployeeCreate, EmployeeOut
from datetime import datetime
import hashlib
def get_user_by_identity(identity: str):
    session: Session = SessionLocal()
    try:
        user = session.query(EmployeeORM).filter(EmployeeORM.identity == identity).first()
        return user, user.hashed_password if user else (None, None)
    except Exception as e:
        raise DataFetchError(f"[SQLAlchemy ERROR] {str(e)}")
    finally:
        session.close()


def fetch_all_employees():
    session: Session = SessionLocal()
    try:
        employees = session.query(EmployeeORM).all()
        return [EmployeeOut.model_validate(emp).model_dump() for emp in employees]
    except Exception as e:
        raise DataFetchError(f"[Fetch Error] {str(e)}")
    finally:
        session.close()

def add_employee(employee: EmployeeCreate):
    session: Session = SessionLocal()
    try:
        hashed_pw = hashlib.sha256(employee.password.encode("utf-8")).hexdigest()
        new_emp = EmployeeORM(
            identity=employee.identity,
            name=employee.name,
            phone=employee.phone,
            location=employee.location,
            joining_date=employee.joining_date,
            role=employee.role,
            worker_type=employee.worker_type if employee.role == "worker" else None,
            created_at=datetime.utcnow(),
            hashed_password=hashed_pw
        )
        session.add(new_emp)
        session.commit()
        session.refresh(new_emp)
        return EmployeeOut.model_validate(new_emp).model_dump()
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Add Error] {str(e)}")
    finally:
        session.close()

def delete_employee_by_identity(identity: str):
    session: Session = SessionLocal()
    try:
        emp = session.query(EmployeeORM).filter_by(identity=identity).first()
        if not emp:
            raise DataFetchError("Employee not found.")
        session.delete(emp)
        session.commit()
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Delete Error] {str(e)}")
    finally:
        session.close()