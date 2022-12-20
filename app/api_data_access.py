from flask import current_app
import json
import requests

class TemplateAPI:

    def list():
        data = TemplateAPI.request_get('list')
        return data


    def option_add(contract_size, coll_asset, settle_asset, start, expiry, strike_price):
        payload = {
            'contract_size': contract_size,
            'coll_asset': coll_asset,
            'settle_asset': settle_asset,
            'start': start,
            'expiry': expiry,
            'strike_price': strike_price
        }
        data = TemplateAPI.request_post(
            'init', payload)
        return data


    def option(contract_id):
        payload = {
            'contract_id': contract_id,
        }
        data = TemplateAPI.request_post(
            'info', payload)
        return data


    def fund(contract_id, num_contracts):
        payload = {
            'contract_id': contract_id,
            'num_contracts' : num_contracts
        }
        data = TemplateAPI.request_post(
            'fund', payload)
        return data


    def cancel(contract_id, num_contracts):
        payload = {
            'contract_id': contract_id,
            "num_contracts" : num_contracts
        }
        data = TemplateAPI.request_post(
            'cancel', payload)
        return data


    def expire(contract_id, num_contracts):
        payload = {
            'contract_id': contract_id,
            "num_contracts" : num_contracts
        }
        data = TemplateAPI.request_post(
            'expire', payload)
        return data


    def exercise(contract_id, num_contracts):
        payload = {
            'contract_id': contract_id,
            "num_contracts" : num_contracts
        }
        data = TemplateAPI.request_post(
            'exercise', payload)
        return data


    def settle(contract_id, num_contracts):
        payload = {
            'contract_id': contract_id,
            "num_contracts" : num_contracts
        }
        data = TemplateAPI.request_post(
            'settle', payload)
        return data


    def export(contract_id):
        payload = {
            'contract_id': contract_id
        }
        data = TemplateAPI.request_post(
            'export_option', payload)
        return data


    def remove(contract_id):
        payload = {
            'contract_id': contract_id
        }
        data = TemplateAPI.request_post(
            'remove_option', payload)
        return data


    def import_option(payload):
        data = TemplateAPI.request_post(
            'import_option', payload)
        return data


    def request_get(url, params={}):
        api_url = current_app.config['API_URL']
        token_read = current_app.config['READ_TOKEN']
        headers_read = {'content-type': 'application/json', 'Authorization': f'{token_read}'}
        url = f'{api_url}/{url}'
        response = requests.get(url, params=params, headers=headers_read)
        if response.status_code == 403 or response.status_code == 404 or response.status_code == 400:
            raise PermissionError
        data = json.loads(response.text)
        return data


    def request_post(url, payload):
        api_url = current_app.config['API_URL']
        token_write = current_app.config['WRITE_TOKEN']
        headers_write = {'content-type': 'application/json', 'Authorization': f'{token_write}'}
        url = f'{api_url}/{url}'
        response = requests.post(
            url, data=json.dumps(payload), headers=headers_write)
        if response.status_code == 403 or response.status_code == 404 or response.status_code == 400:
            message = 'An error occured.'
            if response.text:
                data = json.loads(response.text)
                for value in data.values():
                    if isinstance(value, list):
                        message = message + f' {value[0]}.'
                    else:
                        message = message + f' {value}.'
            raise ValueError(message)
        data = json.loads(response.text)
        return data
