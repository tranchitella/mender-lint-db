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
from .logging import logger, setup_logging


def process_tenant(client: MongoClient, tenant: str):
    process_tenant_deviceauth_and_inventory(client, tenant)


def process_tenants(client: MongoClient, tenant_id: List[str], first_tenant_id: str):
    tenantadm = client["tenantadm"]
    tenants_filter = {}
    if tenant_id:
        tenants_filter["_id"] = {"$in": tenant_id}
    elif first_tenant_id:
        tenants_filter["_id"] = {"$lte": first_tenant_id}
    tenants_count = tenantadm.tenants.count_documents(tenants_filter)
    tenants = tenantadm.tenants.find(tenants_filter).sort([("_id", DESCENDING)])
    for i, tenant in enumerate(tenants):
        logger.info(
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
    "--tenant-id",
    help="tenant ID to sync (multiple)",
    multiple=True,
)
@click.option(
    "--first-tenant-id",
    help="first tenant ID to process",
)
@click.option("--debug/--no-debug", default=False)
def main(mongodb_uri: str, tenant_id: List[str], first_tenant_id: str, debug: bool):
    setup_logging(debug)
    client = MongoClient(mongodb_uri)
    process_tenants(client, tenant_id, first_tenant_id)


if __name__ == "__main__":
    main()
