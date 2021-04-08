from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


receiver = ['zhang@gmail.com', '1@163.com']

sender_user_name = '188'
sender_email = ''
pwd = ''
host_server = 'smtp.qq.com'


def send_mail(mail_title='', mail_content=''):
    # ssl登录
    smtp = SMTP_SSL(host_server)
    # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(0)
    smtp.ehlo(host_server)
    smtp.login(sender_user_name, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_email
    msg["To"] = ','.join(receiver)
    smtp.sendmail(sender_email, receiver, msg.as_string())
    smtp.quit()


def send_macy_instock_mail(product_name, product_url):
    print('send email')
    in_stock_mail_title = '补货通知: Macy {}'.format(product_name)
    in_stock_mail_content = 'Macy网站的{}已经补货,网站链接:\n{}'.format(product_name, product_url)
    send_mail(mail_title=in_stock_mail_title, mail_content=in_stock_mail_content)


def send_nd_instock_mail(product_name, product_url):
    print('send email')
    in_stock_mail_title = '补货通知: Macy {}'.format(product_name)
    in_stock_mail_content = 'NordStorm网站的{}已经补货,网站链接:\n{}'.format(product_name, product_url)
    send_mail(mail_title=in_stock_mail_title, mail_content=in_stock_mail_content)


if __name__ == '__main__':
    # in_stock_mail_title = '补货通知: <网站名> <商品名>'
    # test_mail_content = 'test_content'
    #
    # send_mail(mail_title=in_stock_mail_title,
    #           mail_content=test_mail_content)
    send_macy_instock_mail('沐浴露', 'www.baidu.com')
