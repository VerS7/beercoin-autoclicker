"""
Main
"""
from autoclicker.clicker import AutoClicker
from autoclicker.notification.console.notificator import ConsoleNotificator
from autoclicker.settings import settings


clicker = AutoClicker(cookie_path=settings.cookie_path,
                      notificator=ConsoleNotificator())

try:
    clicker.run()
except:
    exit()
