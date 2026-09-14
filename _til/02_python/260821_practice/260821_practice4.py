# chap11-3 문제 1
import httpx
import asyncio

async def fetch_todo():
    async with httpx.AsyncClient() as client:
        url = f"https://jsonplaceholder.typicode.com/todos/1"

        res = await client.get(url)
        result = res.json()

        print(result['id'], result['title'])

    
asyncio.run(fetch_todo())
