import logging
import uvicorn
from src.server.config import PORT


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    uvicorn.run("src.server.main:app", host="localhost",
                port=PORT, reload=False)
