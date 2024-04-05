from odoo import models, fields, api
import requests


class CryptoEmpirePortfolioLines(models.Model):
    _name = "crypto.empire.portfolio.lines"
    _description = "Crypto Portfolio Lines"
    _order = "total_price desc"


    name = fields.Char("Name")
    price = fields.Float("Price", readonly=True, digits=(16, 4))
    portfolio_id = fields.Many2one('crypto.empire.portfolio', string='Portfolio')
    quantity = fields.Float("Quantity", digits=(16, 4))
    total_price = fields.Float("Total Price", readonly=True, digits=(16, 4))

    @api.constrains("name", 'quantity')
    def _onchange_name(self):
        for record in self:
            if record.name:
                try:
                    url = "https://crypto-market-prices.p.rapidapi.com/tokens/" + record.name
                    querystring = {"base": "USDT"}

                    headers = {
                        "X-RapidAPI-Key": "b89eda7d12mshc56e0632676b083p1c083ajsn3ea19170320c",
                        "X-RapidAPI-Host": "crypto-market-prices.p.rapidapi.com"
                    }
                    response = requests.get(url, headers=headers, params=querystring)
                    record.price = response.json()['data']['tokens'][0]['price']
                    record.total_price = record.price * record.quantity
                except:
                    pass

