import asyncio
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Tuple

import pyrogram
from async_lru import alru_cache
from pyrogram.filters import Filter
from pyrogram.types import ChatMember, Message

if TYPE_CHECKING:
    from .core import Anjani


class CustomFilter(Filter):
    anjani: "Anjani"
    include_bot: bool

FilterFunc = Callable[[CustomFilter, pyrogram.Client, Message],
                      Coroutine[Any, Any, bool]]


def create(func: FilterFunc, name: str = None, **kwargs) -> CustomFilter:
    return type(
        name or func.__name__ or "CustomAnjaniFilter",
        (CustomFilter,),
        {"__call__": func, **kwargs}
    )()


# { staff_only
def _staff_only(include_bot: bool = True) -> CustomFilter:

    async def func(flt: CustomFilter, _: pyrogram.Client, message: Message) -> bool:
        user = message.from_user
        return bool(user.id in flt.anjani.staff)

    return create(func, "staff_only", include_bot=include_bot)

staff_only = _staff_only()
# }


# { permission
@alru_cache(maxsize=128)
async def fetch_permissions(client: pyrogram.Client,
                            chat: int, user: int) -> Tuple[ChatMember, ChatMember]:
    bot, member = await asyncio.gather(client.get_chat_member(chat, "me"),
                                       client.get_chat_member(chat, user))
    return bot, member

async def _can_delete(_: Filter, client: pyrogram.Client, message: Message) -> bool:
    if message.chat.type == "private":
        return False

    bot, member = await fetch_permissions(client, message.chat.id,
                                          message.from_user.id)  # type: ignore
    return bool(bot.can_delete_messages and member.can_delete_messages)


async def _can_change_info(_: Filter, client: pyrogram.Client, message: Message) -> bool:
    if message.chat.type == "private":
        return False

    bot, member = await fetch_permissions(client, message.chat.id,
                                          message.from_user.id)  # type: ignore
    return bool(bot.can_change_info and member.can_change_info)


async def _can_invite(_: Filter, client: pyrogram.Client, message: Message) -> bool:
    if message.chat.type == "private":
        return False

    bot, member = await fetch_permissions(client, message.chat.id,
                                          message.from_user.id)  # type: ignore
    return bool(bot.can_invite_users and member.can_invite_users)


async def _can_pin(_: Filter, client: pyrogram.Client, message: Message) -> bool:
    if message.chat.type == "private":
        return False

    bot, member = await fetch_permissions(client, message.chat.id,
                                          message.from_user.id)  # type: ignore
    return bool(bot.can_pin_messages and member.can_pin_messages)


async def _can_promote(_: Filter, client: pyrogram.Client, message: Message) -> bool:
    if message.chat.type == "private":
        return False

    bot, member = await fetch_permissions(client, message.chat.id,
                                          message.from_user.id)  # type: ignore
    return bool(bot.can_promote_members and member.can_promote_members)


async def _can_restrict(_: Filter, client: pyrogram.Client, message: Message) -> bool:
    if message.chat.type == "private":
        return False

    bot, member = await fetch_permissions(client, message.chat.id,
                                          message.from_user.id)  # type: ignore
    return bool(bot.can_restrict_members and member.can_restrict_members)


can_delete = pyrogram.filters.create(_can_delete, "can_delete")
can_change_info = pyrogram.filters.create(_can_change_info, "can_change_info")
can_invite = pyrogram.filters.create(_can_invite, "can_invite")
can_pin = pyrogram.filters.create(_can_pin, "can_pin")
can_promote = pyrogram.filters.create(_can_promote, "can_promote")
can_restrict = pyrogram.filters.create(_can_restrict, "can_restrict")
# }