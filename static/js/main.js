(function () {
	let preloader = document.querySelector('#preloader')
	if (preloader) window.addEventListener('load', e => preloader.remove())
})()
