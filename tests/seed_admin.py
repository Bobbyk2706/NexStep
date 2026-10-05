from app.database.session import SessionLocal
from app.models.admin import Admin
from app.auth.security import hash_password

db = SessionLocal()
db.add(Admin(name="Admin Test", email="admin@test.com",
             password_hash=hash_password("adminpass123"), account_status="active"))
db.commit()
print("admin created")