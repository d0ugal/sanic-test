import asyncio
import collections
import os
import json

from sanic import Sanic
from sanic.response import file

app = Sanic(__name__)


@app.route('/')
async def index(request):
    return await file('websocket.html')


connected = set()
user_agents = collections.defaultdict(int)

@app.websocket('/feed')
async def feed(request, ws):

    connected.add(ws)
    user_agent = request.headers.get('user-agent', 'unknown')
    user_agents[user_agent] += 1
    print("Open WebSockets: ", len(connected))

    try:
        while True:
            await ws.send(json.dumps({
                "user_agents": user_agents,
                "websockets": len(connected),
            }))
            await asyncio.sleep(1)
    finally:
        connected.remove(ws)
        user_agents[user_agent] -= 1
        if user_agents[user_agent] == 0:
            user_agents.pop(user_agent)
        print("Open WebSockets: ", len(connected))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host="0.0.0.0", port=port, debug=True)

