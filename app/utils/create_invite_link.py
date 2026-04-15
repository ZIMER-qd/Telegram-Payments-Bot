from aiogram import Bot


async def create_link(bot: Bot):
    invite = await bot.create_chat_invite_link(
        chat_id=-1003835688732,
        member_limit=1
    )
    return invite.invite_link