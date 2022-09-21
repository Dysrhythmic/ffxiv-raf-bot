### This bot is not up-to-date.

The FFXIV website has been updated so that the bot will no longer work properly. I currently have no plans to update the bot as I no longer have a use for it, and I can no longer test getting the codes from their website since I no longer have a FFXIV subscription.

---

The FFXIV RAF Bot utilizes [Selenium](https://www.selenium.dev/documentation/en/getting_started_with_webdriver/) to open FireFox, login to the Mogstation with given credentials from a .env file, navigate to the page where Recruit-A-Friend codes are generated, copy the code, post the code on the official FFXIV forum in the [Official Recruit a Friend Code Thread](https://forum.square-enix.com/ffxiv/threads/272808-Official-Recruit-a-Friend-Code-Thread), and post the code in the [FFXIV: Recruit-A-Friend subreddit](https://www.reddit.com/r/ffxivraf/).

To customize the post, edit the "post.txt" file. The bot will replace any instances of `<CODE>` in that file with the invitation code when posting the message.

It logs the recruitment code and the URLs of the posts it creates in a "bot.log" file that it creates. Since recruitment codes can only be generated once every 3 hours, it will check the log for the date and time of the last line and only continue if it has been longer than 3 hours since that time. If it hasn't, it will print a message in the terminal with the time remaining until the 3 hours have passed.

Since the bot is using Selenium to run FireFox, it requires [FireFox](https://www.mozilla.org/en-US/firefox/new/) and [GeckoDriver](https://github.com/mozilla/geckodriver/).
