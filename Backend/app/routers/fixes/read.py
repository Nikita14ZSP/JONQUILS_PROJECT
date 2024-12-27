from app.infrastructure.schemas.fix_info_schemas import SFixInfoGet
from app.repositories.fix_info_repository import FixInfoRepository


async def get_all_fixes():
    fixes = await FixInfoRepository.get_all()

    fixes = [
        SFixInfoGet(
            **fix[0].__dict__
        ) for fix in fixes
    ]

    return fixes


async def get_by_fix_id(fix_info_id: int):
    fix_info = await FixInfoRepository.get_by_id(fix_info_id=fix_info_id)
    fix_info_data = fix_info[0]

    return SFixInfoGet(**fix_info_data.__dict__)

