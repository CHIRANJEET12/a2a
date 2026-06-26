from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    print("Starting Debate AI Server...")

    yield

    print("Shutting Down...")