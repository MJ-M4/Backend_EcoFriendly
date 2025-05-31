import uuid
from sqlalchemy.orm import Session
from src.models.shift_model import ShiftCreate
from src.models.db import SessionLocal
from src.errors.general_errors import DataFetchError
from src.models.shift_proposal_model import ShiftProposal, ShiftProposalCreate, ProposalStatus
from src.datalayer.shift_data import add_shift
from datetime import datetime

def create_shift_proposal(proposal: ShiftProposalCreate):
    session: Session = SessionLocal()
    try:
        new_proposal = ShiftProposal(
            id=str(uuid.uuid4())[:5],
            worker_id=proposal.worker_id,
            worker_name=proposal.worker_name,
            worker_type=proposal.worker_type,
            date=proposal.date,
            start_time=proposal.start_time,
            end_time=proposal.end_time,
            location=proposal.location,
            status=ProposalStatus.PENDING,
            submitted_at=datetime.utcnow().date()
        )
        session.add(new_proposal)
        session.commit()
        session.refresh(new_proposal)
        return {
            "id": new_proposal.id,
            "worker_id": new_proposal.worker_id,
            "worker_name": new_proposal.worker_name,
            "worker_type": new_proposal.worker_type,
            "date": new_proposal.date.isoformat() if new_proposal.date else None,
            "start_time": new_proposal.start_time.isoformat() if new_proposal.start_time else None,
            "end_time": new_proposal.end_time.isoformat() if new_proposal.end_time else None,
            "location": new_proposal.location,
            "status": new_proposal.status.value,
            "submitted_at": new_proposal.submitted_at.isoformat() if new_proposal.submitted_at else None
        }
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error creating shift proposal] {str(e)}")
    finally:
        session.close()

def fetch_pending_proposals():
    session: Session = SessionLocal()
    try:
        proposals = session.query(ShiftProposal).filter_by(status=ProposalStatus.PENDING).all()
        return [
            {
                "id": proposal.id,
                "worker_id": proposal.worker_id,   
                "worker_name": proposal.worker_name,
                "worker_type": proposal.worker_type,
                "date": proposal.date.isoformat() if proposal.date else None,
                "start_time": proposal.start_time.isoformat() if proposal.start_time else None,
                "end_time": proposal.end_time.isoformat() if proposal.end_time else None,
                "location": proposal.location,
                "status": proposal.status.value,
                "submitted_at": proposal.submitted_at.isoformat() if proposal.submitted_at else None
            }
            for proposal in proposals
        ]
    except Exception as e:
        raise DataFetchError(f"[Error fetching pending proposals] {str(e)}")
    finally:
        session.close()

def update_proposal_status(proposal_id: str, status: str):
    session: Session = SessionLocal()
    try:
        proposal = session.query(ShiftProposal).filter_by(id=proposal_id).first()
        if not proposal:
            raise DataFetchError("Proposal not found.")
        proposal.status = ProposalStatus(status)
        session.commit()
        session.refresh(proposal)
        return {
            "id": proposal.id,
            "worker_id": proposal.worker_id,
            "worker_name": proposal.worker_name,
            "worker_type": proposal.worker_type,
            "date": proposal.date.isoformat() if proposal.date else None,
            "start_time": proposal.start_time.isoformat() if proposal.start_time else None,
            "end_time": proposal.end_time.isoformat() if proposal.end_time else None,
            "location": proposal.location,
            "status": proposal.status.value,
            "submitted_at": proposal.submitted_at.isoformat() if proposal.submitted_at else None
        }
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error updating proposal status] {str(e)}")
    finally:
        session.close()

def approve_and_add_shift(proposal_id: str):
    session: Session = SessionLocal()
    try:
        proposal = session.query(ShiftProposal).filter_by(id=proposal_id).first()
        if not proposal:
            raise DataFetchError("Proposal not found.")
        # Update proposal status
        proposal.status = ProposalStatus.APPROVED
        session.commit()
        # Add to shifts using existing add_shift function
        shift_data = ShiftCreate(
            worker_id=proposal.worker_id,
            worker_name=proposal.worker_name,
            worker_type=proposal.worker_type,
            date=proposal.date.isoformat(),
            start_time=proposal.start_time.isoformat(),
            end_time=proposal.end_time.isoformat(),
            location=proposal.location
        )
        result = add_shift(shift_data)
        return result
    except Exception as e:
        session.rollback()
        raise DataFetchError(f"[Error approving and adding shift] {str(e)}")
    finally:
        session.close()