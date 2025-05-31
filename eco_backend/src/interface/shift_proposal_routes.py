from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.datalayer.shift_proposal_data import create_shift_proposal, fetch_pending_proposals, update_proposal_status, approve_and_add_shift
from src.models.shift_proposal_model import ShiftProposalCreate
from src.errors.general_errors import DataFetchError

shift_proposal_bp = Blueprint("shift_proposals", __name__)

@shift_proposal_bp.route("/proposeShift", methods=["POST"])
def propose_shift():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), HTTPStatus.BAD_REQUEST
        proposal_data = ShiftProposalCreate.model_validate(data)
        result = create_shift_proposal(proposal_data)
        return jsonify({"status": "success", "message": "Shift proposal created", "proposal": result}), HTTPStatus.CREATED
    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@shift_proposal_bp.route("/getPendingProposals", methods=["GET"])
def get_pending_proposals():
    try:
        proposals = fetch_pending_proposals()
        return jsonify({"status": "success", "proposals": proposals}), HTTPStatus.OK
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@shift_proposal_bp.route("/approveProposal/<proposal_id>", methods=["PUT"])
def approve_proposal(proposal_id: str):
    try:
        result = approve_and_add_shift(proposal_id)
        return jsonify({"status": "success", "message": "Proposal approved and shift added", "shift": result}), HTTPStatus.OK
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@shift_proposal_bp.route("/denyProposal/<proposal_id>", methods=["PUT"])
def deny_proposal(proposal_id: str):
    try:
        result = update_proposal_status(proposal_id, "denied")
        return jsonify({"status": "success", "message": "Proposal denied", "proposal": result}), HTTPStatus.OK
    except DataFetchError as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR