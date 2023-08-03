# -*- coding: utf-8 -*-

import os
from gpt4all import GPT4All
import requests
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import json
 
class Channel(models.Model):
    _inherit = 'mail.channel'

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        rdata = super(Channel, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
        chatgpt_channel_id = self.env.ref('gpt_4_all.channel_chatgpt') # channel id
        user_chatgpt = self.env.ref("gpt_4_all.user_chatgpt") # memanggil user ChatGpt
        partner_chatgpt = self.env.ref("gpt_4_all.partner_chatgpt") # memanggil res.partner ChatGpt
        author_id = msg_vals.get('author_id') # user yang sedang login
        chatgpt_name = str(partner_chatgpt.name or '') + ', ' # nama partner chatgpt
        prompt = msg_vals.get('body')  #message yang dikirimkan oleh user
        if not prompt:
            return rdata
        Partner = self.env['res.partner']
        partner_name = ''
        if author_id:
            partner_id = Partner.browse(author_id)
            if partner_id:
                partner_name = partner_id.name
        if author_id != partner_chatgpt.id and chatgpt_name in msg_vals.get('record_name', '') or 'ChatGPT,' in msg_vals.get('record_name', '') and self.channel_type == 'chat':
            try:
                res = self._generate_response(prompt=prompt)
                self.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
            except Exception as e:
                raise UserError(_(e))

        elif author_id != partner_chatgpt.id and msg_vals.get('model', '') == 'mail.channel' and msg_vals.get('res_id', 0) == chatgpt_channel_id.id:
            try:
                res = self._generate_response(prompt=prompt)

                chatgpt_channel_id.with_user(user_chatgpt).message_post(body=res, message_type='comment', subtype_xmlid='mail.mt_comment')
            except Exception as e:

                raise UserError(_(e))

        return rdata
    
    def _generate_response(self, prompt):
        models_path = os.path.dirname(os.path.realpath(__file__)) + '/../static/ai_models/' 
        model_name = 'orca-mini-3b.ggmlv3.q4_0.bin'

        try:
            model = GPT4All(models_path+model_name)

            with model.chat_session():
                response = model.generate(prompt=prompt, top_k=1, max_tokens=3000, top_p=1)
                print("Answer : ", response)
                session = model.current_chat_session
                answer = session[-1]["content"]
                print("raw session : ", session)
                print('answer :',answer)
                print("debug : ", model.chat_session())
                return answer
        except Exception as e:
            print("error message :", e)
            return e