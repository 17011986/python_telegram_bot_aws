import math
from bs4 import BeautifulSoup
import fake_useragent
import aiohttp
import asyncio
import config
class Man:
    def __init__(self, z, toyear, stryear, model, make):
        self.z = int(z)
        self.make = make
        self.model = model
        self.stryear = stryear
        self.toyear = toyear

        self.data = {
            'pf.username': f'{config.ManheimLogin}',
            'pf.pass': f'{config.ManheimPass}',
            'ok': 'clicked',
            'pf.adapterld': 'ManheimDirectoryFA'
        }
        self.data2 = {
            'make': self.make,
            'model': self.model,
            'fromYear': self.stryear,
            'toYear': self.toyear,
        }
        self.cars =[]
        self.otch = list()
        self.user = fake_useragent.UserAgent().random
        self.header = {
            'user-agent' : self.user
        }
        self.LoginURL = "https://profiles-ui.manheim.com/profile"
        self.URL = "https://api.manheim.com/oauth2/authorization.oauth2?adaptor=manheim_customer&client_id=qdp6ewmug522t9umyxyqydnx&response_type=code&scope=openid&redirect_uri=https%3A%2F%2Fmembers.manheim.com%2Fgateway%2Fcallback"
        self.SEC_URL = "https://www.manheim.com/members/powersearch/searchResults.do"
        self.loop = asyncio.get_event_loop()
    async def get_registr(self):

        session = aiohttp.ClientSession()

        reg =  await session.post(self.URL, params=self.data, headers=self.header)

        resp = await session.post(self.SEC_URL, params=self.data2, headers=self.header)

        soup = BeautifulSoup(await resp.text(), 'lxml')
        page = soup.find('div', class_='vehicleResultRow').find('a', class_="visitedLink").get('onclick')
        total_page = page.split(' 0,')[1].split(')')[0].replace("'", "")
        print(total_page)
        x = int(total_page)
        c = 25
        if x > c:
            x = math.ceil(x / c)
            for i in range(0, x):
                self.data2.update(
                    {'searchResultsOffset': i * 25})

                resp = await session.post(self.SEC_URL, data=self.data2, headers=self.header)
                resp1 = await resp.text()

                soup = BeautifulSoup(resp1, 'lxml')
                items = soup.find_all('div', class_='vehicleResultRow')
                for item in items:
                    cena = item.find('input', attrs={"name": "BUY NOW"})
                    if cena:
                        cena1 = cena['value'].replace('Buy Now $', '').replace('Buy Now C$', '').replace(',', '')
                        try:
                            vin = cena['onmousedown'].split("', '")[3]
                        except:
                            pass
                        self.cars.append({
                            'cena': int(cena1),
                            'vin': vin
                        })

            await session.close()            # print(self.cars)
            for value in self.cars:
                    if value.get('cena') <= self.z:
                        self.otch.append(value)




            return (self.otch)

        else:
            resp = await session.post(self.SEC_URL, data=self.data2, headers=self.header)
            resp1 = await resp.text()
            await session.close()
            soup = BeautifulSoup(resp1, 'lxml')
            items = soup.find_all('div', class_='vehicleResultRow')
            for item in items:
                cena = item.find('input', attrs={"name": "BUY NOW"})
                if cena:
                    cena1 = cena['value'].replace('Buy Now $', '').replace('Buy Now C$', '').replace(',', '')
                    try:
                        vin = cena['onmousedown'].split("', '")[3]
                    except:
                          pass
                    self.cars.append({
                    'cena': int(cena1),
                    'vin' : vin
                                     })

            for value in self.cars:
                    if value.get('cena') <= self.z:
                        self.otch.append(value)




            return (self.otch)