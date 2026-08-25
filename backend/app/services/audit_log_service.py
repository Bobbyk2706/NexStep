from datetime import datetime

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.admin import Admin
from app.models.audit_log import AuditLog


def create_audit_log(
    admin_id,
    action_type,
    entity_type,
    entity_id,
    description,
    old_value,
    new_value
):
    with SessionLocal() as s:

        admin = None

        if admin_id is not None:
            admin = s.scalar(
                select(Admin).where(
                    Admin.admin_id == admin_id
                )
            )

            if admin is None:
                raise ValueError("Admin not found")

        audit_log = AuditLog(
            action_type=action_type,
            entity_type=entity_type,
            entity_id=entity_id,
            description=description,
            old_value=old_value,
            new_value=new_value,
            created_at=datetime.now()
        )

        if admin is not None:
            admin.audit_logs.append(audit_log)

        s.add(audit_log)
        s.commit()

        return audit_log.audit_id