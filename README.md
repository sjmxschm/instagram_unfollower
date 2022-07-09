# Instagram Unfollow Bot

## Introduction
In general, growing a bigger fan base is a tedious work and takes time. On the one hand side,
it is important to grow slowly and organically to connect to your fans through creating great
content, but on the other hand reaching out to possible new fans is important too, so even 
more people can enjoy your great content.

I am personally not a big fan of Instagram or other social media because it makes me 
addicted too fast. But still, Instagram and other social media offer a lot of chances
to small artist like me. Therefore, I was exactly at this point - trying to grow with the 
help of Instagram - one of the most influential social networks today.

When it comes to an automated use, Instagram is extremely sensitive and strict. 
Before I programmed this, I tried the preexisting toolboxes for Instagram automation
but (1) got banned all the time and (2) was not able to tweak it in a way that it was 
working for me. 

The code in this repo is designed extremely conservative but enables automation of 
Instagram with reduced risk of getting blocked or banned. And I mean it this way - Instagram
is really sensitive, so using my code is on your own risk.

## Usage of the UnfollowBot

This repository provides the `UnfollowBot`, a class capable of finding the accounts who are
following a given <span style="color: red;"> account</span>, the accounts which are followed
by the given <span style="color: red;"> account</span>, comparing the accounts followed with
the accounts which follow and unfollow all accounts which are followed but do not follow back.

When calling the `UnfollowBot`, the following information is needed:
 - `username`: username of instagram account to log into
 - `password`: respective instagram password
 - `sleeping_factor`: sleeping factor for wait times - the higher the better
 - `bl_threshold`: accounts which are followed and do not follow back, but have more than 
    `bl_threshold` are not unfollowed
 - `nb_accs_follow_page`: number of accounts displayed when clicked on a profiles _followers_
  or _followings_. This number can change with the browser and might need to be updated

`username` and `password` can be edited and imported from `secrets.py`. `main.py` provides a
short wrap-up of how to call the bot and how to use the implemented functions and their order. 
