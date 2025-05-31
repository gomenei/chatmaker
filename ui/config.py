from PyQt5.QtCore import QObject, pyqtSignal, QFile


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
                "发送转账": "./fig/icon/transfer_send.png",
                "收到转账": "./fig/icon/transfer_receive.png",
                "发送红包": "./fig/icon/red_pocket_send.png",
                "收到红包": "./fig/icon/red_pocket_receive.png",
                "插入时间": "./fig/icon/time.png",
                "拍一拍": "./fig/icon/tickle.png",
                "领取红包": "./fig/icon/red_pocket.png",
                "转账过期": "./fig/icon/transfer__.png",
                "撤回消息": "./fig/icon/revoke.png",
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
            self.huawei_status_icon_path = {
                "eye_protecting": "./fig/status/huawei_status/eye_protecting.png",
                "nfc": "./fig/status/huawei_status/nfc.png",
                "clock": "./fig/status/huawei_status/clock.png",

                "bluetooth": "./fig/status/huawei_status/bluetooth.png",
                "bluetooth_connected": "./fig/status/huawei_status/bluetooth_connected.png",
                "bluetooth_electricity": "./fig/status/huawei_status/bluetooth_electricity.png",

                "do_not_disturb": "./fig/status/huawei_status/do_not_disturb.png",

                "vibrate": "./fig/status/huawei_status/vibrate.png",
                "mute": "./fig/status/huawei_status/mute.png",

                "flying": "./fig/status/huawei_status/flying.png",

                "hotspot": "./fig/status/huawei_status/hotspot.png",

                "normal_wifi": "./fig/status/huawei_status/normal_wifi.png",
                "hotspot_wifi": "./fig/status/huawei_status/hotspot_wifi.png",
                "abnormal_wifi": "./fig/status/huawei_status/abnormal_wifi.png",

                "signal_4G": "./fig/status/huawei_status/signal_4G.png",
                "signal_5G": "./fig/status/huawei_status/signal_5G.png",
                "signal_out": "./fig/status/huawei_status/signal_out.png",

                "battery_full": "./fig/status/huawei_status/battery_full.png",
                "battery_half": "./fig/status/huawei_status/battery_half.png",
                "battery_out": "./fig/status/huawei_status/battery_out.png",
                "charging": "./fig/status/huawei_status/charging.png",
                "super_charging": "./fig/status/huawei_status/super_charging.png",
                "save_electricity": "./fig/status/huawei_status/save_electricity.png"
            }

            self.apple_status_icon_path = {
                "signal": "./fig/status/apple_status/signal.png",
                "flying": "./fig/status/apple_status/flying.png",

                "wifi": "./fig/status/apple_status/wifi.png",

                "battery": "./fig/status/apple_status/battery.png",
            }

            self.pocket_path = {
                "red_pocket_send_me": "./fig/pocket/red_pocket_send_me.png",
                "red_pocket_send_other": "./fig/pocket/red_pocket_send_other.png",
                "red_pocket_receive_me": "./fig/pocket/red_pocket_receive_me.png",
                "red_pocket_receive_other": "./fig/pocket/red_pocket_receive_other.png",
                "transfer_send_me": "./fig/pocket/transfer_send_me.png",
                "transfer_send_other": "./fig/pocket/transfer_send_other.png",
                "transfer_receive_me": "./fig/pocket/transfer_receive_me.png",
                "transfer_receive_other": "./fig/pocket/transfer_receive_other.png",
            }

            self.refuse_icon_path = "./fig/icon/refuse.png"

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

    def get_huawei_status_icon(self, status: str) -> str:
        return self.huawei_status_icon_path.get(status, "")

    def get_apple_status_icon(self, status: str) -> str:
        return self.apple_status_icon_path.get(status, "")

    def get_pocket_path(self, pocket_type: str) -> str:
        #检查
        path = self.pocket_path.get(pocket_type, "")
        if path and not QFile.exists(path):
            print(f"Warning: Pocket image not found: {path}")
        return path

    def get_refuse_icon(self) -> str:
        return self.refuse_icon_path