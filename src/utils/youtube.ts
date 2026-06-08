export function getYoutubeVideoId(url: string): string | null {
	try {
		const parsed = new URL(url);
		if (parsed.hostname === 'youtu.be') {
			return parsed.pathname.slice(1).split('/')[0] || null;
		}
		if (parsed.hostname.includes('youtube.com')) {
			return parsed.searchParams.get('v');
		}
	} catch {
		return null;
	}
	return null;
}

export function getYoutubeThumbnail(url: string): string | null {
	const id = getYoutubeVideoId(url);
	return id ? `https://img.youtube.com/vi/${id}/mqdefault.jpg` : null;
}
