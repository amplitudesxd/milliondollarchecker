# milliondollarchecker

this checks the registration status of all domains on milliondollarhomepage.com, then a list of all available domains are output to the console

the list of domains was scraped using the following javascript code

```js
let pixels = [];
Array.from(document.getElementById('Map').children).forEach((child) => {
  pixels.push({
    coords: child.getAttribute('coords'),
    site: child.getAttribute('href'),
  });
});
document.body.innerHTML = JSON.stringify(pixels);
```
