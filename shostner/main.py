from fastapi import FastAPI
from .db.mongodb_utils import close_mongo_connection, connect_to_mongo


urls = {
    "google": "http://www.google.com.br",
    "jlugao": "http://jlugao.com"
}


def get_app() -> FastAPI:
    from .views.data import router as data_router
    from .views.links import router as links_router
    from .views.users import router as users_router
    from .views.login import router as login_router
    app = FastAPI()
    app.add_event_handler("startup", connect_to_mongo)
    app.add_event_handler("shutdown", close_mongo_connection)
    app.include_router(login_router)
    app.include_router(data_router, prefix="/logs")
    app.include_router(users_router, prefix="/users")
    app.include_router(links_router)
    return app

app = get_app()


"""
url.jlugao.com/live10
-> slides


- Link + curto do que speackerdeck.com/fulano/xyz

- Analytics -> na live do edu eu recebi 50 acessos
            -> numa talk no grupy-sp eu recebi 20 acessos


"""



