from app.database.session import SessionLocal
from app.models.official_notification import OfficialNotification
from app.models.extraction_history import ExtractionHistory
import datetime
def create_pending_extractions(extraction_id):
    db=SessionLocal()
    extraction=ExtractionHistory(extraction_status='PENDING')
    db.add(extraction)
    db.commit()
