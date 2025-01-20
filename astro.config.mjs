// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
// import remarkToc from 'remark-toc';

// https://astro.build/config
export default defineConfig({
	site: 'https://manasvi.co.in',
	integrations: [ mdx(), sitemap() ],
//   markdown: {
//     remarkPlugins: [ [remarkToc, { heading: 'toc', maxDepth: 3 } ] ],
//   },
});
