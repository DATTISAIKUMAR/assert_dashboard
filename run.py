from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from login import router
from manage import dashboard
from edit_delete import edit
from filters import filter
from desktop import desktop

app=FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router,tags=["login"])
app.include_router(dashboard,tags=["managing system data"])
app.include_router(edit,tags=["edit managing system data"])
app.include_router(filter,tags=["filter data"])
app.include_router(desktop,tags=["desktop dashboard data"])

