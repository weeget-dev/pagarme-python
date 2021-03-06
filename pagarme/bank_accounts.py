# encoding: utf-8
import json
import requests

from .resource import AbstractResource
from .settings import BASE_URL


class BankAccount(AbstractResource):
    BASE_URL = BASE_URL + 'bank_accounts'

    def __init__(
            self,
            api_key=None,
            _id=None,
            count=None,
            page=None,
            bank_code=None,
            agencia=None,
            agencia_dv=None,
            conta=None,
            conta_dv=None,
            document_type=None,
            document_number=None,
            legal_name=None,
            charge_transfer_fees=None,
            date_created=None):

        if bank_code and agencia and conta:
            self.data = {
                'id': _id,
                'bank_code': bank_code,
                'agencia': agencia,
                'agencia_dv': agencia_dv,
                'conta': conta,
                'conta_dv': conta_dv,
                'document_type': document_type,
                'document_number': document_number,
                'legal_name': legal_name,
                'charge_transfer_fees': charge_transfer_fees,
                'date_created': date_created                               
            }
        else:
            self.data = {}
            if _id:
                self.data['id'] = _id
            else:
                if count:
                    self.data['count'] = count
                if page:
                    self.data['page'] = page
        self.data['api_key'] = api_key


    def handle_response(self, data):
        self._id = data['id']
        self.bank_code = data['bank_code']
        self.agencia = data['agencia']
        self.agencia_dv = data['agencia_dv']
        self.conta = data['conta']
        self.conta_dv = data['conta_dv']
        self.document_type = data['document_type']
        self.document_number = data['document_number']
        self.legal_name = data['legal_name']
        self.charge_transfer_fees = data['charge_transfer_fees']
        self.date_created = data['date_created']

    def get_data(self):
        return self.data

    def find_by_id(self):
        bank_id = self.data['id']    
        url = self.BASE_URL + '/' + str(bank_id)   
        pagarme_response = requests.get(url, params={'api_key': self.data['api_key']})
        if pagarme_response.status_code == 200:
            try:
                self.handle_response(json.loads(pagarme_response.content))
            except:
                self.handle_response(json.loads(pagarme_response.content.decode(encoding='UTF-8')))
        else:
            try:
                self.error(pagarme_response.content)
            except:
                self.error(json.loads(pagarme_response.content.decode(encoding='UTF-8')))
            
    def find_all(self):
        url = self.BASE_URL + '/'      
        pagarme_response = requests.get(url, params={'api_key': self.data['api_key']})
            
        if pagarme_response.status_code == 200:
            try:
                list_banks = json.loads(pagarme_response.content)
            except:
                list_banks = json.loads(pagarme_response.content.decode(encoding='UTF-8')) 
            
            return list_banks
        else:
            try:
                self.error(pagarme_response.content)
            except:
                self.error(json.loads(pagarme_response.content.decode(encoding='UTF-8')))
