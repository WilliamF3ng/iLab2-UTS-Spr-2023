# pip install googletrans==4.0.0-rc1
import googletrans
from googletrans import Translator
trans = Translator()

print(trans.translate("Today the weather is hot", dest = 'zh-cn'))

print(googletrans.LANGCODES)