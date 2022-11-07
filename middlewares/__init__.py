from bot import dp
from middlewares.throttling import ThrottlingMiddleware
from middlewares.blacklist import BlacklistMiddleware

dp.middleware.setup(ThrottlingMiddleware(limit=0.5))
dp.middleware.setup(BlacklistMiddleware())