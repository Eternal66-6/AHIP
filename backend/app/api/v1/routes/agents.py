from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import AgentExecutionLog, AuditLog
from app.domain.schemas.schemas import AgentRunRequest
from app.application.agents.orchestrator import WorkflowOrchestrator

router = APIRouter()

@router.post("/run-case-review")
def run_case_review(request: AgentRunRequest, db: Session = Depends(get_db)):
    # Run the orchestrator
    result = WorkflowOrchestrator(db).run_case_review(request.case_id)
    
    # Audit log the execution
    import datetime
    audit = AuditLog(
        case_id=request.case_id,
        action="AGENT_EXECUTION",
        actor="System",
        details="Multi-Agent Pipeline executed and generated a Consolidated Output.",
        created_at=datetime.datetime.utcnow().isoformat()
    )
    db.add(audit)
    db.commit()
    
    return result

@router.get("/logs")
def get_agent_logs(db: Session = Depends(get_db)):
    logs = db.query(AgentExecutionLog).order_by(AgentExecutionLog.created_at.desc()).all()
    return [
        {
            "id": log.id,
            "case_id": log.case_id,
            "agent_name": log.agent_name,
            "observation": log.observation,
            "recommendation": log.recommendation,
            "confidence": log.confidence,
            "created_at": log.created_at
        }
        for log in logs
    ]

from app.application.context.context_builder import HealthcareContextBuilder

@router.get("/context/{case_id}")
def get_case_context_mapping(case_id: str, db: Session = Depends(get_db)):
    builder = HealthcareContextBuilder(db)
    return {
        "case_id": case_id,
        "patient_journey": builder.build_patient_journey_context(case_id).model_dump(),
        "claim": builder.build_claim_context(case_id).model_dump(),
        "provider_contract": builder.build_provider_contract_context(case_id).model_dump(),
        "compliance": builder.build_compliance_context(case_id).model_dump(),
    }

from app.domain.schemas.schemas import DecisionRequest

@router.get("/priority-queue")
def get_priority_queue(db: Session = Depends(get_db)):
    # Fetch all consolidator logs, ordered by date descending
    logs = db.query(AgentExecutionLog).filter(
        AgentExecutionLog.agent_name == "Consolidator Agent"
    ).order_by(AgentExecutionLog.created_at.desc()).all()
    
    # Deduplicate by case_id (keep only the most recent)
    seen_cases = set()
    unique_logs = []
    for log in logs:
        if log.case_id not in seen_cases:
            seen_cases.add(log.case_id)
            unique_logs.append(log)
    
    # Sort them: High risk first, then by date
    def sort_key(log):
        is_high_risk = "Senior Claims Analyst" in (log.related_workflow_event or "") or "High" in (log.observation or "") or "High" in (log.recommendation or "")
        # Return tuple: (0 if High Risk else 1, timestamp desc)
        return (0 if is_high_risk else 1, log.created_at)
        
    sorted_logs = sorted(unique_logs, key=sort_key)
    
    return [
        {
            "id": log.id,
            "case_id": log.case_id,
            "routing_destination": log.related_workflow_event,
            "summary_observation": log.observation,
            "recommended_action": log.recommendation,
            "confidence": log.confidence,
            "created_at": log.created_at
        }
        for log in sorted_logs
    ]

@router.post("/cases/{case_id}/decision")
def submit_decision(case_id: str, request: DecisionRequest, db: Session = Depends(get_db)):
    import datetime
    
    # 1. Update the AgentExecutionLog decision status
    # We find the most recent Consolidator Agent log for this case
    log = db.query(AgentExecutionLog).filter(
        AgentExecutionLog.case_id == case_id,
        AgentExecutionLog.agent_name == "Consolidator Agent"
    ).order_by(AgentExecutionLog.created_at.desc()).first()
    
    if log:
        log.decision_status = "ACCEPTED" if request.action == "Accept" else "OVERRIDDEN"
        log.decision_reason = request.reason
        log.decided_by = request.user_id or "Anonymous"
    
    # 2. Add an AuditLog for the decision
    action_type = "DECISION_ACCEPTED" if request.action == "Accept" else "DECISION_OVERRIDDEN"
    actor_name = f"{request.user_id or 'Unknown'} ({request.user_role or 'No Role'})"
    details_str = f"Action: {request.action}"
    if request.reason:
        details_str += f" | Reason: {request.reason}"
        
    audit = AuditLog(
        case_id=case_id,
        action=action_type,
        actor=actor_name,
        details=details_str,
        created_at=datetime.datetime.utcnow().isoformat()
    )
    db.add(audit)
    db.commit()
    
    return {
        "status": "success",
        "case_id": case_id,
        "decision": request.action,
        "message": f"Successfully recorded '{request.action}' for case {case_id}."
    }

@router.get("/audit-logs")
def get_audit_logs(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).all()
    return [
        {
            "id": log.id,
            "case_id": log.case_id,
            "action": log.action,
            "actor": log.actor,
            "details": log.details,
            "created_at": log.created_at
        }
        for log in logs
    ]
