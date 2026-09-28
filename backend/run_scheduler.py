from __future__ import annotations

import logging
import time

from app.scheduler.monitoring_scheduler import (
    start_monitoring_scheduler,
    stop_monitoring_scheduler,
)


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)


def main() -> None:

    start_monitoring_scheduler()

    try:

        while True:
            time.sleep(60)

    except KeyboardInterrupt:

        logging.info(
            "Stopping monitoring scheduler."
        )

        stop_monitoring_scheduler()


if __name__ == "__main__":
    main()