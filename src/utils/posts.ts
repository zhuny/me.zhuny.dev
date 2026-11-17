import { getCollection, type CollectionEntry } from 'astro:content';

export async function getPublishedPosts(): Promise<CollectionEntry<'blog'>[]> {
	const posts = await getCollection('blog');
	return posts.filter((post) => post.data.draft !== true);
}
