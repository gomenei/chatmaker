from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QDialog, QRadioButton, QVBoxLayout, \
    QPushButton, QGroupBox, QLineEdit, QMessageBox, QCheckBox
from PyQt5.QtCore import Qt
from ui.config import ConfigManager


class StatusWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ConfigManager().instance()
        self.init_ui()

    def init_ui(self):
        self.setFixedHeight(24)
        self.setStyleSheet("background-color: #ededed; color: black;")
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 确保背景覆盖
        self.pattern = "huawei"

        self.status_layout = QHBoxLayout(self)
        self.status_layout.setContentsMargins(10, 0, 12, 0)

        # 左侧
        self.time = "10:00"
        self.status_left = QLabel(self.time)
        font = QFont("HarmonyOS Sans SC")
        self.status_left.setFont(font)
        self.status_layout.addWidget(self.status_left, alignment=Qt.AlignLeft)

        # 中间 → 替换为 QLabel 使其可以填充背景
        status_middle = QLabel("")
        status_middle.setStyleSheet("background-color: #ededed;")
        self.status_layout.addWidget(status_middle, stretch=1)

        # 右侧
        self.status_right = QWidget()
        right_layout = QHBoxLayout(self.status_right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        wifi = QLabel()
        wifi_pic = QPixmap(self.config.get_huawei_status_icon("normal_wifi"))
        wifi_pic = wifi_pic.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        wifi.setPixmap(wifi_pic)
        wifi.setFixedSize(20, 20)

        signal = QLabel()
        signal_pic = QPixmap(self.config.get_huawei_status_icon("signal_5G"))
        signal_pic = signal_pic.scaled(24, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        signal.setPixmap(signal_pic)
        signal.setFixedSize(24, 16)

        battery = QLabel()
        battery_pic = QPixmap(self.config.get_huawei_status_icon("battery_full"))
        battery_pic = battery_pic.scaled(30, 15, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        battery.setPixmap(battery_pic)
        battery.setFixedSize(30, 15)

        right_layout.addWidget(wifi, alignment=Qt.AlignRight)
        right_layout.addWidget(signal, alignment=Qt.AlignRight)
        right_layout.addWidget(battery, alignment=Qt.AlignRight)

        self.status_right.setLayout(right_layout)
        self.status_layout.addWidget(self.status_right)

    def change_pattern(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("模式选择")
        self.dialog.resize(250, 200)
        layout = QVBoxLayout()

        self.huawei_radio = QRadioButton("华为手机")
        self.apple_radio = QRadioButton("苹果手机")
        self.huawei_radio.setChecked(True)

        btn_confirm = QPushButton("确认选择")
        btn_confirm.clicked.connect(self.status_detail)

        layout.addWidget(self.huawei_radio)
        layout.addWidget(self.apple_radio)
        layout.addWidget(btn_confirm)

        self.dialog.setLayout(layout)

        self.dialog.exec_()

    def mouseDoubleClickEvent(self, event):
        self.change_pattern()
        super().mouseDoubleClickEvent(event)

    def status_detail(self):
        self.dialog.close()
        if self.huawei_radio.isChecked():
            self.huawei_status()
        elif self.apple_radio.isChecked():
            self.apple_status()

    def huawei_status(self):
        self.huawei_dialog = QDialog(self)
        self.huawei_dialog.setWindowTitle("状态栏细节")
        self.huawei_dialog.resize(400, 600)
        main_layout = QVBoxLayout()

        # 时间
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("请输入一个时间，格式为小时:分钟")
        self.time_input.setEnabled(True)
        self.time_input.editingFinished.connect(self.monitor_time_input)
        main_layout.addWidget(self.time_input)

        # 蓝牙
        bluetooth_group = QGroupBox("蓝牙状态")
        bluetooth_group_layout = QHBoxLayout()
        self.bluetooth_closed = QRadioButton("关闭蓝牙")
        self.bluetooth = QRadioButton("打开蓝牙")
        self.bluetooth_connected = QRadioButton("蓝牙已连接")
        self.bluetooth_electricity = QRadioButton("已连接设备电量")
        self.bluetooth_closed.setChecked(True)
        bluetooth_group_layout.addWidget(self.bluetooth_closed)
        bluetooth_group_layout.addWidget(self.bluetooth)
        bluetooth_group_layout.addWidget(self.bluetooth_connected)
        bluetooth_group_layout.addWidget(self.bluetooth_electricity)
        bluetooth_group.setLayout(bluetooth_group_layout)
        main_layout.addWidget(bluetooth_group)

        # 设备音量
        volume_group = QGroupBox("设备音量")
        volume_group_layout = QHBoxLayout()
        self.ring = QRadioButton("响铃")
        self.vibrate = QRadioButton("振动")
        self.mute = QRadioButton("静音")
        self.ring.setChecked(True)
        volume_group_layout.addWidget(self.ring)
        volume_group_layout.addWidget(self.vibrate)
        volume_group_layout.addWidget(self.mute)
        volume_group.setLayout(volume_group_layout)
        main_layout.addWidget(volume_group)

        # 热点
        hotspot_group = QGroupBox("热点")
        hotspot_group_layout = QHBoxLayout()
        self.no_hotspot = QRadioButton("关闭热点")
        self.hotspot = QRadioButton("打开热点")
        self.no_hotspot.setChecked(True)
        hotspot_group_layout.addWidget(self.no_hotspot)
        hotspot_group_layout.addWidget(self.hotspot)
        hotspot_group.setLayout(hotspot_group_layout)
        main_layout.addWidget(hotspot_group)

        # 网络
        net_group = QGroupBox("网络")
        net_group_layout = QHBoxLayout()
        self.no_wifi = QRadioButton("关闭网络")
        self.normal_wifi = QRadioButton("WiFi正常")
        self.hotspot_wifi = QRadioButton("连接至热点")
        self.abnormal_wifi = QRadioButton("WiFi故障")
        self.normal_wifi.setChecked(True)
        net_group_layout.addWidget(self.no_wifi)
        net_group_layout.addWidget(self.normal_wifi)
        net_group_layout.addWidget(self.hotspot_wifi)
        net_group_layout.addWidget(self.abnormal_wifi)
        net_group.setLayout(net_group_layout)
        main_layout.addWidget(net_group)

        # 飞行模式
        fly_group = QGroupBox("网络相关")
        fly_group_layout = QVBoxLayout()
        fly_group.setLayout(fly_group_layout)
        self.flying = QCheckBox("飞行模式")
        self.flying.stateChanged.connect(self.huawei_flying)
        fly_group_layout.addWidget(self.flying)

        # 信号
        signal_group = QGroupBox("信号")
        signal_group_layout = QHBoxLayout()
        self.signal_4G = QRadioButton("4G信号")
        self.signal_5G = QRadioButton("5G信号")
        self.signal_out = QRadioButton("无信号")
        self.signal_4G.setChecked(True)
        signal_group_layout.addWidget(self.signal_4G)
        signal_group_layout.addWidget(self.signal_5G)
        signal_group_layout.addWidget(self.signal_out)
        signal_group.setLayout(signal_group_layout)
        fly_group_layout.addWidget(signal_group)

        main_layout.addWidget(fly_group)

        # 电池
        battery_group = QGroupBox("电池状态")
        battery_group_layout = QVBoxLayout()
        up_layout = QHBoxLayout()
        self.electricity_full = QRadioButton("满格电量")
        self.electricity_half = QRadioButton("半格电量")
        self.electricity_out = QRadioButton("电池没电")
        up_layout.addWidget(self.electricity_full)
        up_layout.addWidget(self.electricity_half)
        up_layout.addWidget(self.electricity_out)
        down_layout = QHBoxLayout()
        self.charging = QRadioButton("正在充电")
        self.super_charging = QRadioButton("超级快充")
        self.save_electricity = QRadioButton("省电模式")
        down_layout.addWidget(self.charging)
        down_layout.addWidget(self.super_charging)
        down_layout.addWidget(self.save_electricity)
        self.electricity_full.setChecked(True)
        battery_group_layout.addLayout(up_layout)
        battery_group_layout.addLayout(down_layout)
        battery_group.setLayout(battery_group_layout)
        main_layout.addWidget(battery_group)

        # 其他
        other_group = QGroupBox("可选状态")
        other_group_layout = QVBoxLayout()
        # 护眼模式
        self.eye_protecting = QCheckBox("护眼模式")
        # nfc模式
        self.nfc = QCheckBox("NFC模式")
        # 闹钟
        self.clock = QCheckBox("闹钟")
        # 免打扰
        self.do_not_disturb = QCheckBox("免打扰")
        other_group_layout.addWidget(self.eye_protecting)
        other_group_layout.addWidget(self.nfc)
        other_group_layout.addWidget(self.clock)
        other_group_layout.addWidget(self.do_not_disturb)
        other_group.setLayout(other_group_layout)
        main_layout.addWidget(other_group)

        # 确认
        btn_confirm = QPushButton("确认选择")
        main_layout.addWidget(btn_confirm)
        btn_confirm.clicked.connect(self.huawei_pattern)

        self.huawei_dialog.setLayout(main_layout)

        self.huawei_dialog.exec_()

    def apple_status(self):
        self.apple_dialog = QDialog(self)
        self.apple_dialog.setWindowTitle("状态栏细节")
        self.apple_dialog.resize(400, 600)
        main_layout = QVBoxLayout()

        # 时间
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("请输入一个时间，格式为小时:分钟")
        self.time_input.setEnabled(True)
        self.time_input.editingFinished.connect(self.monitor_time_input)
        main_layout.addWidget(self.time_input)

        # 信号
        signal_group = QGroupBox("信号")
        signal_group_layout = QHBoxLayout()
        self.signal = QRadioButton("满格信号")
        self.flying = QRadioButton("飞行模式")
        self.signal.setChecked(True)
        signal_group_layout.addWidget(self.signal)
        signal_group_layout.addWidget(self.flying)
        signal_group.setLayout(signal_group_layout)
        main_layout.addWidget(signal_group)

        # 网络
        net_group = QGroupBox("网络")
        net_group_layout = QHBoxLayout()
        self.no_wifi = QRadioButton("关闭网络")
        self.normal_wifi = QRadioButton("WiFi正常")
        self.normal_wifi.setChecked(True)
        net_group_layout.addWidget(self.no_wifi)
        net_group_layout.addWidget(self.normal_wifi)
        net_group.setLayout(net_group_layout)
        main_layout.addWidget(net_group)

        # 确认
        btn_confirm = QPushButton("确认选择")
        main_layout.addWidget(btn_confirm)
        btn_confirm.clicked.connect(self.apple_pattern)

        self.apple_dialog.setLayout(main_layout)

        self.apple_dialog.exec_()

    def monitor_time_input(self):
        time = self.time_input.text()
        try:
            if ":" in time:
                h, m = time.split(":")
            elif "：" in time:
                h, m = time.split("：")
            else:
                raise ValueError("Invalid format")
            hour, minute = int(h.strip()), int(m.strip())

            # 验证小时和分钟范围
            if not (0 <= hour < 24) or not (0 <= minute < 60):
                raise ValueError("Out of range")

            self.time = str(hour) + ":" + str(minute)
        except ValueError as e:
            wrong_box_format = QMessageBox()
            wrong_box_format.setIcon(QMessageBox.Critical)
            wrong_box_format.setWindowTitle("错误提示")
            wrong_box_format.setText(f"时间格式错误: {e}")
            wrong_box_format.exec_()

    def huawei_pattern(self):
        self.monitor_time_input()
        # self.status_layout.setContentsMargins(90, 0, 12, 0)

        # 左侧时间
        font = QFont("HarmonyOS Sans SC")
        self.status_left.setFont(font)
        self.status_left.setText(self.time)

        # 右侧其他
        right_layout = self.status_right.layout()
        if right_layout:
            # 清空布局中的控件
            while right_layout.count():
                item = right_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        else:
            right_layout = QHBoxLayout(self.status_right)
            right_layout.setContentsMargins(0, 0, 0, 0)
            right_layout.setSpacing(0)

        # 护眼模式
        if self.eye_protecting.isChecked():
            eye_protecting = QLabel()
            eye_protecting_pic = QPixmap(self.config.get_huawei_status_icon("eye_protecting"))
            eye_protecting_pic = eye_protecting_pic.scaled(21, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            eye_protecting.setPixmap(eye_protecting_pic)
            eye_protecting.setFixedSize(21, 14)
            right_layout.addWidget(eye_protecting)
        # NFC
        if self.nfc.isChecked():
            nfc = QLabel()
            nfc_pic = QPixmap(self.config.get_huawei_status_icon("nfc"))
            nfc_pic = nfc_pic.scaled(14, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            nfc.setPixmap(nfc_pic)
            nfc.setFixedSize(14, 14)
            right_layout.addWidget(nfc)
        # 闹钟
        if self.clock.isChecked():
            clock = QLabel()
            clock_pic = QPixmap(self.config.get_huawei_status_icon("clock"))
            clock_pic = clock_pic.scaled(14, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            clock.setPixmap(clock_pic)
            clock.setFixedSize(14, 14)
            right_layout.addWidget(clock)
        # 蓝牙
        if self.bluetooth_closed.isChecked():
            pass
        else:
            bluetooth = QLabel()
            if self.bluetooth.isChecked():
                bluetooth_pic = QPixmap(self.config.get_huawei_status_icon("bluetooth"))
                bluetooth_pic = bluetooth_pic.scaled(11, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                bluetooth.setPixmap(bluetooth_pic)
                bluetooth.setFixedSize(11, 16)
            elif self.bluetooth_connected.isChecked():
                bluetooth_pic = QPixmap(self.config.get_huawei_status_icon("bluetooth_connected"))
                bluetooth_pic = bluetooth_pic.scaled(12, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                bluetooth.setPixmap(bluetooth_pic)
                bluetooth.setFixedSize(12, 18)
            else:
                bluetooth_pic = QPixmap(self.config.get_huawei_status_icon("bluetooth_electricity"))
                bluetooth_pic = bluetooth_pic.scaled(20, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                bluetooth.setPixmap(bluetooth_pic)
                bluetooth.setFixedSize(20, 16)
            right_layout.addWidget(bluetooth)
        # 免打扰
        if self.do_not_disturb.isChecked():
            do_not_disturb = QLabel()
            do_not_disturb_pic = QPixmap(self.config.get_huawei_status_icon("do_not_disturb"))
            do_not_disturb_pic = do_not_disturb_pic.scaled(14, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            do_not_disturb.setPixmap(do_not_disturb_pic)
            do_not_disturb.setFixedSize(14, 14)
            right_layout.addWidget(do_not_disturb)

        # 设备音量
        if self.ring.isChecked():
            pass
        else:
            volume = QLabel()
            if self.vibrate.isChecked():
                volume_pic = QPixmap(self.config.get_huawei_status_icon("vibrate"))
                volume_pic = volume_pic.scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                volume.setPixmap(volume_pic)
                volume.setFixedSize(18, 18)
            else:
                volume_pic = QPixmap(self.config.get_huawei_status_icon("mute"))
                volume_pic = volume_pic.scaled(12, 15, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                volume.setPixmap(volume_pic)
                volume.setFixedSize(12, 15)
            right_layout.addWidget(volume)

        # 热点
        if self.no_hotspot.isChecked():
            pass
        else:
            hotspot = QLabel()
            hotspot_pic = QPixmap(self.config.get_huawei_status_icon("hotspot"))
            hotspot_pic = hotspot_pic.scaled(14, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            hotspot.setPixmap(hotspot_pic)
            hotspot.setFixedSize(14, 14)
            right_layout.addWidget(hotspot)
        # 网络
        if not self.no_wifi.isChecked():
            wifi = QLabel()
            if self.abnormal_wifi.isChecked():
                wifi_pic = QPixmap(self.config.get_huawei_status_icon("abnormal_wifi"))
            elif self.hotspot_wifi.isChecked():
                wifi_pic = QPixmap(self.config.get_huawei_status_icon("hotspot_wifi"))
            else:
                wifi_pic = QPixmap(self.config.get_huawei_status_icon("normal_wifi"))
            wifi_pic = wifi_pic.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            wifi.setPixmap(wifi_pic)
            wifi.setFixedSize(20, 20)
            right_layout.addWidget(wifi, alignment=Qt.AlignRight)

        # 飞行模式
        if self.flying.isChecked():
            flying = QLabel()
            flying_pic = QPixmap(self.config.get_huawei_status_icon("flying"))
            flying_pic = flying_pic.scaled(14, 14, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            flying.setPixmap(flying_pic)
            flying.setFixedSize(14, 14)
            right_layout.addWidget(flying)
        else:
            # 信号
            signal = QLabel()
            if self.signal_4G.isChecked():
                signal_pic = QPixmap(self.config.get_huawei_status_icon("signal_4G"))
            elif self.signal_out.isChecked():
                signal_pic = QPixmap(self.config.get_huawei_status_icon("signal_out"))
            else:
                signal_pic = QPixmap(self.config.get_huawei_status_icon("signal_5G"))
            signal_pic = signal_pic.scaled(24, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            signal.setPixmap(signal_pic)
            signal.setFixedSize(24, 16)
            right_layout.addWidget(signal, alignment=Qt.AlignRight)

        # 电池
        battery = QLabel()
        if self.save_electricity.isChecked():
            battery_pic = QPixmap(self.config.get_huawei_status_icon("save_electricity"))
        elif self.electricity_half.isChecked():
            battery_pic = QPixmap(self.config.get_huawei_status_icon("battery_half"))
        elif self.electricity_out.isChecked():
            battery_pic = QPixmap(self.config.get_huawei_status_icon("battery_out"))
        elif self.charging.isChecked():
            battery_pic = QPixmap(self.config.get_huawei_status_icon("charging"))
        elif self.super_charging.isChecked():
            battery_pic = QPixmap(self.config.get_huawei_status_icon("super_charging"))
        else:
            battery_pic = QPixmap(self.config.get_huawei_status_icon("battery_full"))
        battery_pic = battery_pic.scaled(30, 15, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        battery.setPixmap(battery_pic)
        battery.setFixedSize(30, 15)
        right_layout.addWidget(battery, alignment=Qt.AlignRight)

        self.status_right.setLayout(right_layout)

    def apple_pattern(self):
        self.monitor_time_input()
        # self.status_layout.setContentsMargins(90, 0, 12, 0)

        # 左侧时间
        font = QFont("Inter SemiBold")
        self.status_left.setFont(font)
        self.status_left.setText(self.time)

        # 右侧其他
        right_layout = self.status_right.layout()
        if right_layout:
            # 清空布局中的控件
            while right_layout.count():
                item = right_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        else:
            right_layout = QHBoxLayout(self.status_right)
            right_layout.setContentsMargins(0, 0, 0, 0)
            right_layout.setSpacing(0)

        # 信号
        if self.flying.isChecked():
            flying = QLabel()
            flying_pic = QPixmap(self.config.get_apple_status_icon("flying"))
            flying_pic = flying_pic.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            flying.setPixmap(flying_pic)
            flying.setFixedSize(16, 16)
            right_layout.addWidget(flying)
        else:
            signal = QLabel()
            signal_pic = QPixmap(self.config.get_apple_status_icon("signal"))
            signal_pic = signal_pic.scaled(24, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            signal.setPixmap(signal_pic)
            signal.setFixedSize(24, 16)
            right_layout.addWidget(signal, alignment=Qt.AlignRight)

        # 网络
        if not self.no_wifi.isChecked():
            wifi = QLabel()
            wifi_pic = QPixmap(self.config.get_apple_status_icon("wifi"))
            wifi_pic = wifi_pic.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            wifi.setPixmap(wifi_pic)
            wifi.setFixedSize(20, 20)
            right_layout.addWidget(wifi, alignment=Qt.AlignRight)

        battery = QLabel()
        battery_pic = QPixmap(self.config.get_apple_status_icon("battery"))
        battery_pic = battery_pic.scaled(40, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        battery.setPixmap(battery_pic)
        battery.setFixedSize(40, 20)
        right_layout.addWidget(battery, alignment=Qt.AlignRight)

    def huawei_flying(self):
        if self.flying.isChecked():
            self.signal_4G.setEnabled(False)
            self.signal_5G.setEnabled(False)
            self.signal_out.setEnabled(False)
        else:
            self.signal_4G.setEnabled(True)
            self.signal_5G.setEnabled(True)
            self.signal_out.setEnabled(True)