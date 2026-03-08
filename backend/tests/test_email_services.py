"""Tests para app/services/email_services.py"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import BackgroundTasks


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _make_background_tasks() -> BackgroundTasks:
    bt = MagicMock(spec=BackgroundTasks)
    bt.add_task = MagicMock()
    return bt


# ──────────────────────────────────────────────
# _render_template
# ──────────────────────────────────────────────

class TestRenderTemplate:
    def test_renders_variables(self, tmp_path, monkeypatch):
        """Sustituye {{ key }} correctamente."""
        from app.services import email_services as svc

        # Apuntamos TEMPLATE_DIR a un directorio temporal
        monkeypatch.setattr(svc, "TEMPLATE_DIR", tmp_path)
        tpl = tmp_path / "test.html"
        tpl.write_text("<p>{{ nombre }} - {{ year }}</p>", encoding="utf-8")

        result = svc._render_template("test.html", {"nombre": "Juan", "year": "2025"})
        assert result == "<p>Juan - 2025</p>"

    def test_missing_variable_left_as_placeholder(self, tmp_path, monkeypatch):
        """Si falta una variable, el placeholder queda sin reemplazar."""
        from app.services import email_services as svc

        monkeypatch.setattr(svc, "TEMPLATE_DIR", tmp_path)
        tpl = tmp_path / "test.html"
        tpl.write_text("<p>{{ nombre }}</p>", encoding="utf-8")

        result = svc._render_template("test.html", {})
        assert "{{ nombre }}" in result


# ──────────────────────────────────────────────
# send_verification_email
# ──────────────────────────────────────────────

class TestSendVerificationEmail:
    @pytest.mark.asyncio
    async def test_sends_with_background_tasks(self, tmp_path, monkeypatch):
        """Con BackgroundTasks, agrega la tarea en lugar de enviar directo."""
        from app.services import email_services as svc

        monkeypatch.setattr(svc, "TEMPLATE_DIR", tmp_path)
        (tmp_path / "verification.html").write_text(
            "<a href='{{ verification_url }}'>{{ year }}</a>", encoding="utf-8"
        )

        mock_fm = MagicMock()
        mock_fm.send_message = AsyncMock()
        with patch("app.services.email_services.FastMail", return_value=mock_fm):
            bt = _make_background_tasks()
            await svc.send_verification_email("user@test.com", "tok123", background_tasks=bt)

        bt.add_task.assert_called_once()
        mock_fm.send_message.assert_not_called()

    @pytest.mark.asyncio
    async def test_sends_directly_without_background_tasks(self, tmp_path, monkeypatch):
        """Sin BackgroundTasks, llama send_message directamente."""
        from app.services import email_services as svc

        monkeypatch.setattr(svc, "TEMPLATE_DIR", tmp_path)
        (tmp_path / "verification.html").write_text(
            "<a href='{{ verification_url }}'>{{ year }}</a>", encoding="utf-8"
        )

        mock_fm = MagicMock()
        mock_fm.send_message = AsyncMock()
        with patch("app.services.email_services.FastMail", return_value=mock_fm):
            await svc.send_verification_email("user@test.com", "tok123")

        mock_fm.send_message.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_verification_url_contains_token(self, tmp_path, monkeypatch):
        """La URL de verificación incluye el token y BASE_URL."""
        from app.services import email_services as svc

        monkeypatch.setattr(svc, "TEMPLATE_DIR", tmp_path)
        monkeypatch.setattr(svc, "BASE_URL", "http://example.com")
        (tmp_path / "verification.html").write_text(
            "{{ verification_url }}", encoding="utf-8"
        )

        captured = {}

        async def fake_send(msg):
            captured["body"] = msg.body

        mock_fm = MagicMock()
        mock_fm.send_message = fake_send
        with patch("app.services.email_services.FastMail", return_value=mock_fm):
            await svc.send_verification_email("u@t.com", "MYTOKEN")

        assert "MYTOKEN" in captured["body"]
        assert "http://example.com" in captured["body"]


# ──────────────────────────────────────────────
# send_new_password_email
# ──────────────────────────────────────────────

class TestSendNewPasswordEmail:
    @pytest.mark.asyncio
    async def test_sends_with_background_tasks(self, tmp_path, monkeypatch):
        from app.services import email_services as svc

        monkeypatch.setattr(svc, "TEMPLATE_DIR", tmp_path)
        (tmp_path / "reset_password.html").write_text(
            "<a href='{{ reset_url }}'>{{ year }}</a>", encoding="utf-8"
        )

        mock_fm = MagicMock()
        mock_fm.send_message = AsyncMock()
        with patch("app.services.email_services.FastMail", return_value=mock_fm):
            bt = _make_background_tasks()
            await svc.send_new_password_email("user@test.com", "resettok", background_tasks=bt)

        bt.add_task.assert_called_once()
        mock_fm.send_message.assert_not_called()

    @pytest.mark.asyncio
    async def test_reset_url_contains_token(self, tmp_path, monkeypatch):
        from app.services import email_services as svc

        monkeypatch.setattr(svc, "TEMPLATE_DIR", tmp_path)
        monkeypatch.setattr(svc, "BASE_URL", "http://myapp.io")
        (tmp_path / "reset_password.html").write_text("{{ reset_url }}", encoding="utf-8")

        captured = {}

        async def fake_send(msg):
            captured["body"] = msg.body

        mock_fm = MagicMock()
        mock_fm.send_message = fake_send
        with patch("app.services.email_services.FastMail", return_value=mock_fm):
            await svc.send_new_password_email("u@t.com", "RESETTOKEN")

        assert "RESETTOKEN" in captured["body"]
        assert "http://myapp.io" in captured["body"]


# ──────────────────────────────────────────────
# send_receipt_email
# ──────────────────────────────────────────────

class TestSendReceiptEmail:
    @pytest.mark.asyncio
    async def test_sends_with_background_tasks(self, tmp_path, monkeypatch):
        from app.services import email_services as svc

        monkeypatch.setattr(svc, "TEMPLATE_DIR", tmp_path)
        (tmp_path / "receipt.html").write_text(
            "{{ nombre }} {{ referencia }} {{ fecha }} {{ monto }} {{ lote }} {{ year }}",
            encoding="utf-8",
        )

        mock_fm = MagicMock()
        mock_fm.send_message = AsyncMock()
        with patch("app.services.email_services.FastMail", return_value=mock_fm):
            bt = _make_background_tasks()
            await svc.send_receipt_email(
                "user@test.com",
                b"%PDF-fake",
                bt,
                nombre="Ana",
                referencia="REF001",
                fecha="01/01/2025",
                monto="100000",
                lote="L-01",
            )

        bt.add_task.assert_called_once()
        mock_fm.send_message.assert_not_called()

    @pytest.mark.asyncio
    async def test_receipt_body_contains_fields(self, tmp_path, monkeypatch):
        from app.services import email_services as svc

        monkeypatch.setattr(svc, "TEMPLATE_DIR", tmp_path)
        (tmp_path / "receipt.html").write_text(
            "{{ nombre }}|{{ referencia }}|{{ monto }}|{{ lote }}", encoding="utf-8"
        )

        captured = {}

        async def fake_send(msg):
            captured["body"] = msg.body

        mock_fm = MagicMock()
        mock_fm.send_message = fake_send
        with patch("app.services.email_services.FastMail", return_value=mock_fm):
            await svc.send_receipt_email(
                "u@t.com",
                b"%PDF",
                None,
                nombre="Carlos",
                referencia="R-99",
                monto="500",
                lote="L-5",
            )

        assert "Carlos" in captured["body"]
        assert "R-99" in captured["body"]
        assert "500" in captured["body"]
        assert "L-5" in captured["body"]
