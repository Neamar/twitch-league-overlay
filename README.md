# Twitch League Of Legends overlay
See [goals.md](goals.md) for a description of what we're trying to achieve.

## Setup
```
python3 -m venv venv

# Then, every time, run
source ./venv/bin/activate
```

## Components
### getItems
Return, for a given locale (e.g. `en_GB`) a list of all the items in League current patch.
```
get_items(locale:string) -> [Item]
```

* Throws an exception if unable to download images
* Throws an exception if locale does not exist
* `imagePath` is a path on the filesystem, most likely within `/tmp`

where `Item` is the following class:

```
{
    name:string,
    description:string,
    image_url:string,
    image_path:string
}
```

### getScreenshot
Return, for a given streamer name, a screenshot of his stream.

```
get_screenshot(streamer_name:string) -> {
    screenshot_path:string
}
```

* If this function needs other information (e.g. a Twitch API key), read it from environment
* `imagePath` is a path on the filesystem, most likely within `/tmp`
* If the streamer isn't streaming, returns `null`.
* Image has to be of `source` quality

### parseScreenshot
Parse the given screenshot, looking for items (as returned by `getItems()`) in it.

```
parse_screenshot(screenshot_path, items) -> [{
    rect: Rect,
    item: Item
}]
```

where `Rect` is the following class:

```
{
    x: int,
    y: int,
    width: int,
    height: int
}
```

### fakeHTMLScaffold
A fake HTML page displaying a screenshot, and loading the required CSS and JS for tooltip display.

Only used for demo purpose.


### buildHTML
Builds an HTML page with the tooltips,
Returns a div with embedded CSS for the positioning
Can assume that a CSS and a JS file have been loaded into the page before (for instance, by fakeHTMLScaffold).
