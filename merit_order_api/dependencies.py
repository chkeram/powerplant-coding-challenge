from functools import lru_cache


from merit_order_api.settings import Settings


@lru_cache()
def get_settings() -> Settings:
    return Settings()
