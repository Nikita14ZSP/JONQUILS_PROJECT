from app.infrastructure.schemas.mechanic_schemas import SMechanicGet, SMechanicFixesGet
from app.repositories.mechanic_repository import MechanicRepository


async def get_all_mechanics():
    mechanics = await MechanicRepository.get_all()

    mechanics = [
        SMechanicGet(
            **{
                **mechanic_data.__dict__,
                **user_data.__dict__
            }
        ) for (mechanic_data, user_data) in mechanics
    ]

    return mechanics


async def get_mechanic_by_id(mechanic_id: int):
    mechanic = await MechanicRepository.get_by_mechanic_id(mechanic_id=mechanic_id)

    mechanic_data, user_data = mechanic
    mechanic_dict = {**mechanic_data.__dict__, **user_data.__dict__}

    return SMechanicGet(**mechanic_dict)


async def get_mechanic_fixes(mechanic_id: int):
    mechanic_fixes = await MechanicRepository.get_mechanic_fixes(mechanic_id=mechanic_id)

    mechanic_fixes = [
        SMechanicFixesGet(
            **{
                **fix_data.__dict__,
                **car_data.__dict__
            }
        ) for (mechanic_id, fix_data, car_data) in mechanic_fixes
    ]

    return mechanic_fixes