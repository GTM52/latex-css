const fs = require('fs');
const JSDOM = require('jsdom').JSDOM;
const shiki = require('shiki');
const autoRender = require('katex/dist/contrib/auto-render.js');

function setGlobal(name, value) {
	(function (globals) {
		globals[name] = value;
	})((1, eval)('this'));
}

const args = process.argv.slice(2);

args.forEach(async (path) => {
	let buffer = fs.readFileSync(path);
	let dom = new JSDOM(buffer.toString());
	await highlight();
	await renderMath();
	await removePrerenderScript();
	console.log('overwriting', path);
	fs.writeFileSync(path, dom.serialize());
	async function highlight() {
		console.log('highlighting code...');
		let lightColorSet = new Set();
		let darkColorSet = new Set();
		let codeBlocks = dom.window.document.querySelectorAll('pre');
		let highlighter = await shiki.getHighlighter({
			themes: ['light-plus', 'dark-plus'],
		});
		codeBlocks.forEach((codeBlock) => {
			let lang = codeBlock.firstChild.getAttribute('data-lang');
			let lightHighlighted = highlighter.codeToHtml(
				codeBlock.firstChild.textContent,
				{ lang: lang, theme: 'light-plus' }
			);
			let darkHighlighted = highlighter.codeToHtml(
				codeBlock.firstChild.textContent,
				{ lang: lang, theme: 'dark-plus' }
			);
			let lightColors = lightHighlighted.match(
				/(?<=color: )#([0-9a-fA-F]{6})/g
			);
			let darkColors = darkHighlighted.match(
				/(?<=color: )#([0-9a-fA-F]{6})/g
			);
			lightColors.shift();
			darkColors.shift();
			let highlighted = lightHighlighted
				.replace(/style="background-color: #[0-9a-fA-F]{6}"/g, '')
				.replace(/<code>/, `<code data-lang="${lang}">`);
			while (lightColors.length) {
				let currentLightColor = lightColors.shift();
				let currentDarkColor = darkColors.shift();
				lightColorSet.add(currentLightColor);
				darkColorSet.add(currentDarkColor);
				highlighted = highlighted.replace(
					/style="color: #[0-9a-fA-F]{6}/,
					`data-light-color="${currentLightColor}" data-dark-color="${currentDarkColor}" style="`
				);
			}
			highlighted = highlighted
				.replace(/style=""/g, '')
				.replace(/style="; /g, 'style="');
			codeBlock.outerHTML = highlighted;
		});
		let style = '\n';
		lightColorSet.forEach((color) => {
			style += `[data-light-color="${color}"] { color: ${color}; }\n`;
		});
		darkColorSet.forEach((color) => {
			style += `.latex-dark [data-dark-color="${color}"] { color: ${color}; }\n`;
		});
		style += `@media (prefers-color-scheme: dark) { \n`;
		darkColorSet.forEach((color) => {
			style += `.latex-dark-auto [data-dark-color="${color}"] { color: ${color}; }\n`;
		});
		style += `}\n`;
		let styleElement = dom.window.document.createElement('style');
		styleElement.innerHTML = style;
		dom.window.document.head.appendChild(styleElement);
		console.log('done');
	}
	async function renderMath() {
		const options = {
			// customised options
			// • auto-render specific keys, e.g.:
			delimiters: [
				{ left: '$$', right: '$$', display: true },
				{ left: '$', right: '$', display: false },
				{ left: '\\(', right: '\\)', display: false },
				{ left: '\\[', right: '\\]', display: true },
			],
			// • rendering keys, e.g.:
			throwOnError: false,
		};
		console.log('rendering math...');
		setGlobal('document', dom.window.document);
		autoRender(dom.window.document.body, options);
		console.log('Done!');
	}
	async function removePrerenderScript() {
		console.log('removing prerender script...');
		let prerenderScripts =
			dom.window.document.querySelectorAll('script.prerender');
		for (let script of prerenderScripts) {
			script.remove();
		}
		console.log('Done!');
	}
});
