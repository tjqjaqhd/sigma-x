from src.sigma.db.database import Base, echo_engine


def init_db() -> None:
    """Create database tables."""
    Base.metadata.create_all(bind=echo_engine)


if __name__ == "__main__":
    init_db()
