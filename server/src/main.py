from fastapi import FastAPI
from .core import settings, lifespan, debate_exception_handler, generic_exception_handler, DebateException
from .v1 import api_router
from .middleware import LoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.include_router(
    api_router,
    prefix="/api/v1"
)

app.add_exception_handler(DebateException, debate_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
