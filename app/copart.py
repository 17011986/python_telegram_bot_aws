import asyncio
import aiohttp
import fake_useragent
import config


class Copart():
    def __init__(self, cena, strdata, findata, make, model):
        self.cana = int(cena)
        self.strdata = int(strdata)
        self.findata = findata
        self.make = make
        self.model = model
        self.url = f'{config.CopartURL}'
        self.url1 = f'{self.url}{self.make}&from_year={self.strdata-1}-{self.findata}&model_group={self.model.split(" ")[0]}'
        self.user = fake_useragent.UserAgent().random
        self.loop = asyncio.get_event_loop()
        self.headers = {
            'user-agent': self.user
                       }

    async def coro(self):
            jar = aiohttp.CookieJar(unsafe=True)
            session = aiohttp.ClientSession()
            response = await session.get(self.url1, headers=self.headers)
            text = await response.json()
            await session.close()
            if int(text["count"]) >= 50:
                self.url1 = f'{self.url1}&limit={text["count"]}'
                jar = aiohttp.CookieJar(unsafe=True)
                session = aiohttp.ClientSession()
                response = await session.get(self.url1, headers=self.headers)
                text = await response.json()
                await session.close()
                data = []
                dara = list()
                for m in text['list']:
                    if m["buy_now_price"] == 0:
                        pass
                    elif int(m["buy_now_price"]) <= self.cana:
                        data.append(m)
                if data == []:
                    return None
                else:
                    for x in data:
                        dara.append(f'Лот https://www.copart.com/ru/lot/{x["id"]}, с ценой {x["buy_now_price"]}$\n')
                    answer = ""
                    return answer.join(dara)
            else:
                data = []
                dara = list()
                for m in text['list']:
                    if m["buy_now_price"] == 0:
                        pass
                    elif int(m["buy_now_price"]) <= self.cana:
                        data.append(m)
                if data == []:
                    return None
                else:
                    for x in data:
                        dara.append(f'Лот https://www.copart.com/ru/lot/{x["id"]}, с ценой {x["buy_now_price"]}$\n')
                    answer = ""
                    return answer.join(dara)