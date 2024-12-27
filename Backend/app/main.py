from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.access.access import router as access_router
from app.routers.users.users import router as users_router
from app.routers.drivers.drivers import router as drivers_router
from app.routers.mechanics.mechanics import router as mechanics_router
from app.routers.cars.cars import router as cars_router
from app.routers.fixes.fixes import router as fixes_router
from app.routers.rides.rides import router as rides_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любого источника
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, OPTIONS и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)


@app.get("/")
async def root():
    return {"message": "Let it Snow! Let it Snow! Let it Snow!"}


app.include_router(access_router)
app.include_router(users_router)
app.include_router(drivers_router)
app.include_router(mechanics_router)
app.include_router(cars_router)
app.include_router(fixes_router)
app.include_router(rides_router)