---
title: $\LaTeX$.css - A Hugo theme
date: 2022-10-31T12:50:44+08:00
tags: ['theme', 'hugo', 'latex.css']
categories: theme
author: Local Ghost
abstract: $\LaTeX$.css is a Hugo theme based on Vincent Dörig's $\LaTeX$.css and $\KaTeX$.
toc: true
---

## Features
*	$\LaTeX$ layout, dark mode support
*	`theorem`, `proof`, `table` and `figure` environments support
*	JavaScript-free
*	VS Code syntax highlighting

## Installation

1. Install [Hugo](https://gohugo.io/getting-started/installing/).
2. Create a new site:
```shell
hugo new site mysite
cd mysite
```
3. Add the theme as a submodule:
```shell
git init
git submodule add --depth=1 https://github.com/GTM52/LaTeX-css.git themes/LaTeX-css
```
4.	Start the server:
```shell
hugo server
# go to http://localhost:1313
```

## Configuration

### Site configuration

1.	copy `exampleSite/config.toml` to `config.toml` and edit it.

```toml
baseURL = 'http://www.GTM52.github.io/LaTeX-css/'
languageCode = 'en-us'
title = '$\LaTeX$.css'

[params]
	toc = true
	katex = true
	skin = 'auto'
	headerNav = [
		{ name = 'Tags', url = 'tags/' },
		{ name = 'Categories', url = 'categories/' },
		{ name = 'About', url = 'about/' },
	]
```

*	`baseURL` is the URL of your site. It will be used to generate absolute URLs for RSS feed, sitemap, etc.
*	`languageCode` is the language of your site. It will be used to generate the `lang` attribute of the `<html>` tag.
*	`title` is the title of your site. It will be used as the title of the home page.
*	`params.toc` is a boolean value. If it is `true`, the table of contents will be displayed on the right side of the page.
*	`params.katex` is a boolean value. If it is `true`, $\KaTeX$ will be used to render $\LaTeX$ expressions. If it is `false`, $\LaTeX$ expressions will be rendered as normal text.
*	`params.skin` is a string value. It can be `dark`, `light` or `auto`. It will be used to set the color scheme of the site. Any other value will be treated as `auto`. `auto` means that the color scheme will be set according to the user's system preference.
*	`params.headerNav` is an array of objects. Each object has two keys: `name` and `url`. `name` is the name of the navigation item. `url` is the URL of the navigation item. The navigation items will be displayed in the order of the array.

> You can specify the `toc` and `katex` parameters in the front matter of each post. If you do so, the parameters in the site configuration will be ignored.

## Usage

### Creating a new post

```shell
hugo new posts/my-first-post.md
```

### Setting post metadata

```yaml
---
title: My First Post
date: 2022-10-31T12:50:44+08:00
tags: ['tag1', 'tag2']
categories: 'category1'
author: Local Ghost
abstract: This is my first post.
toc: false
---
```

*	`title` is the title of the post. It will be used as the title of the post page.
*	`date` is the date of the post. It will be used to sort the posts.
*	`tags` is an array of strings. It will be used to generate the tags of the post. The tags will be displayed at the top of the post page as `keywords`.
*	`categories` is a string. It will be used to generate the category of the post.
*	`author` is a string. It will be shown below the title with the `date`.
*	`abstract` is a string. It will override the summary (displayed in the list of posts) of the post.

### Math formulas and environments

```latex
{{</* theorem lemma theorem */>}} Let $F$ be a functor from a locally small category $\mathcal C$ to $\mathbf{Set}$. 
Then for each object $A$ of $\mathcal C$, the natural transformation
	$\operatorname{Nat}(h_A, F) \equiv \operatorname{Hom}(\operatorname{Hom}(A, \cdot), F)$
from $h_A$ to $F$ are in one-to-one correspondence with the elements of $F(A)$. That is,
\[
	\operatorname{Nat}(h_A, F) \cong F(A).
\]
Moreover, the isomorphism is natural in $A$ and $F$ 
when both sides are regarded as functors from $\mathcal C \times \mathbf{Set}^{\mathcal C}$ to $\mathbf{Set}$.
```

{{< theorem lemma theorem >}} Let $F$ be a functor from a locally small category $\mathcal C$ to $\mathbf{Set}$. 
Then for each object $A$ of $\mathcal C$, the natural transformation $\operatorname{Nat}(h_A, F) \equiv \operatorname{Hom}(\operatorname{Hom}(A, \cdot), F)$ from $h_A$ to $F$ are in one-to-one correspondence with the elements of $F(A)$. That is,
\\[
	\operatorname{Nat}(h_A, F) \cong F(A).
\\]
Moreover, the isomorphism is natural in $A$ and $F$ when both sides are regarded as functors from $\mathcal C \times \mathbf{Set}^{\mathcal C}$ to $\mathbf{Set}$.

{{< proof >}}
See [wiki](https://en.wikipedia.org/wiki/Yoneda_lemma#Proof).
{{< qed >}}

### Sidenotes

```md
This is a text.{{</* sidenote "This is a sidenote." /*/>}}
sidenote "This is a sidenote."
```
This is a text.{{< sidenote "This is a sidenote." />}} 

### Text Formatting

```md
This sentence is **bold**. If you like semantics, you might go with {{</* text strong strong */>}}  or {{</* text em emphasized */>}} text. 
If not, *italic* is still around. 

{{</* text small small */>}} text is for fine print. 
Your copy can also be {{</* text sub subscripted */>}} and {{</* text sup superscripted */>}}, {{</* text ins inserted */>}}, {{</* text del deleted */>}}, or {{</* text mark highlighted */>}}. 
You would use a [hyperlink](#!) to go to a new page. 
Keyboard input elements like {{</* text kbd Cmd */>}} + {{</* text kbd Shift */>}} are used to display textual user input.
```

This sentence is **bold**. If you like semantics, you might go with {{< text strong strong >}}  or {{< text em emphasized >}} text. If not, *italic* is still around. 
{{< text small small >}} text is for fine print. Your copy can also be {{< text sub subscripted >}} and {{< text sup superscripted >}}, {{< text ins inserted >}}, {{< text del deleted >}}, or {{< text mark highlighted >}}. You would use a [hyperlink](#!) to go to a new page. Keyboard input elements like {{< text kbd Cmd >}} + {{< text kbd Shift >}} are used to display textual user input.

### Table

```md
{{</* table caption="A sample table with a descriptive caption." */>}}
| Header 1      | Header 2      | Header 3      |
| ------------- | ------------- | ------------- |
| Description 1 | Description 2 | Description 3 |
| Description 1 | Description 2 | Description 3 |
| Description 1 | Description 2 | Description 3 |
| **Footer 1**  | **Footer 2**  | **Footer 3**  |
{{</* /table */>}}
```

{{< table caption="A sample table with a descriptive caption." >}}
| Header 1      | Header 2      | Header 3      |
| ------------- | ------------- | ------------- |
| Description 1 | Description 2 | Description 3 |
| Description 1 | Description 2 | Description 3 |
| Description 1 | Description 2 | Description 3 |
| **Footer 1**  | **Footer 2**  | **Footer 3**  |
{{< /table >}}

### Figure

```md
{{</* figure src=https://picsum.photos/800/600 
caption="A sample figure with a descriptive caption by [Lorem Picsum](https://picsum.photos/)" width=800 height=600 */>}}
```

{{< figure src=https://picsum.photos/800/600 
caption="A sample figure with a descriptive caption by [Lorem Picsum](https://picsum.photos/)" width=800 height=600 >}}

## Miscellaneous
### Scroll Overflow

\\[
(1 + x)^n = 1 + nx + \frac{n(n-1)}{2}x^2 + \frac{n(n-1)(n-2)}{6}x^3 + \frac{n(n-1)(n-2)(n-3)}{24}x^4 + \cdots + \frac{n(n-1)(n-2)\cdots(n-r+1)}{r!}x^r + \cdots
\\]

### Syntax Highlighting

<!-- todo -->