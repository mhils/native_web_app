import shutil
import subprocess
import webbrowser
from typing import Optional

try:
    import winreg
except ImportError:
    winreg = None


def read_registry_app_path(browser: str) -> Optional[str]:
    """Read an executable path from the Windows registry.
    Safe to call on all OSes, returns None if no entry has been found."""
    if not winreg:
        return None

    # https://docs.microsoft.com/en-us/windows/win32/shell/app-registration#using-the-app-paths-subkey
    APP_PATHS = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"
    browser += ".exe"

    try:
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, APP_PATHS, 0, winreg.KEY_READ
            ) as key:
                return winreg.QueryValue(key, browser)
        except FileNotFoundError:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, APP_PATHS, 0, winreg.KEY_READ
            ) as key:
                return winreg.QueryValue(key, browser)
    except OSError:
        return None


def get_executable(browser: str) -> Optional[str]:
    return shutil.which(browser) or read_registry_app_path(browser)


APP_BROWSERS = [
    "chrome",
    "msedge",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
]

# Order here is important: We first try the platform's default browsers and then some specific binaries.
FALLBACK_BROWSERS = [
    "windows-default",
    "macosx",
    "wslview %s",  # Open default Windows browser from WSL
    "x-www-browser %s",
    "gnome-open %s",
    "firefox",
    "opera",
    "safari",
]


def open(url: str, try_app_mode: bool = True) -> None:
    """
    Open a URL in a modern webbrowser.
    In contrast to webbrowser.open, this method gracefully degrades
    to a no-op on headless servers, where webbrowser.open would otherwise open lynx.

    Args:
        url:
            The URL to open, e.g. http://localhost:1234.
        try_app_mode:
            If True, try to open the URL in "app mode", i.e. without browser controls.
            This allows for Electron-like apps without having to deal with Electron.
            If no suitable browser is found, it gracefully falls back to a regular browser instance.

    Raises:
        RuntimeError, if no suitable browser is found.
        OSError, if the browser executable could not be executed.

        For robustness, implementors should catch any Exception and take that as a signal that opening the URL failed.
    """

    # We first try to see if we find a browser that offers an app mode:
    if try_app_mode:
        for browser in APP_BROWSERS:
            exe = get_executable(browser)
            if exe:
                try:
                    p = subprocess.Popen(
                        [exe, f"--app={url}"], close_fds=True, start_new_session=True
                    )
                    ret = p.poll()
                    if ret:
                        raise OSError(f"Early return: {ret}")
                except OSError as e:
                    pass
                else:
                    return

    # Fallback: We did not find an app-mode browser browser that offers an app mode, so
    for browser in FALLBACK_BROWSERS:
        try:
            b = webbrowser.get(browser)
        except webbrowser.Error:
            pass
        else:
            if b.open(url):
                return

    raise RuntimeError("could not locate runnable browser")


__all__ = ["open"]
__version__ = "1.0.2"
