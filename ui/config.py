from PyQt5.QtCore import QObject, pyqtSignal

class ConfigManager(QObject):
    """
    资源管理器
    功能：存储全局头像路径，提供修改接口
    """
    _instance = None
    avatar_changed= pyqtSignal(str, str)

    def __init__(self):
        if not ConfigManager._instance:
            super().__init__()
            self._avatars = {
                "me": "./fig/avatar/user.jpeg",
                "other": "./fig/avatar/default.jpeg"
            }
            ConfigManager._instance = self

            self._icon_path = {
                "文字消息": "./fig/icon/text-message.png",
                "语音消息": "./fig/icon/voice-message.png",
                "语音通话": "./fig/icon/voice-call.png",
                "视频通话": "./fig/icon/video-call.png",
                "图片消息": "./fig/icon/photo-message.png",
                "表情包": "./fig/icon/gif.png",
                "已领取": "./fig/icon/recieve-pocket.png",
                "插入时间": "./fig/icon/time.png",
            }
            self.emoji_map = {
                f"{i}": f"./fig/emojis/{i}.gif" for i in range(1, 109)
            }
            self.input_icon_path = {
                "voice": "./fig/icon/voice.png",
                "voice_pressed": "./fig/icon/voice_pressed.png",
                "emoji": "./fig/icon/emoji.png",
                "emoji_pressed": "./fig/icon/emoji_pressed.png",
                "others": "./fig/icon/others.png",
                "others_pressed": "./fig/icon/others_pressed.png",
            }

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = ConfigManager()
        return cls._instance

    def get_avatar_path(self, role: str) -> str:
        return self._avatars.get(role)
    
    def set_avatar_path(self, role: str, path: str):
        self._avatars[role] = path
        self.avatar_changed.emit(role, path)
    
    def get_icon_path(self, text: str) -> str:
        return self._icon_path.get(text, "./fig/icon/fix.png")

    def get_input_icon(self, icon_type: str) -> str:
        return self.input_icon_path.get(icon_type, "")
