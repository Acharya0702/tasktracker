from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

from app.config import settings


def test_migrations_upgrade_and_downgrade(tmp_path, monkeypatch):
    database_url = f"sqlite:///{(tmp_path / 'migration.db').as_posix()}"
    monkeypatch.setattr(settings, "database_url", database_url)
    config = Config("alembic.ini")
    command.upgrade(config, "head")
    engine = create_engine(database_url)
    try:
        assert {"users", "projects", "tasks"} <= set(inspect(engine).get_table_names())
        command.check(config)
        command.downgrade(config, "base")
        assert not {"users", "projects", "tasks"} & set(inspect(engine).get_table_names())
    finally:
        engine.dispose()
