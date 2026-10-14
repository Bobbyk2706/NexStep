# python admin_tool.py list   
# python admin_tool.py create 


import sys
import getpass

from app.database.session import SessionLocal
from app.models.admin import Admin
from app.auth.security import hash_password


def list_admins(db):
    rows = db.query(Admin).order_by(Admin.admin_id).all()
    print(f"{len(rows)} admin account(s)")
    for a in rows:
        print(f"  id={a.admin_id}  {a.name}  {a.email}  status={a.account_status}")


def create_admin(db):
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    if db.query(Admin).filter(Admin.email == email).first():
        print("An admin with that email already exists.")
        return
    password = getpass.getpass("Password (min 8 chars): ")
    if len(password) < 8:
        print("Password too short.")
        return
    if password != getpass.getpass("Confirm password: "):
        print("Passwords don't match.")
        return
    db.add(Admin(
        name=name,
        email=email,
        password_hash=hash_password(password),
        account_status="active",
    ))
    db.commit()
    print("Admin created.")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    with SessionLocal() as db:
        if cmd == "list":
            list_admins(db)
        elif cmd == "create":
            create_admin(db)
        else:
            print("Usage: python admin_tool.py list | create")