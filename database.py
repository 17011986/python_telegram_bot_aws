import logging
import pickle
import redis
import ujson
import config


class Cache(redis.StrictRedis):
    def __init__(self, host, port, password,
                 charset="utf-8",
                 decode_responses=True):
        super(Cache, self).__init__(host, port,
                                    password=password,
                                    charset=charset,
                                    decode_responses=decode_responses)
        logging.info("Redis start")

    def jset(self, name, value, ex=0):
        """функция конвертирует python-объект в Json и сохранит"""
        return self.setex(name, ex, ujson.dumps(value))

    def jget(self, name):
        """функция возвращает Json и конвертирует в python-объект"""
        r = self.get(name)
        if r is None:
            return r
        return ujson.loads(r)

cache = Cache(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD
)
r = redis.StrictRedis('localhost',6379,0,config.REDIS_PASSWORD)
# database = Database(config.BOT_DB_NAME)
p_mydict = pickle.dumps(config.TOYOTA)
r.set('TOYOTA', p_mydict)
p_mydict1 = pickle.dumps(config.Chevrolet)
r.set('Chevrolet', p_mydict1)
p_mydict2 = pickle.dumps(config.TESLA)
r.set('TESLA', p_mydict2)
p_mydict3 = pickle.dumps(config.LEXUS)
r.set('LEXUS', p_mydict3)
p_mydict4 = pickle.dumps(config.NISSAN)
r.set('NISSAN', p_mydict4)
p_mydict5 = pickle.dumps(config.HONDA)
r.set('HONDA', p_mydict5)
p_mydict6 = pickle.dumps(config.MAZDA)
r.set('MAZDA', p_mydict6)
p_mydict7 = pickle.dumps(config.SUBARU)
r.set('SUBARU', p_mydict7)

# Copart

p_mydictcop = pickle.dumps(config.Copart_TOYOTA)
r.set('Copart_TOYOTA', p_mydictcop)
p_mydictcop1 = pickle.dumps(config.Copart_HONDA)
r.set('Copart_HONDA', p_mydictcop1)
p_mydictcop2 = pickle.dumps(config.Copart_TESLA)
r.set('Copart_TESLA', p_mydictcop2)
p_mydictcop3 = pickle.dumps(config.Copart_LEXUS)
r.set('Copart_LEXUS', p_mydictcop3)
p_mydictcop4 = pickle.dumps(config.Copart_NISSAN)
r.set('Copart_NISSAN', p_mydictcop4)
p_mydictcop5 = pickle.dumps(config.Copart_MAZDA)
r.set('Copart_MAZDA', p_mydictcop5)
p_mydictcop6 = pickle.dumps(config.Copart_SUBARU)
r.set('Copart_SUBARU', p_mydictcop6)
p_mydictcop7 = pickle.dumps(config.Copart_Chevrolet)
r.set('Copart_Chevrolet', p_mydictcop7)

