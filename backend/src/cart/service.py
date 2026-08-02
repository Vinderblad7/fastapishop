def get_cart_cache_key(user_id: int) -> str:
    return f"cart:user:{user_id}"