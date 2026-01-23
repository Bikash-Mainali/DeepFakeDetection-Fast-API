import asyncio
import uvicorn

if __name__ == "__main__":
    # Force SelectorEventLoop on Windows instead of ProactorEventLoop
    if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    uvicorn.run("fast-api:app", host="0.0.0.0", port=8000, log_level="info")