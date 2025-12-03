from pathlib import Path
import base64


from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.hackathons.schemas import HackInfo, UpdateHackInfo, CreateHack
from backend.hackathons.service import update_hack, create_hack, all_hacks, get_hack_by_id, delete_hack


router = APIRouter(prefix="/hackathons", tags=["hackathons"])
BASE_DIR = Path(__file__).resolve().parent.parent
HACK_DIR = BASE_DIR / "data" / "hackathons"
HACK_DIR.mkdir(parents=True, exist_ok=True)
SUPPORTED_AVATAR_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif")


def load_hack(hack_id: int) -> bytes:
    for ext in SUPPORTED_AVATAR_EXT:
        candidate =  HACK_DIR / f"{str(hack_id)}{ext}"
        if candidate.exists():
            return candidate.read_bytes()
    return b""

#Общедоступные методы -----------------------------------------------------------------------------------------------------------------
@router.get("", response_model=list[HackInfo])
async def all_hacks_info(
    session: AsyncSession = Depends(get_db),
):
    hacks = await all_hacks(session=session)

    return [
        HackInfo(
            hack_id=hack.hack_id,
            title=hack.title or "",
            description=hack.description or "",
            pic=base64.b64encode(load_hack(hack.hack_id)).decode(),
            event_date=hack.event_date
        )
        for hack in hacks if hack
    ]

@router.get("/{hack_id}", response_model=HackInfo)
async def hack_info(
    hack_id: int,
    session: AsyncSession = Depends(get_db),
) -> HackInfo:
    hack = await get_hack_by_id(session=session, hack_id=hack_id)

    if not hack:
        raise HTTPException(status_code=404, detail="Hack not found")

    return HackInfo(
        hack_id=hack.hack_id,
        title=hack.title or "",
        description=hack.description or "",
        pic=base64.b64encode(load_hack(hack.hack_id)).decode(),
        event_date=hack.event_date
    )
#-----------------------------------------------------------------------------------------------------------------------------------------


#Методы админа ---------------------------------------------------------------------------------------------------------------------------
@router.post("/{hack_id}/update_hack", response_model=HackInfo)
async def update_hack_info(
    hack_id: int,
    data: UpdateHackInfo,
    session: AsyncSession = Depends(get_db),
) -> HackInfo:
    hack = await get_hack_by_id(session=session, hack_id=hack_id)

    if not hack:
        raise HTTPException(status_code=404, detail="Hack not found")

    hack = await update_hack(
        session=session,
        hack=hack,
        title=data.title,
        event_date=data.event_date,
        description=data.description,
        pic=data.pic,
    )

    return HackInfo(
        hack_id=hack.hack_id,
        title=hack.title or "",
        description=hack.description or "",
        pic=base64.b64encode(load_hack(hack.hack_id)).decode(),
        event_date=hack.event_date
    )


@router.post("/{hack_id}/delete_hack", response_model=HackInfo)
async def delete_hack_info(
    hack_id: int,
    session: AsyncSession = Depends(get_db),
) -> str:
    hack = await get_hack_by_id(session=session, hack_id=hack_id)

    if not hack:
        raise HTTPException(status_code=404, detail="Hack not found")

    await delete_hack(session=session, hack=hack)

    return 'Успешно удалено'



@router.post("/create_hack", response_model=CreateHack)
async def create_hack_endpoint(
        data: CreateHack,
        session: AsyncSession = Depends(get_db),
) -> HackInfo:
    hack = await create_hack(session=session,
                             title=data.title,
                             description=data.description,
                             pic=data.pic,
                             event_date=data.event_date)

    return HackInfo(
        hack_id=hack.hack_id,
        title=hack.title or "",
        description=hack.description or "",
        pic=base64.b64encode(load_hack(hack.hack_id)).decode(),
        event_date=hack.event_date
    )


#-----------------------------------------------------------------------------------------------------------------------------------------


