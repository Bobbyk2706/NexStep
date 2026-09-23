from app.scheduler.monitoring_scheduler import (
    run_monitoring_cycle_now,
)


def main() -> None:

    result = run_monitoring_cycle_now()

    print(
        "Monitoring cycle completed."
    )

    print(
        f"Notifications found: "
        f"{result['notifications_found']}"
    )

    print(
        f"Notifications processed: "
        f"{result['notifications_processed']}"
    )

    print(
        f"Successful: "
        f"{result['successful']}"
    )

    print(
        f"Failed: "
        f"{result['failed']}"
    )


if __name__ == "__main__":
    main()