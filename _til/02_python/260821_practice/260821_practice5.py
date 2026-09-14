# chap11-3 문제 2
import httpx
import asyncio

todo = [1, 2, 3, 4, 5]


async def fetch_todo_by_id(id):
    async with httpx.AsyncClient() as client:
        url = f"https://jsonplaceholder.typicode.com/todos/{id}"

        res = await client.get(url)
        result = res.json()

        return f"id: {result['id']} | title: {result['title']}"

    
async def main():
    fetch_lists = [fetch_todo_by_id(i) for i in range(1, 6)]

    result = await asyncio.gather(*fetch_lists)

    for r in result:
        print(r)

asyncio.run(main())
