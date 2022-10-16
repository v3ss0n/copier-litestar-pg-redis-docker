from typing import TYPE_CHECKING
from unittest.mock import AsyncMock

from app.domain import authors
from app.lib import email

if TYPE_CHECKING:
    from pytest import MonkeyPatch


async def test_author_domain_send_email(monkeypatch: "MonkeyPatch") -> None:
    email_client_mock = AsyncMock()

    monkeypatch.setattr(email, "client", email_client_mock)
    await authors.Service.send_author_created_email("test message content")
    email_client_mock.__aenter__.assert_called_once()
    email_client_mock.send_message.assert_called_once()
    email_client_mock.__aexit__.assert_called_once_with(None, None, None)
    send_message_call = email_client_mock.send_message.mock_calls[0]
    sent_email = send_message_call.args[0]
    assert (
        str(sent_email).strip()
        == """
From: root@localhost
To: someone@somewhere.com
Subject: New Author Added
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 7bit
MIME-Version: 1.0

test message content
    """.strip()
    )
