# chapter11-3 문제 3
import httpx
import asyncio

async def fetch_todo(num):

    async with httpx.AsyncClient() as client:
        url = f"https://jsonplaceholder.typicode.com/todos/{num}"

        
        try:
            res = await client.get(url)
            res.raise_for_status()
            result = res.json()
            return result['id'], result['title']
            

        except httpx.HTTPError as error:
           print(f"경고: {num}번 게시글 다운로드 실패 ({error}). 빈 값으로 대체 후 처리를 지속합니다.")
           return {'id': num, 'title': "수집 에러 대체 데이터"}

async def main():
    trying = [1, 2, 3, 999]
    fetch_lists = [fetch_todo(i) for i in trying]
    results = await asyncio.gather(*fetch_lists)
    for r in results:
        print(r)

asyncio.run(main())
