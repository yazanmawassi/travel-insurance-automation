import asyncio

from pyzeebe import ZeebeWorker, create_camunda_cloud_channel

from config import (
    CAMUNDA_CLIENT_ID,
    CAMUNDA_CLIENT_SECRET,
    CAMUNDA_CLUSTER_ID,
    CAMUNDA_REGION
)
from tasks import register_tasks


async def main():
    # Verbindung zu Camunda Cloud herstellen.
    channel = create_camunda_cloud_channel(
        client_id=CAMUNDA_CLIENT_ID,
        client_secret=CAMUNDA_CLIENT_SECRET,
        cluster_id=CAMUNDA_CLUSTER_ID,
        region=CAMUNDA_REGION
    )

    # Worker erstellen.
    worker = ZeebeWorker(channel)

    # Alle Service Tasks aus tasks.py registrieren.
    register_tasks(worker)

    print("Worker läuft mit Camunda Cloud...")

    # Worker dauerhaft laufen lassen.
    await worker.work()


if __name__ == "__main__":
    asyncio.run(main())