from typing import Optional

from src.app.database.repo import ServerRepo
from src.app.services.pilot_api import ServerNode
from dishka import FromDishka


async def fetch_contracts_by_id(server_id:int, contract_id:str, server_repo:ServerRepo) -> Optional[dict]:
    server = await server_repo.get_server(server_id)
    async with ServerNode(server.admin_url, server.user_url) as node:
        try:
            await node.admin.login()

            data = await node.admin.get_contracts()
            contract_list = data.get("data",[])

            for contract in contract_list:
                if str(contract.get("id")) == contract_id:
                    return contract
            return None
        except Exception as e:
            print(f"ОШИБКА: {e}")
            # raise e