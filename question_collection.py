### crawls the question from zhihu.com by using the module zhihu_oauth

from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedCaptchaException

client = ZhihuClient()
try:
    client.login(zhihu_account, zhihu_password)
except NeedCaptchaException:
   ### here we need to save the CAPTCHA and relogin
    with open('a.gif', 'wb') as f:
        f.write(client.get_captcha())
    captcha = input('please input captcha:')
    client.login(zhihu_account, zhihu_password, captcha)
    
### the id of zhihu.com is not always continuous, we have to traverse all the id
q = []
for id in range(281736391,311982210):
    question = client.question(id)
    try:
        q.append(question.title)
    except zhihu_oauth.exception.GetDataErrorException:
        continue

### I totally crawled 14W+ questions from zhihu.com
