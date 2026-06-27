import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()


        request.state.request_id = request_id

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        response.headers["X-Request-ID"] = request_id 
        response.headers["X-Process-Time"] = f"{process_time:.3f}s"

        print(
            f"{request.method} "
            f"{request.url.path} "
            f"{response.status_code} "
            f"{process_time:.3f}s "
            f"{request_id}"
        )

        return response