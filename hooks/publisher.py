# -*- coding: utf-8 -*-

import pika


class RabbitPublisher:
    PERSISTENT_MESSAGE_FLAG = 2

    def __init__(self, login, password, host, port, virtual_host, exchange_name):
        self._login = login
        self._password = password
        self._host = host
        self._port = port
        self._virtual_host = virtual_host
        self._exchange_name = exchange_name

    def __enter__(self):
        credentials = pika.PlainCredentials(self._login, self._password)
        params = pika.ConnectionParameters(host=self._host, port=self._port, virtual_host=self._virtual_host, credentials=credentials)
        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=self._exchange_name, exchange_type="topic", durable=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

    def send_event(self, scope, json_data):
        self._channel.basic_publish(
            exchange=self._exchange_name,
            routing_key=scope,
            body=json_data,
            properties=pika.BasicProperties(
                headers={"__TypeId__": "HookEventMessage"},
                content_encoding="utf-8",
                content_type="application/json",
                delivery_mode=self.PERSISTENT_MESSAGE_FLAG
            )
        )

    def send_hubspot_event(self, json_data):
        self._channel.basic_publish(
            exchange=self._exchange_name,
            routing_key="hubspot",
            body=json_data,
            properties=pika.BasicProperties(
                headers={"__TypeId__": "HubspotEventMessage"},
                content_encoding="utf-8",
                content_type="application/json",
                delivery_mode=self.PERSISTENT_MESSAGE_FLAG
            )
        )
