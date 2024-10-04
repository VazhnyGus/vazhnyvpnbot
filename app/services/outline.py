from outline_vpn import OutlineVPN, OutlineKey

from app.utils.config import config


client = OutlineVPN(config.outline_api_url)


async def create_new_outline_key() -> OutlineKey:
    await client.init(config.outline_api_cert)
    return await client.create_key()


async def delete_outline_key(key_id: int) -> bool:
    await client.init(config.outline_api_cert)
    return await client.delete_key(key_id)
