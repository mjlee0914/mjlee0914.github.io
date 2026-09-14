# chap11-2 문제 3
import asyncio
import time

async def send_notification(customer, seconds):
    print(f"{customer}에게 문자를 발송합니다")
    await asyncio.sleep(seconds)
    print(f"{customer}에게 문자가 전송되었습니다")


async def main():

    start_time = time.perf_counter()
    await asyncio.gather(
        send_notification("고객 A", 1),
        send_notification("고객 B", 3),
        send_notification("고객 C", 2)
    )

    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print(f"작업에 걸린 총 소요 시간: {elapsed:.2f}초")

# in jupyter notebook
# await main()
# in .py
asyncio.run(main())