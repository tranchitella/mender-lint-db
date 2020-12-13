# Copyright 2020 Northern.tech AS
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http:#www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from typing import List

import click

from pymongo import MongoClient, DESCENDING

from .deviceauth_and_inventory import process_tenant_deviceauth_and_inventory
from .logging import logger


def process_tenant(client: MongoClient, tenant: str):
    process_tenant_deviceauth_and_inventory(client, tenant)


def process_tenants(client: MongoClient, tenant_id: List[str]):
    tenantadm = client["tenantadm"]
    tenants_count = tenantadm.tenants.count_documents({})
    tenants_filter = {}
    if tenant_id:
        tenants_filter["_id"] = {"$in": tenant_id}
    tenants = tenantadm.tenants.find(tenants_filter).sort([("_id", DESCENDING)])
    for i, tenant in enumerate(tenants):
        logger.debug(
            "Processing tenant ID: %s (%d/%d)", tenant["_id"], i + 1, tenants_count
        )
        process_tenant(client, tenant)


@click.command()
@click.option(
    "--mongodb-uri",
    default="mongodb:#localhost:27017",
    help="connection URI to the mongodb",
)
@click.option(
    "--tenant-id", help="connection URI to the mongodb", multiple=True,
)
def main(mongodb_uri: str, tenant_id: List[str]):
    client = MongoClient(mongodb_uri)
    process_tenants(client, tenant_id)


if __name__ == "__main__":
    main()
