from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
from astrbot.api import logger


class AvatarOnlyPlugin(Star):
    """这是一个只用于修改 NapCat QQ Bot 自身头像的 AstrBot 插件 仅面向 NapCat/OneBot v11"""

    def __init__(self, context: Context):
        super().__init__(context)

    async def _find_image(self, event: AstrMessageEvent):
        """查找当前消息或引用消息中的第一张图片 并返回可供 NapCat 使用的地址"""
        raw = getattr(event.message_obj, "raw_message", None)

        # 1. 当前消息直接带图片
        if isinstance(raw, dict):
            for seg in raw.get("message", []) or []:
                if isinstance(seg, dict) and seg.get("type") == "image":
                    data = seg.get("data", {}) or {}
                    url = data.get("url")
                    if url:
                        return url
                    file = data.get("file")
                    if file:
                        try:
                            result = await event.bot.call_action(
                                "get_image",
                                file=file,
                            )
                            if isinstance(result, dict):
                                result = result.get("data", result)
                                return (
                                    result.get("url")
                                    or result.get("file")
                                    or file
                                )
                        except Exception:
                            return file

            # 2. 回复一条图片消息
            for seg in raw.get("message", []) or []:
                if isinstance(seg, dict) and seg.get("type") == "reply":
                    reply_id = seg.get("data", {}).get("id")
                    if reply_id:
                        try:
                            msg = await event.bot.call_action(
                                "get_msg",
                                message_id=reply_id,
                            )
                            if isinstance(msg, dict):
                                for rseg in msg.get("message", []) or []:
                                    if (
                                        isinstance(rseg, dict)
                                        and rseg.get("type") == "image"
                                    ):
                                        data = rseg.get("data", {}) or {}
                                        url = data.get("url")
                                        if url:
                                            return url
                                        file = data.get("file")
                                        if file:
                                            try:
                                                result = await event.bot.call_action(
                                                    "get_image",
                                                    file=file,
                                                )
                                                if isinstance(result, dict):
                                                    result = result.get(
                                                        "data", result
                                                    )
                                                    return (
                                                        result.get("url")
                                                        or result.get("file")
                                                        or file
                                                    )
                                            except Exception:
                                                return file
                        except Exception as exc:
                            logger.warning("获取引用图片失败: %s", exc)

        return None

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("换头像", alias={"set_avatar", "头像"})
    async def set_avatar(self, event: AstrMessageEvent, image_url: str = ""):
        """修改Bot自己的QQ头像 可直接发送图片 或引用图片后发送 /换头像"""
        image_url = (image_url or "").strip()

        if not image_url:
            image_url = await self._find_image(event)

        if not image_url:
            yield event.plain_result(
                "请发送 /换头像 + 图片 或引用一张图片发送 /换头像"
            )
            return

        try:
            await event.bot.call_action(
                "set_qq_avatar",
                file=image_url,
            )
            yield event.plain_result("头像已更换哦")
        except Exception as exc:
            logger.error("设置 QQ 头像失败: %s", exc)
            yield event.plain_result(
                "头像更换失败 请确认当前QQ端是NapCat并检查图片是否有效"
            )
