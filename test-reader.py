from tornado.platform.asyncio import AsyncIOMainLoop
import nsq, asyncio

def finish_pub(conn, data):
    print(data)
    print(conn)

def message_handler(message: nsq.Message):
    message.enable_async()
    print(message.body)
    message.finish()


async def push_to_nsq():

    reader = nsq.Reader(
            topic="nsq-test-writer", channel="test-ch", message_handler=message_handler,
            lookupd_connect_timeout=10, requeue_delay=10, 
            nsqd_tcp_addresses=['localhost:4150'], max_in_flight=5, snappy=False
    )

if __name__ == "__main__":

    from tornado.platform.asyncio import AsyncIOMainLoop

    loop = asyncio.get_event_loop()
    AsyncIOMainLoop().install()
    loop.create_task(push_to_nsq())
    loop.run_forever()