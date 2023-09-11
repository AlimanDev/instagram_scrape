from typing import List, Dict

from instaloader import Post, Profile, Instaloader


class InstagramParser:

    def __init__(self):
        self.loader = Instaloader()
        login = 'prog.rammer99'
        self.loader.load_session_from_file(login, f'/root/instagram_scrape/session-{login}')

    def get_profile(self, username: str):
        self.client: Profile = self._load_client(username)
        self.post_iterator = self.client.get_posts()

    def __iter__(self):
        return self

    def __next__(self) -> Dict[str, str]:
        try:
            post = next(self.post_iterator)
            if post.typename in ['GraphImage', 'GraphSidecar']:
                return self._reformat_post(post)
            else:
                return self.__next__()
        except StopIteration:
            raise StopIteration

    def get_posts_as_list(self) -> List[Dict]:

        data = []
        for post in self.post_iterator:
            if post.typename in ['GraphImage', 'GraphSidecar']:
                reformat_post = self._reformat_post(post)
                print('post', reformat_post)
                data.append(reformat_post)
        return data

    def _reformat_post(self, post: Post) -> Dict[str, str]:
        return {
            'title': post.title,
            'caption': post.caption,
            'caption_hashtags': post.caption_hashtags,
            'media_id': post.mediaid,
            'owner_id': post.owner_id,
            'date_utc': post.date_utc,
            'typename': post.typename,
            'media_count': post.mediacount,
            'images': self._get_node_images(post) if post.typename == 'GraphSidecar' else [post.url]
        }

    @staticmethod
    def _get_node_images(post) -> List[str]:
        return [i.display_url for i in post.get_sidecar_nodes()]

    def _load_client(self, username: str) -> Profile:
        client = Profile.from_username(self.loader.context, username)
        return client
