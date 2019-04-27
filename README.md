# PlusPlus2 

PlusPlus2 is a resurrection of the former [plusplus.chat](http://plusplus.chat). It was implemented in Python and 
is (somewhat) based on the [Javascript version](https://github.com/tdmalone/working-plusplus/) by @tdmalone.

If you didn't use plusplus.chat before it went offline, it was an app that let you reward members of your slack team with imaginary points. All you had to do was type something like `@jake++` to reward someone a point, or `@jake--` to take away a point. 


### Features

- `@jake++`: give a point to a user or a thing
- `@jake--`: take a point away from a user or a thing
- `@jake==`: get the current number of points a user or thing has
- `plusplus leaderboard`: get (up to) 10 of the top users and things

### Install Instructions

(Instructions adapted from [here](https://github.com/tdmalone/working-plusplus/blob/master/README.md#installation))

1. **Create a new app in your Slack team.**

   You can do this from the [Slack API Apps page](https://api.slack.com/apps). 
   You'll need permission to add new apps, which depending on your team settings might require an admin to do it for you.

1. **Add a bot user for your app.**

    This can be done under *Bot Users* in the menu on the left. You can name it whatever you like, and for best results, select it to always show as online.

    This allows the app to speak back to your team when they ++ and -- things.

1. **Add chat permissions, and install the app.**

   Under *OAuth & Permissions*, scroll down to *Scopes* and add the `chat:write:bot` permission. Click *Save Changes*.

   You can now install the app. Scroll back up, click *Install App to Workspace*, and follow the prompts.

1. **Copy your tokens.**

   From the same *OAuth & Permissions* page, copy the ***Bot** User OAuth Access Token* (_not_ the non-bot token!) and store it somewhere.

   Go back to the *Basic Information* page, scroll down, and copy the *Signing Secret* too.

1. **Deploy the app to Heroku.**

   [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
 
   This app was designed for Heroku, and shouldn't cost much to operate there. You may have to put in a credit card to increase the number of free hours alloted per month, though.
   
1. **Back at Slack apps, switch on *Event Subscriptions* for your app.**

   Via *Event Subscriptions* in the left menu. After switching on, enter your new Heroku app address - eg. `https://my-plusplus.herokuapp.com` - as the request URL.

   Scroll down and, under *Subscribe to Bot Events*, select the relevant events for the features you want the app to support:

   * Select `message.channels` to support all general features in _public_ channels it is invited to
   * Select `message.groups` to support all general features in _private_ channels it is invited to
   * Select `app_mention` to support extended features such as leaderboards

   Finally, click *Save Changes*. If you wish, you can come back to this screen later and add or change the events the app handles.

1. **Invite your new bot to any channel in your Slack team and use it.**

    */invite @yourplusplus2bot*
    
    *@jake++*
    
## Contributions

Contributions are welcome to this repository! Please open an issue/check for open issues _before_ starting a change.

