var iframe = document.getElementById('workstation-iframe');
var rootPath = STUDIO_ROOT_PATH || '/';
var currentUrl = window.location.protocol + '//' + window.location.host + rootPath + 'workstation';
iframe.src = currentUrl;