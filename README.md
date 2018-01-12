# Twitch League Of Legends overlay

## Components
### getImages
Return, for a given locale (e.g. `en_GB`) a list of all the items in League current patch.
```
getImages(locale:string) -> [{
    name:string,
    description:string,
    imageURL:string,
    imageData:string
}]
```

* Throws an exception if unable to download images
* Throws an exception if locale does not exist

### getScreenshot
Return, for a given streamer name, a screenshot of his stream.
If the streamer isn't streaming, returns `null`.

```
getScreen
