from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from src.app.errors.http_error import http_error_handler
from src.app.errors.validation_error import http422_error_handler
from src.app.core.config import get_app_settings
from src.app.core.events import create_start_app_handler, create_stop_app_handler

from src.authentication.router import router as authentication_router
# from src.users import router as users_router
# from src.profiles import router as profiles_router
# from src.articles import router as articles_router
# from src.comments import router as comments_router
# from src.tags import router as tags_router

def get_application() -> FastAPI:
    settings = get_app_settings()

    print("ENV Loaded:", settings.secret_key.get_secret_value())

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler(
        "startup",
        create_start_app_handler(application, settings),
    )
    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(application),
    )

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    router = APIRouter()
    router.include_router(authentication_router, tags=["authentication"], prefix="/auth")
    # router.include_router(users_router, tags=["users"], prefix="/users")
    # router.include_router(profiles_router, tags=["profiles"], prefix="/profiles")
    # router.include_router(articles_router, tags=["articles"], prefix="/articles")
    # router.include_router(comments_router, tags=["comments"], prefix="/articles/{slug}/comments")
    # router.include_router(tags_router, tags=["tags"], prefix="/tags")

    application.include_router(router, prefix=settings.api_prefix)

    return application


app = get_application()
