import asyncio
from asyncio import AbstractEventLoop
from http_rquest_tr_protocol import HTTPGetClientProtocol


async def make_reaquest(host: str, port: int, loop: AbstractEventLoop):
    def protocol_factory():
        return HTTPGetClientProtocol(host, loop)
    
    _, protocol = await loop.create_connection(protocol_factory, host=host,
                                               port=port)
    
    return await protocol.get_respnse()

async def main():
    loop = asyncio.get_running_loop()
    result = await make_reaquest('www.example.com', 800, loop)
    print(result)

asyncio.run(main())


