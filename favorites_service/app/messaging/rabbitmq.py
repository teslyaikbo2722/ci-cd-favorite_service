import json
import logging
from typing import Optional, Callable, Any
from aio_pika import connect_robust, Message, IncomingMessage
from aio_pika.abc import AbstractConnection, AbstractChannel, AbstractQueue
from app.settings import settings

logger = logging.getLogger(__name__)


class RabbitMQClient:
    """Клиент для работы с RabbitMQ"""
    
    def __init__(self):
        self.connection: Optional[AbstractConnection] = None
        self.channel: Optional[AbstractChannel] = None
    
    async def connect(self):
        """Установить соединение с RabbitMQ"""
        try:
            self.connection = await connect_robust(settings.rabbitmq_url)
            self.channel = await self.connection.channel()
            logger.info("Connected to RabbitMQ")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    async def disconnect(self):
        """Закрыть соединение с RabbitMQ"""
        if self.connection:
            await self.connection.close()
            logger.info("Disconnected from RabbitMQ")
    
    async def publish(self, exchange_name: str, routing_key: str, message: dict):
        """Опубликовать сообщение в очередь"""
        if not self.channel:
            await self.connect()
        
        exchange = await self.channel.declare_exchange(
            exchange_name,
            type="topic",
            durable=True
        )
        
        message_body = json.dumps(message).encode()
        await exchange.publish(
            Message(message_body),
            routing_key=routing_key
        )
        logger.info(f"Published message to {exchange_name}/{routing_key}")
    
    async def consume(
        self,
        queue_name: str,
        callback: Callable[[dict], Any],
        exchange_name: Optional[str] = None,
        routing_key: Optional[str] = None
    ):
        """Подписаться на очередь и обрабатывать сообщения"""
        if not self.channel:
            await self.connect()
        
        # Объявить exchange, если указан
        if exchange_name:
            exchange = await self.channel.declare_exchange(
                exchange_name,
                type="topic",
                durable=True
            )
        else:
            exchange = None
        
        # Объявить очередь
        queue = await self.channel.declare_queue(queue_name, durable=True)
        
        # Привязать очередь к exchange, если указан
        if exchange and routing_key:
            await queue.bind(exchange, routing_key)
        
        async def process_message(message: IncomingMessage):
            async with message.process():
                try:
                    body = json.loads(message.body.decode())
                    await callback(body)
                    logger.info(f"Processed message from {queue_name}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
                    # Можно добавить логику повторной обработки или отправки в DLQ
        
        await queue.consume(process_message)
        logger.info(f"Started consuming from {queue_name}")


# Глобальный экземпляр клиента
rabbitmq_client = RabbitMQClient()

