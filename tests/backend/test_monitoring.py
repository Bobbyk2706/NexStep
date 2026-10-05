# $env:PYTHONPATH="$PWD\backend"
# uv run python tests\backend\test_monitoring.py > monitoring_result.txt


from app.scheduler.monitoring_scheduler import (
    run_monitoring_cycle_now,
)


if __name__ == "__main__":

    print("=" * 60)
    print("STARTING MONITORING TEST")
    print("=" * 60)

    result = run_monitoring_cycle_now()

    print()
    print("MONITORING RESULT")
    print("=" * 60)

    print(result)

    print("=" * 60)
    print("TEST FINISHED")
    print("=" * 60)