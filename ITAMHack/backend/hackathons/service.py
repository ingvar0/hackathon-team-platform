

from backend.hackathons.models import Hackathon
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date





async def get_hack_by_id(session: AsyncSession, hack_id: int) -> Hackathon | None:
    result = session.execute(select(Hackathon).where(Hackathon.hack_id == hack_id))
    hack = result.scalars().first()
    return hack

async def all_hacks(session: AsyncSession) -> list[Hackathon]:
    result = await session.execute(select(Hackathon))
    return result.scalars().all()


async def create_hack(session: AsyncSession, description: str, pic: str, event_date: date, title: str) -> Hackathon:
    new_hack = Hackathon(
        title=title,
        pic=pic,
        description=description,
        event_date=event_date,
    )

    session.add(new_hack)
    await session.commit()
    await session.refresh(new_hack)

    return new_hack


async def update_hack(session: AsyncSession, description: str, pic: str, event_date: date, hack: Hackathon, title: str) -> Hackathon:

    hack.title=title
    hack.description=description
    hack.pic=pic
    hack.event_date=event_date

    await session.commit()
    await session.refresh(hack)

    return hack

async def delete_hack(session: AsyncSession, hack: Hackathon) -> None:
    await session.delete(hack)
    await session.commit()

