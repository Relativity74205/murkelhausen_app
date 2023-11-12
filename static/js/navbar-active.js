$(document).ready(function () {
    const url = window.location;
    $('div.navbar-nav a[href="'+ url +'"]').addClass('active').attr('aria-current', 'page');
    $('div.navbar-nav a').filter(function() {
         return this.href == url;
    }).addClass('active').attr('aria-current', 'page');
});