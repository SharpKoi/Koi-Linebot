import os
import argparse

parser = argparse.ArgumentParser(description='Arguments for running line bot app')
parser.add_argument('--token', type=str,
                    help='The channel access token of your line bot.')
parser.add_argument('--secret', type=str,
                    help='The channel secret of your line bot.')
parser.add_argument('--db', type=str,
                    help='The database url which your line bot app uses.')


def parse_args():
    args = parser.parse_args()
    channel_access_token = args.token if args.token else 'deadbeef'
    channel_secret = args.secret if args.secret else 'deadbeef'
    database_url = args.db if args.db else 'deadbeef'

    # set default environment variables if not exists
    os.environ.setdefault('CHANNEL_ACCESS_TOKEN', channel_access_token)
    os.environ.setdefault('CHANNEL_SECRET', channel_secret)
    os.environ.setdefault('DATABASE_URL', database_url)

    return channel_access_token, channel_secret, database_url
