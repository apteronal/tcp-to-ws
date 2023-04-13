"""
Example TCP-to-WebSocket tunnel.

Forwards data between a local TCP socket and a WebSocket.
"""

import asyncio
import logging

import websockets


LOCAL_PORT = 12345
URI = 'ws://example.com/foo'


def main():
    """Main function."""
    asyncio.run(run_server())


async def run_server():
    """Run server."""
    server = await asyncio.start_server(handle_client, 'localhost', LOCAL_PORT)
    async with server:
        await server.serve_forever()


async def handle_client(reader, writer):
    """Handle client."""
    logging.debug("Connecting...")
    async with websockets.connect(URI) as websocket:
        logging.debug("Connected.")
        asyncio.create_task(forward_web_to_tcp(websocket, writer))
        asyncio.create_task(forward_tcp_to_web(reader, websocket))
        await asyncio.Future()


async def forward_web_to_tcp(websocket, writer):
    """Forward data received by WebSocket to TCP socket."""
    async for data in websocket:
        logging.debug("Sending %d bytes to TCP socket...", len(data))
        writer.write(data)
        await writer.drain()


async def forward_tcp_to_web(reader, websocket):
    """Forward data received by TCP socket to WebSocket."""
    while True:
        data = await reader.read(4096)
        logging.debug("Sending %d bytes to WebSocket...", len(data))
        await websocket.send(data)


if __name__ == '__main__':
    main()
