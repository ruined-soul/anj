"""Anjani custom types"""
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

from abc import abstractmethod, abstractproperty
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Callable,
    Coroutine,
    Iterable,
    List,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
    Union,
)

from pyrogram.filters import Filter
from pyrogram.types import ChatMember, ForceReply, InlineKeyboardMarkup
from pyrogram.types import Message as M
from pyrogram.types import MessageEntity, ReplyKeyboardMarkup, ReplyKeyboardRemove
from pyrogram.types.messages_and_media.message import Str

if TYPE_CHECKING:
    from anjani.core import Anjani

Bot = TypeVar("Bot", bound="Anjani", covariant=True)
ChatId = TypeVar("ChatId", int, None, covariant=True)
TextName = TypeVar("TextName", bound=str, covariant=True)
NoFormat = TypeVar("NoFormat", bound=bool, covariant=True)
TypeData = TypeVar("TypeData", covariant=True)


class CustomFilter(Filter):  # skipcq: PYL-W0223
    anjani: "Anjani"
    include_bot: bool


class Message(M):
    command: List[str]
    text: Str

    @abstractmethod
    async def edit(
        self,
        text: str,
        *,
        parse_mode: Any = object,
        entities: List[MessageEntity] = [],
        disable_web_page_preview: bool = False,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> "Message":  # skipcq: PYL-W0221
        ...

    @abstractmethod
    async def edit_text(
        self,
        text: str,
        *,
        parse_mode: Any = object,
        entities: List[MessageEntity] = [],
        disable_web_page_preview: bool = False,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
    ) -> "Message":  # skipcq: PYL-W0221
        ...

    @abstractmethod
    async def reply(
        self,
        text: str,
        *,
        quote: bool = False,
        parse_mode: Any = object,
        entities: List[MessageEntity] = [],
        disable_web_page_preview: bool = False,
        disable_notification: bool = False,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, None
        ] = None,
    ) -> "Message":  # skipcq: PYL-W0221
        ...

    @abstractmethod
    async def reply_text(
        self,
        text: str,
        *,
        quote: bool = False,
        parse_mode: Any = object,
        entities: List[MessageEntity] = [],
        disable_web_page_preview: bool = False,
        disable_notification: bool = False,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, None
        ] = None,
    ) -> "Message":  # skipcq: PYL-W0221
        ...

    @abstractmethod
    async def reply_animation(
        self,
        animation: Union[IO[bytes], BinaryIO, str],
        *,
        quote: bool = False,
        caption: str = "",
        parse_mode: Any = object,
        caption_entities: List[MessageEntity] = [],
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: Optional[str] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, None
        ] = None,
        progress: Optional[Callable[..., Union[Coroutine[Any, Any, None], None]]] = None,
        progress_args: Tuple[Any, ...] = (),
    ) -> "Message":  # skipcq: PYL-W0221
        ...

    @abstractmethod
    async def reply_audio(
        self,
        audio: Union[IO[bytes], BinaryIO, str],
        *,
        quote: bool = False,
        caption: str = "",
        parse_mode: Any = object,
        caption_entities: List[MessageEntity] = [],
        duration: int = 0,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumb: Optional[str] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, None
        ] = None,
        progress: Optional[Callable[..., Union[Coroutine[Any, Any, None], None]]] = None,
        progress_args: Tuple[Any, ...] = (),
    ) -> "Message":  # skipcq: PYL-W0221
        ...

    @abstractmethod
    async def reply_document(
        self,
        document: Union[IO[bytes], BinaryIO, str],
        *,
        quote: bool = False,
        thumb: Optional[str] = None,
        caption: str = "",
        parse_mode: Any = object,
        caption_entities: List[MessageEntity] = [],
        disable_notification: bool = False,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, None
        ] = None,
        progress: Optional[Callable[..., Union[Coroutine[Any, Any, None], None]]] = None,
        progress_args: Tuple[Any, ...] = (),
    ) -> "Message":  # skipcq: PYL-W0221
        ...

    @abstractmethod
    async def reply_photo(
        self,
        photo: Union[IO[bytes], BinaryIO, str],
        *,
        quote: bool = False,
        caption: str = "",
        parse_mode: Any = object,
        caption_entities: List[MessageEntity] = [],
        ttl_seconds: Optional[int] = None,
        disable_notification: bool = False,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, None
        ] = None,
        progress: Optional[Callable[..., Union[Coroutine[Any, Any, None], None]]] = None,
        progress_args: Tuple[Any, ...] = (),
    ) -> "Message":  # skipcq: PYL-W0221
        ...

    @abstractmethod
    async def reply_video(
        self,
        video: Union[IO[bytes], BinaryIO, str],
        *,
        quote: bool = False,
        caption: str = "",
        parse_mode: Any = object,
        caption_entities: List[MessageEntity] = [],
        ttl_seconds: Optional[int] = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: Optional[str] = None,
        supports_streaming: bool = True,
        disable_notification: bool = False,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Union[
            InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, None
        ] = None,
        progress: Optional[Callable[..., Union[Coroutine[Any, Any, None], None]]] = None,
        progress_args: Tuple[Any, ...] = (),
    ) -> "Message":  # skipcq: PYL-W0221
        ...


class MemberInformation:
    def __init__(self, delegate: ChatMember) -> None:
        self.status = delegate.status
        self.user = delegate.user
        self.chat = delegate.chat
        self.custom_title = delegate.custom_title
        self.until_date = delegate.until_date
        self.joined_date = delegate.joined_date
        self.invited_by = delegate.invited_by
        self.promoted_by = delegate.promoted_by
        self.restricted_by = delegate.restricted_by
        self.is_member = delegate.is_member
        self.can_be_edited = delegate.can_be_edited
        self.permissions = delegate.permissions
        self.privileges = delegate.privileges


class NDArray(Protocol[TypeData]):
    @abstractmethod
    def __getitem__(self, key: int) -> Any:
        raise NotImplementedError

    @abstractproperty
    def size(self) -> int:
        raise NotImplementedError


class Pipeline(Protocol):
    @abstractmethod
    def predict(self, X: Iterable[Any], **predict_params: Any) -> NDArray[Any]:
        raise NotImplementedError

    @abstractmethod
    def predict_proba(self, X: Iterable[Any]) -> NDArray[Any]:
        raise NotImplementedError
