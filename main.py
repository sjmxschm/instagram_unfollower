from Unfollower import UnfollowBot

from secrets import pw, acc


def main():
    username = acc  # import from secrets file
    password = pw   # import from secrets file

    unfollow_bot = UnfollowBot(username, password)
    unfollow_bot.get_followings()
    unfollow_bot.get_followers()
    unfollow_bot.compare_follower_and_followings()
    unfollow_bot.unfollow_targets()


if __name__ == "__main__":
    main()
