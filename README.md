<p align="center">
    <img alt="demo app screenshot" width="600" height="215" src="https://uploads.hi.ls/2020-08/example-app.png">
</p>

# native-web-app
![](https://img.shields.io/pypi/wheel/native-web-app.svg)
![](https://img.shields.io/pypi/v/native-web-app.svg)
![](https://img.shields.io/pypi/pyversions/native-web-app.svg)
![](https://img.shields.io/pypi/l/native-web-app.svg)

A drop-in replacement for Python's `webbrowser.open()` 
that opens a native browser window without browser controls. Build Electron-style apps without shipping Electron!

```python
import native_web_app

url = "http://localhost:8000/"

try:
    native_web_app.open(url)
except Exception:
    print(f"No web browser found. Please open a browser and point it to {url}.")
```

## Demo

There is an [example app](https://github.com/mhils/native_web_app/blob/master/example-app.pyw) in the repository.

## API Documentation

This module exposes a single `open` function:

```python
def open(url: str, try_app_mode: bool = True) -> None:
    """
    Open a URL in a modern browser.
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
```

## Compatibility

OS | Browser | Status (✅ app mode, ☑️ regular browser)
--- | --- | ---
Windows 10 (2004) | Google Chrome 84 | ✅
Windows 10 (2004) | Microsoft Edge 84 | ✅
Windows 10 (2004) | Windows Subsystem for Linux | ☑️
Windows 10 (2004) | Default Browser | ☑️
Ubuntu 20.04 | Google Chrome 84 | ✅
Ubuntu 20.04 | Default Browser | ☑️
macOS Catalina | Google Chrome 84 | ✅
macOS Catalina | Default Browser | ☑️

Firefox implemented app mode ("site-specific browser functionality") in 2020,
but enabled it only for `https://` URLs. This means it [does not work with `http://localhost:1234`
or `file://` URLs](https://bugzilla.mozilla.org/show_bug.cgi?id=1631271).
This makes it unsuitable for inclusion in native_web_app.

## Changelog

This project follows semantic versioning.

#### native_web_app 1.0.2 (2020-08-12)

 - Add support for Python 3.5 and 3.6.

#### native_web_app 1.0.1 (2020-08-12)

 - Enforce browsers to start in background. This fixes
   compatibility with Microsoft Edge on Windows 10.
 - Extend documentation on compatibility.

#### native_web_app 1.0.0 (2020-08-11)

 - Initial Release

## FAQ

#### How do I detect when the browser window is closed?

Monitoring the spawned browser process does not work reliably across platforms.
We recommend you use JavaScript to notify your backend:

```javascript
window.addEventListener('unload', function() {
    navigator.sendBeacon("/shutdown");
}, false);
```
