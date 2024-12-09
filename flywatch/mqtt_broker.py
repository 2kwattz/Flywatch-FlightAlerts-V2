from hbmqtt.broker import Broker
import asyncio

broker_config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '0.0.0.0:1883',
        }
    },
    'sys_interval': 60,
    'topic-check': {
        'enabled': True
    }
}

async def start_broker():
    broker = Broker(broker_config)
    await broker.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_broker())
        loop.run_forever()
        print("MQTT BROKER HAS BEEN STARTED")
    except KeyboardInterrupt:
        print("Broker stopped manually")
    finally:
        loop.stop()
