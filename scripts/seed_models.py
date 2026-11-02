"""Идемпотентный сидер моделей. Запуск: python -m scripts.seed_models"""
import asyncio

from sqlalchemy import select

from app.db.models import Model, ModelCategory
from app.db.session import dispose_engine, session_scope

SEED = [
    dict(
        slug="echo-1",
        provider="echo",
        provider_model="echo",
        title="Echo (заглушка)",
        category=ModelCategory.TEXT,
        price=1,
    ),
    dict(
        slug="gpt-4o-mini",
        provider="openai",
        provider_model="gpt-4o-mini",
        title="GPT-4o mini",
        category=ModelCategory.TEXT,
        price=2,
    ),
]


async def main() -> None:
    async with session_scope() as s:
        for row in SEED:
            exists = await s.scalar(select(Model).where(Model.slug == row["slug"]))
            if exists is None:
                s.add(Model(**row))
    await dispose_engine()


if __name__ == "__main__":
    asyncio.run(main())