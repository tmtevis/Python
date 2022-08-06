from lxml import html
import requests

page = requests.get('https://allagentreports.com/Forms/BettorWagersByPartner.aspx')
tree = html.fromstring(page.content)

buyers = tree.xpath('//div[@id="ctl00_ContentSection_BettorWagers_ReportData"]')
print('Bettors: ', buyers)