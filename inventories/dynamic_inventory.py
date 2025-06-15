#!/usr/bin/env python3

import json
import argparse

def get_inventory_data():
    """
    Возвращает структуру инвентаря в виде словаря.
    """
    return {
        # ГРУППЫ И ХОСТЫ
        "staging": {
            "children": [
                "staging_webservers",
                "staging_dbservers"
            ]
        },
        "production": {
            "children": [
                "prod_webservers",
                "prod_dbservers"
            ]
        },
        "staging_webservers": {
            "hosts": ["stage-web-01"]
        },
        "staging_dbservers": {
            "hosts": ["stage-db-01"]
        },
        "prod_webservers": {
            "hosts": ["prod-web-01"]
        },
        "prod_dbservers": {
            "hosts": ["prod-db-01"]
        },

        # ПЕРЕМЕННЫЕ ДЛЯ ХОСТОВ (_meta) 
        "_meta": {
            "hostvars": {
                "stage-web-01": {
                    "ansible_host": "localhost",
                    "ansible_connection": "local",
                    "some_custom_var": "value_for_stage_web"
                },
                "stage-db-01": {
                    "ansible_host": "localhost",
                    "ansible_connection": "local"
                },
                "prod-web-01": {
                    "ansible_host": "localhost",
                    "ansible_connection": "local",
                    "some_custom_var": "value_for_prod_web"
                },
                "prod-db-01": {
                    "ansible_host": "localhost",
                    "ansible_connection": "local"
                }
            }
        }
    }

# ЛОГИКА ОБРАБОТКИ АРГУМЕНТОВ 
# Ansible может вызывать скрипт с аргументом --list или --host <hostname>
def main():
    parser = argparse.ArgumentParser(description="Simple Dynamic Inventory Script")
    parser.add_argument('--list', action='store_true', help="List all inventory groups and hosts")
    parser.add_argument('--host', help="Get all variables about a specific host")
    args = parser.parse_args()

    inventory = get_inventory_data()

    if args.list:
        # При вызове с --list, Ansible ожидает ВСЮ структуру (кроме _meta)
        output = {}
        for group, data in inventory.items():
            if group != "_meta":
                output[group] = data
        print(json.dumps(output, indent=4))

    elif args.host:
        # При вызове с --host, Ansible ожидает переменные для этого хоста
        # Мы просто вернем пустой JSON, т.к. все переменные уже в _meta
        print(json.dumps(inventory["_meta"]["hostvars"].get(args.host, {}), indent=4))

    else:
        # По умолчанию (если нет аргументов), можно считать это как --list
        output = {}
        for group, data in inventory.items():
            if group != "_meta":
                output[group] = data
        print(json.dumps(output, indent=4))


if __name__ == "__main__":
    main()
