from bot import dp
from filters.rights import RightsFilter

dp.filters_factory.bind(RightsFilter)