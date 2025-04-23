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
                "me": "./fig/lyc.jpeg",
                "other": "./fig/default.jpeg"
            }
            ConfigManager._instance = self
    
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
