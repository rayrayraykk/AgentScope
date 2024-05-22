// 获取iframe元素
var iframe = document.getElementById('workstation-iframe');
// 构建完整的URL
var currentUrl = window.location.protocol + '//' + window.location.host + '/workstation';
// 设置iframe的`src`属性
iframe.src = currentUrl;
console.log(iframe.src)