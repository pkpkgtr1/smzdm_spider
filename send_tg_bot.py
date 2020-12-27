import telegram

chat_id = "@pkpkgtr1"  # 频道地址
token = "1456525222:AAFF-oIy_GEsYk8WxDSuvEfj6zde12hMxW0"  # 机器人 TOKEN
bot = telegram.Bot(token=token)



def send_tg_bot(lx,sp_name,sp_jg,sp_sj,sp_url,sp_jpg):
    text =f'''
    <b>{lx}</b>
    <b>商品名称：{sp_name}</b>
    <em>售价: {sp_jg}</em>
    <em>活动商家：{sp_sj}</em>
    <a href="{sp_url}">商品地址</a>
    '''

    bot.send_photo(
        chat_id=chat_id,
        photo=sp_jpg,
        caption=text,
        parse_mode=telegram.ParseMode.HTML
    )
