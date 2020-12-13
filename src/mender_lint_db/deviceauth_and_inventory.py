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
 
from pymongo import MongoClient, ASCENDING

from .logging import logger


def process_tenant_deviceauth_and_inventory(client: MongoClient, tenant: str):
    deviceauth = client["deviceauth-" + tenant["_id"]]
    inventory = client["inventory-" + tenant["_id"]]
    # verify sync between deviceauth and inventory
    filter_devices = {"status": {"$ne": "preauthorized"}}
    devices_count = deviceauth.devices.count_documents(filter_devices)
    devices = deviceauth.devices.find(filter_devices).sort([("_id", ASCENDING)])
    for i, device in enumerate(devices):
        logger.debug(
            "- Processing device ID: %s (%d/%d)", device["_id"], i + 1, devices_count
        )
        # get the device from inventory
        device_inventory = inventory["devices"].find_one({"_id": device["_id"]})
        if device_inventory is None:
            logger.error("- Device NOT FOUND!")
            continue
        # get the device status from inventory
        device_inventory_status = (
            device_inventory.get("attributes", {})
            .get("identity-status", {})
            .get("value", None)
        )
        # missing status, set it
        if device_inventory_status is None:
            logger.error(
                "- Device status NOT FOUND in inventory: %s vs. %s",
                device,
                device_inventory,
            )
            inventory.devices.update_one(
                {"_id": device_inventory["_id"]},
                {
                    "$set": {
                        "attributes.identity-status": {
                            "name": "status",
                            "scope": "identity",
                            "value": device["status"],
                        }
                    }
                },
            )
            device_inventory_status = device["status"]
        # verify matching between device status in deviceauth and inventory
        if device_inventory_status != device["status"]:
            logger.error(
                "- Device status MISMATCH: %s vs. %s",
                device_inventory_status,
                device["status"],
            )
            inventory.devices.update_one(
                {"_id": device_inventory["_id"]},
                {"$set": {"attributes.identity-status.value": device["status"]}},
            )
        # verify matching between device revision in deviceauth and inventory
        device_revision = device.get("revision", 0)
        device_inventory_revision = device_inventory.get("revision", 0)
        if device_inventory_revision > device_revision:
            logger.error(
                "- Device revision MISMATCH: %s vs. %s",
                device_inventory_revision,
                device_revision,
            )
            inventory.devices.update_one(
                {"_id": device_inventory["_id"]},
                {"$set": {"revision": device_revision}},
            )
    # verify missing decommissioning in inventory
    inventory_devices_count = inventory.devices.count_documents({})
    if inventory_devices_count == devices_count:
        return
    # we have a mismatch, post-process inventory devices
    devices = inventory.devices.find({}).sort([("_id", ASCENDING)])
    for i, device in enumerate(devices):
        logger.debug(
            "- Post-processing device ID: %s (%d/%d)",
            device["_id"],
            i + 1,
            devices_count,
        )
        # get the device from deviceauth
        device_deviceauth = deviceauth["devices"].find_one({"_id": device["_id"]})
        if device_deviceauth is None:
            logger.error("- Device NOT FOUND in deviceauth: %s", device)
