<p align="center">
    <img width="600" height="215" src="https://uploads.hi.ls/2020-08/example-app.png">
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
```

## Changelog

#### native_web_app 1.0.0 (2020-08-11)

 - Initial Release

## FAQ

#### How do I detect when the browser window is closed?

We recommend you use JavaScript to notify your backend:

```javascript
window.addEventListener('unload', function() {
    navigator.sendBeacon("/shutdown");
}, false);
```

#### What about Firefox?

Firefox implemented what they call "site-specific browser functionality" in 2020, 
but it currently only supports HTTPS, i.e. it does not work with `http://127.0.0.1:1234` 
or `file://` URLs (<https://bugzilla.mozilla.org/show_bug.cgi?id=1631271>).
This makes it unsuitable for this project.