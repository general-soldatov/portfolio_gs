from typing import Union, Dict, Any 

from aiogram import html
from aiogram.filters import BaseFilter
from aiogram.types import Message

class HasUsernamesFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        entities = message.entities or []

        found_usernames = [
            item.extract_from(message.text) for item in entities
            if item.type == 'mention'
        ]

        if len(found_usernames) > 0:
            return {'usernames': found_usernames}
        
        return False
    
class LoginParser(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        data = {
        'url': '<N/A>',
        'email': '<N/A>',
        'code': '<N/A>'
        }

        entities = message.entities or []
        for item in entities:
            if item.type in data.keys():
                data[item.type] = item.extract_from(message.text)

        if data['url'] != '<N/A>':
            return {'login': [html.quote(data['url']), html.quote(data['email']), html.quote(data['code'])]}
        
        return False
    
