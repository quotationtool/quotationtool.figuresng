var ulang;
if (navigator.userLanguage) // IE
    ulang = navigator.userLanguage;
else if (navigator.language) // FF 
    ulang = navigator.language;
else
    ulang = 'en';
var alang;
alang = 'en';
if (ulang.substring(0,2) == 'de')
   alang = 'de';
tinyMCE.init({
	language : alang,
        mode : "textareas",
        theme : "advanced",
        plugins : "-quotationtoolexample,preview,spellchecker",
        theme_advanced_blockformats : "p,blockquote,h1,h2,h3,h4,h5,h6",
        theme_advanced_buttons1 : "qttlExampleQuid,qttlExampleProQuo,qttlExampleMarker",
        theme_advanced_buttons2 : "charmap,|,bold,italic,underline,|,sub,sup,|,outdent,indent,|,formatselect,|,undo,redo,|,preview,code,|,spellchecker,removeformat",
        theme_advanced_buttons3 : "",      
        theme_advanced_toolbar_location : "top",
        theme_advanced_toolbar_align : "left",
        theme_advanced_statusbar_location : "bottom",
        theme_advanced_resizing : true
});
