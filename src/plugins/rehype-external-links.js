const SITE_HOST = 'me.zhuny.dev';

function isExternal(href) {
	if (!href.startsWith('http://') && !href.startsWith('https://')) {
		return false;
	}

	try {
		return new URL(href).hostname !== SITE_HOST;
	} catch {
		return false;
	}
}

function visit(node, visitor) {
	visitor(node);

	if (!node.children) {
		return;
	}

	for (const child of node.children) {
		visit(child, visitor);
	}
}

/** @returns {import('unified').Plugin} */
export function rehypeExternalLinks() {
	return (tree) => {
		visit(tree, (node) => {
			if (node.type !== 'element' || node.tagName !== 'a') {
				return;
			}

			const href = node.properties?.href;
			if (!href || !isExternal(String(href))) {
				return;
			}

			const existing = node.properties.className;
			node.properties.className = [
				...(Array.isArray(existing) ? existing : existing ? [existing] : []),
				'external-link',
			];
			node.properties.target = '_blank';
			node.properties.rel = 'noopener noreferrer';
		});
	};
}
