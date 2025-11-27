import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.endpoints.favorites_router import favorites_router
from app.messaging.rabbitmq import rabbitmq_client

logger = logging.getLogger(__name__)


async def handle_order_event(message: dict):
    """Обработчик событий о заказах"""
    event_type = message.get("event_type")
    order_id = message.get("order_id")
    user_id = message.get("user_id")
    logger.info(f"Received event: {event_type} for order {order_id}, user {user_id}")
    # Здесь можно добавить логику обработки, например, уведомления пользователя


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await rabbitmq_client.connect()
    
    # Запускаем consumer в фоне для каждого типа события
    async def start_consumers():
        # Подписываемся на разные события заказов
        for event_type in ["order.created", "order.paid", "order.delivered", "order.canceled"]:
            asyncio.create_task(
                rabbitmq_client.consume(
                    queue_name=f"favorites_{event_type}",
                    callback=handle_order_event,
                    exchange_name="orders",
                    routing_key=event_type
                )
            )
    
    # Запускаем consumers
    asyncio.create_task(start_consumers())
    
    yield
    # Shutdown
    await rabbitmq_client.disconnect()


app = FastAPI(title="Favorites Service", lifespan=lifespan)
app.include_router(favorites_router, prefix="/api")
