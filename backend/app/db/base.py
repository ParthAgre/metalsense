# Import all the models, so that Base has them before being
# imported by Alembic or init_db
from app.db.base_class import Base
from app.db.models.user import User
