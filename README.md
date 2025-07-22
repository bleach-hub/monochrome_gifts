# Color Similarity Script

> _will help you with finding monochrome gifts_

## Some information

- **How does it work?** *Short answer: Magic.*
- **How accurate is it?** _There's no way you can code 100% accurate script for monochrome gifts without using AI models or stuff like that. But this script gives you pretty nice amount of successes. I would say it's around 70-80%._
- _**How can it be improved?** _The key thing is calculating the similarity. If you're a good coder and know how to work with colors - you may improve success rate to 90%+. I tried, I failed :D__

## Basic usage

> *Note: this is **NOT** the bot for finding gifts. If you want to use this script with a bot, you need to write it yourself. It's simple (you can check out [my Portals library](https://github.com/bleach-hub/aportalsmp)). Just don't be lazy like me :D*

Main function is **colorSimilarity()**. 

It takes two arguments: short name of the gift *(e.g. bdaycandle, durovscap, jackinthebox etc.)* and the number of the gift *(e.g. 1, 100, 111 etc.)*

```python
result  =  asyncio.run(colorSimilarity("bdaycandle", 96898))
print(result.get("similarity")) # 92.91 - similarity%
```

## What can it find (3 examples)

> There's much more though xd

- [https://i.ibb.co/pBbjz7Xp/Candy-Cane.png](https://i.ibb.co/HDHxQQvw/Lol-Pop.png)
- [https://i.ibb.co/C3bJT93X/Restless-Jar.png](https://i.ibb.co/HDHxQQvw/Lol-Pop.png)
- [https://i.ibb.co/HDHxQQvw/Lol-Pop.png](https://i.ibb.co/HDHxQQvw/Lol-Pop.png)

# Contacts

* *my telegram: [https://t.me/perfectlystill](https://t.me/perfectlystill)*
* *telegram channel: [https://t.me/giftsdevs](https://t.me/giftsdevs)*
* *telegram chat: [https://t.me/giftsdevschat](https://t.me/giftsdevschat)*
