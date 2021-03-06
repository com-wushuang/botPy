from telethon import TelegramClient
import db

api_id = 1234567
api_hash = "abcdefghigklmnopqrst123456789"

client = TelegramClient(
    "user",
    api_id,
    api_hash,
    proxy=("socks5", '127.0.0.1', 1080),
)


async def main():
    ads = db.list_ads()
    for ad in ads:
        await client.send_message("hao1234bot", ad['key'])
        reply = await client.get_messages("hao1234bot", limit=1)
        for item in reply[0].entities:
            try:
                await client.send_message(item.url, ad['content'])
            except Exception as e:
                print(e)


with client:
    client.loop.run_until_complete(main())
