""" Message purging plugin. """
# Copyright (C) 2020 - 2022  UserbotIndo Team, <https://github.com/userbotindo.git>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
from typing import Any, ClassVar, List, MutableMapping, Optional, Tuple

from pyrogram.types import Message

from anjani import command, filters, plugin, util


class Filters(plugin.Plugin):
    name: ClassVar[str] = "Filters"
    helpable: ClassVar[bool] = True

    db: util.db.AsyncCollection
    trigger: MutableMapping[int, List[str]] = {}

    async def on_load(self) -> None:
        self.db = self.bot.db.get_collection("FILTERS")

    async def on_start(self, _: int) -> None:
        async for chat in self.db.find({}):
            self.trigger[chat["chat_id"]] = list(chat["trigger"].keys())

    async def on_plugin_backup(self, chat_id: int) -> MutableMapping[str, Any]:
        data = await self.db.find_one({"chat_id": chat_id}, {"_id": False})
        return {self.name: data} if data else {}

    async def on_plugin_restore(self, chat_id: int, data: MutableMapping[str, Any]) -> None:
        await self.db.update_one({"chat_id": chat_id}, {"$set": {data[self.name]}}, upsert=True)

    async def on_message(self, message: Message) -> None:
        chat = message.chat
        text = message.text or message.caption

        if not (text or chat):
            return

        chat_trigger = self.trigger.get(chat.id, [])
        if not chat_trigger:
            return

        await self.reply_filter(message, chat_trigger, text)

    async def reply_filter(self, message: Message, trigger: List[str], text: str):
        for i in trigger:
            pattern = r"( |^|[^\w])" + re.escape(i) + r"( |$|[^\w])"
            if re.search(pattern, text, flags=re.IGNORECASE):
                filt = await self.get_filter(message.chat.id, i)
                if not filt:
                    return

                await message.reply_text(filt)
                break

    async def get_filter(self, chat_id: int, keyword: str) -> Optional[str]:
        data = await self.db.find_one({"chat_id": chat_id})
        return data["trigger"][keyword] if data else None

    async def save_filter(self, chat_id: int, keyword: str, content: str):
        await self.db.update_one(
            {"chat_id": chat_id}, {"$set": {f"trigger.{keyword}": content}}, upsert=True
        )

        if self.trigger.get(chat_id):
            self.trigger[chat_id].append(keyword)
        else:
            self.trigger[chat_id] = [keyword]

    async def del_filter(self, chat_id: int, keyword: str) -> Tuple[bool, str]:
        filt = self.trigger.get(chat_id)
        if not filt:
            return False, "This chat has no filters, nothing to remove"
        if keyword not in filt:
            return False, f"No filters named {keyword} on this chat."

        await self.db.update_one(
            {"chat_id": chat_id},
            {"$unset": {f"trigger.{keyword}": ""}},
        )
        self.trigger[chat_id].remove(keyword)
        return True, ""

    @command.filters(filters.admin_only)
    async def cmd_filter(self, ctx: command.Context, trigger: str, *, text: str) -> None:
        if not trigger or not text:
            await ctx.respond("Usage: `/filters <trigger> <text>`")
            return

        await self.save_filter(ctx.chat.id, trigger, text)
        await ctx.respond(f"Successfully added `{trigger}` as filter.")

    @command.filters(filters.admin_only)
    async def cmd_stop(self, ctx: command.Context, trigger: str):
        if not trigger:
            await ctx.respond("Usage: `/stop <trigger>`")
            return

        deleted, out = await self.del_filter(ctx.chat.id, trigger)
        if not deleted:
            await ctx.respond(out)
        await ctx.respond(f"Successfully removed `{trigger}` as filter.")

    @command.filters(filters.admin_only)
    async def cmd_rmallfilter(self, ctx: command.Context) -> str:
        chat_id = ctx.chat.id
        triggers = self.trigger.pop(chat_id, None)
        if not triggers:
            return "This chat has no filters, nothing to remove"
        await self.db.delete_one({"chat_id": chat_id})
        return f"Successfully removed {len(triggers)} filters."

    @command.filters(filters.admin_only)
    async def cmd_filters(self, ctx: command.Context) -> str:
        data = self.trigger.get(ctx.chat.id)
        if not data:
            return "No filters found."

        output = f"Filters in **{ctx.chat.title}**:"
        output += "\n".join([f"`{i}`" for i in data])
        return output
