from odoo import models, fields, api
import requests


class CryptoEmpirePortfolio(models.Model):
    _name = "crypto.empire.portfolio"

    name = fields.Char("Name")
    crypto_empire_portfolio_lines_ids = fields.One2many(
        'crypto.empire.portfolio.lines',
        'portfolio_id',
        string='Crypto Lines'
    )
    portfolio_value = fields.Float(compute='_compute_portfolio_value')

    @api.depends('crypto_empire_portfolio_lines_ids')
    def _compute_portfolio_value(self):
        for record in self:
            sum_of_lines = 0
            for line in record.crypto_empire_portfolio_lines_ids:
                sum_of_lines += line.total_price
            self.portfolio_value = sum_of_lines

    def refresh_coins(self):
        for record in self:
            for line in record.crypto_empire_portfolio_lines_ids:
                if line.name:
                    try:
                        url = "https://crypto-market-prices.p.rapidapi.com/tokens/" + line.name
                        querystring = {"base": "USDT"}

                        headers = {
                            "X-RapidAPI-Key": "b89eda7d12mshc56e0632676b083p1c083ajsn3ea19170320c",
                            "X-RapidAPI-Host": "crypto-market-prices.p.rapidapi.com"
                        }
                        response = requests.get(url, headers=headers, params=querystring)
                        line.price = response.json()['data']['tokens'][0]['price']
                        line.total_price = line.price * line.quantity
                    except:
                        pass
