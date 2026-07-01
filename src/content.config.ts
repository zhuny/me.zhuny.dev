import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const youtube = z.object({
	url: z.string().url(),
	title: z.string(),
	subtitle: z.string().optional(),
	thumbnail: z.string().url().optional(),
});

const blog = defineCollection({
	// Load Markdown and MDX files in the `src/content/blog/` directory.
	// README.md is a contributor guide, not a published post.
	loader: glob({
		base: './src/content/blog',
		pattern: ['**/*.{md,mdx}', '!README.md'],
	}),
	// Type-check frontmatter using a schema
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			// Transform string to Date object
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			heroImage: z.optional(image()),
			youtube: youtube.optional(),
		}),
});

export const collections = { blog };
