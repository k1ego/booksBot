from aiogram import Dispatcher

from handlers.start import router as start_router
from handlers.info import router as info_router
from handlers.catalog import router as catalog_router

def register_routes(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(info_router)
    dp.include_router(catalog_router)

