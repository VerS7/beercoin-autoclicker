"""
Beertap Game miner
"""
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect

from selenium.common.exceptions import StaleElementReferenceException

from .settings import settings

sleep_impl = sleep


class AutoClicker:
    def __init__(self, cookie_path: str, notificator=None):
        """
        :param cookie_path: Path to Google Chrome cookies
        """
        self._options = webdriver.ChromeOptions()
        self._options.add_argument(f"user-data-dir={cookie_path}")
        self._options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self._options)
        self.wait = WebDriverWait(self.driver, 20)

        self._tap_btn = None
        self._clicker_data = None

        self._notificator = notificator

    def _update_clicker_data(self):
        """Update clicker data element"""
        self._clicker_data = self.wait.until(
            expect.visibility_of_element_located((
                By.XPATH, '//*[@id="root"]/main/div[1]'
            ))
        )

    @property
    def window_fps(self) -> str:
        """Get window FPS"""
        return self.driver.execute_script(
            "const getFPS = () => "
            "new Promise(resolve => "
            "requestAnimationFrame(t1 => requestAnimationFrame(t2 => resolve(1000 / (t2 - t1)))));"
            "return await getFPS();"
        )

    @property
    def total(self) -> str:
        """
        Get total earned coins
        :return str:
        """
        return self._clicker_data.text.split('\n')[-1]

    @property
    def earn(self) -> str | None:
        """
        Get last earned coins
        :return str:
        """
        try:
            data = self._clicker_data.text.split('\n')
        except StaleElementReferenceException:
            self._update_clicker_data()
            return None

        if len(data) != 3:
            return None

        return self._clicker_data.text.split('\n')[1].replace("+ ", "")

    def update(self):
        """Tick"""
        for i in range(settings.clicks_per_update):
            self._tap_btn.click()
            sleep_impl(0.07)
        sleep_impl(1.7)

        if self._notificator is not None:
            self._notificator.update(earn=self.earn, total=self.total)

    def run(self):
        """Run clicker"""
        self.driver.get("https://web.telegram.org/k/#@BeerCoinTap_Bot")
        # Set window size to minimal working
        self.driver.set_window_size(840, 960)
        # Hide window by set position to large amount
        if settings.hide_window:
            self.driver.set_window_position(32000, 32000)
        else:
            self.driver.set_window_position(500, 0)
        # Wait until "Start Beertap Game" button appears and click
        self.wait.until(
            expect.visibility_of_element_located((
                By.XPATH, '//*[@id="column-center"]/div/div/div[4]/div/div[1]/div/div[8]/div[1]/div[2]'
            ))
        ).click()
        # Wait until "Beertap Game" frame appears and switch to it
        self.driver.switch_to.frame(
            self.wait.until(
                expect.visibility_of_element_located((
                    By.XPATH, '/html/body/div[7]/div/div[2]/iframe')
                ))
        )
        # Wait until "Start game" button appears and click
        self.wait.until(
            expect.visibility_of_element_located((
                By.XPATH, '//*[@id="root"]/main/div/div/button'
            ))
        ).click()
        # Element of total coins earned
        self._update_clicker_data()
        # "Tap here" button
        self._tap_btn = self.wait.until(
            expect.visibility_of_element_located((
                By.XPATH, '//*[@id="root"]/main/div[3]/button'
            ))
        )

        while True:
            self.update()
