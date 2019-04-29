# PlusPl.us Server

PlusPl.us is a resurrection of the former [plusplus.chat](http://plusplus.chat). It was implemented in Python and 
is (somewhat) based on the [Javascript version](https://github.com/tdmalone/working-plusplus/) by @tdmalone, but has 
been expanded to work as a fully hosted Slack app for multiple teams like the original plusplus.chat.

If you didn't use plusplus.chat before it went offline, it was an app that let you reward members of your Slack team 
with imaginary points. All you had to do was type something like `@jake++` to reward someone a point, or `@jake--` 
to take away a point. A few additional features have been built in (see below), and more features are planned.


### Features

- `@jake++`: give a point to a user or a thing
- `@jake--`: take a point away from a user or a thing
- `@jake==`: get the current number of points a user or thing has
- `@pluspl.us leaderboard`: get (up to) 10 of the top users and things
- `@pluspl.us loserboard`: get (up to) 10 of the bottom users and things
- `@pluspl.us help`: get a list of the available commands from within Slack


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

1. **Add a redirect URL**

   Under the *OAuth & Permissions* section, scroll down to *Redirect URLs* and add the following URL:
   `<your_domain_name.com>/slack/callback`
   
1. **Copy your tokens.**

   From the same *Basic Information* page, store the following tokens (you'll need them to setup the app on Heroku): 
   
   - The Client ID
   - The Client Secret
   - The Signing Secret
  
   From the *Manage Distribution* page, stor the *Shareable URL*.

1. **Register for Sentry.io**
   
   Register your new application at Sentry.io to provide error logging. It will generate a url that will be needed to 
   install this app.

1. **Deploy the app to Heroku.**

   [![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
 
   This app was designed for Heroku, and shouldn't cost much to operate there. 
   You may have to put in a credit card to increase the number of free hours alloted per month, though.
   Input the tokens and URL you collected in the previous step to the Heroku configuration to properly set up the app.
   
1. **Back at Slack apps, switch on *Event Subscriptions* for your app.**

   Via *Event Subscriptions* in the left menu. After switching on, enter your new Heroku app address - eg. `https://your-domain.herokuapp.com/slack/event` - as the request URL.

   Scroll down and, under *Subscribe to Bot Events*, select the relevant events for the features you want the app to support:

   * Select `message.channels` to support all general features in _public_ channels it is invited to.
   * Select `message.groups` to support all general features in _private_ channels it is invited to.
   * Select `message.im` to support receiving commands by private message.
   
   Finally, click *Save Changes*. If you wish, you can come back to this screen later and add or change the events the app handles.

1. **Invite your new bot to any channel in your Slack team and use it.**

    */invite @yourplusplus2bot*
    
    *@jake++*
    
## Contributions

Contributions are welcome to this repository! Please read our [Code of Conduct](/CODE_OF_CONDUCT.md) before contributing, and 
consider opening an issue before writing code.

