import asyncio
import logging
from datetime import datetime
from aiowebsocket.converses import AioWebSocket


async def startup(uri):
    async with AioWebSocket(uri) as aws:
        converse = aws.manipulator
        # 客户端给服务端发送消息
        await converse.send('{"action":"subscribe","args":["QuoteBin5m:14"]}')
        while True:
            mes = await converse.receive()
            print('{time}-Client receive: {rec}'
                  .format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rec=mes))


if __name__ == '__main__':
    remote = 'wss://api.bbxapp.vip/v1/ifcontract/realTime'
    try:
        asyncio.get_event_loop().run_until_complete(startup(remote))
    except KeyboardInterrupt as exc:
        logging.info('Quit.')


