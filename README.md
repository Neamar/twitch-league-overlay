# Twitch League Of Legends overlay

## Components
### getItems
Return, for a given locale (e.g. `en_GB`) a list of all the items in League current patch.
```
getItems(locale:string) -> [Item]
```

* Throws an exception if unable to download images
* Throws an exception if locale does not exist
* `imagePath` is a path on the filesystem, most likely within `/tmp`

where `Item` is the following class:

```
{
    name:string,
    description:string,
    imageURL:string,
    imagePath:string
}
```

### getScreenshot
Return, for a given streamer name, a screenshot of his stream.

```
getScreenshot(streamerName:string) -> {
    screenshotPath:string
}
```

* If this function needs other information (e.g. a Twitch API key), read it from environment
* `imagePath` is a path on the filesystem, most likely within `/tmp`
* If the streamer isn't streaming, returns `null`.
* Image has to be of `source` quality

### parseScreenshot
Parse the given screenshot, looking for items (as returned by `getItems()`) in it.

```
parseScreenshot(screenshotPath, items) -> [{
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
