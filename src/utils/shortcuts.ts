import { shortcuts } from '../data/shortcuts';

const slugToHex = Object.fromEntries(
	Object.entries(shortcuts).map(([hex, slug]) => [slug, hex]),
);

export function getSlugByHex(hex: string): string | undefined {
	return shortcuts[hex.toLowerCase()];
}

export function getHexBySlug(slug: string): string | undefined {
	return slugToHex[slug];
}

export function getShortcutUrl(slug: string, site = 'https://me.zhuny.dev'): string | null {
	const hex = getHexBySlug(slug);
	if (!hex) return null;
	return new URL(`/z/${hex}`, site).href;
}
