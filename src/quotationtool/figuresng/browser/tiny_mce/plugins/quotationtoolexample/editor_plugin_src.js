/**
 * editor_plugin_src.js
 *
 * Copyright 2011, Christian Lück
 * Released under LGPL License.
 *
 * License: http://quotationtool.org/license
 */

(function() {
	// Load plugin specific language pack
	tinymce.PluginManager.requireLangPack('quotationtoolexample');

	tinymce.create('tinymce.plugins.QuotationtoolExamplePlugin', {
		// Initializes the plugin
		init : function(ed, url) {
			// Register commands so that they can be
			// invoked by using
			// tinyMCE.activeEditor.execCommand('qttlExampleQuid');
			ed.addCommand('qttlExampleQuid', function() {
				ed.formatter.toggle('qttlExampleQuid');
				});
			ed.addCommand('qttlExampleProQuo', function() {
				ed.formatter.toggle('qttlExampleProQuo');
				});
			ed.addCommand('qttlExampleMarker', function() {
				ed.formatter.toggle('qttlExampleMarker');
				});

			// Register buttons
			ed.addButton('qttlExampleQuid', {
				title : 'quotationtoolexample.quid',
				cmd : 'qttlExampleQuid',
				image : url + '/img/quid.gif'
				//label : 'quotationtoolexample.quid'
			});
			ed.addButton('qttlExampleProQuo', {
				title : 'quotationtoolexample.proquo',
				cmd : 'qttlExampleProQuo',
				image : url + '/img/proquo.gif'
				//label : 'quotationtoolexample.proquo'
				
			});
			ed.addButton('qttlExampleMarker', {
				title : 'quotationtoolexample.marker',
				cmd : 'qttlExampleMarker',
				image : url + '/img/marker.gif'
				//label : 'quotationtoolexample.marker'
			});

			// Add a node change handler, selects the
			// button in the UI when a image is selected
			ed.onNodeChange.add(function(ed, cm, n) {
				cm.setActive('qttlExampleQuid', ed.dom.hasClass(n, 'quotationtool-example-quid'));
			});
			ed.onNodeChange.add(function(ed, cm, n) {
				cm.setActive('qttlExampleProQuo', ed.dom.hasClass(n, 'quotationtool-example-proquo'));
			});
			ed.onNodeChange.add(function(ed, cm, n) {
				cm.setActive('qttlExampleMarker', ed.dom.hasClass(n, 'quotationtool-example-marker'));
			});

			// Register formats and load css when editor was initialized
			ed.onInit.add(function(ed) {
				ed.formatter.register({
					qttlExampleQuid : {
						inline : 'span', 
						classes : 'quotationtool-example-quid'
						},
					qttlExampleProQuo : {
						inline : 'span', 
						classes : 'quotationtool-example-proquo'
						},
					qttlExampleMarker : {
						inline : 'span', 
						classes : 'quotationtool-example-marker'
						}
					});
				ed.dom.loadCSS( url + '/css/example.css');
				//ed.windowManager.alert('editor is done: ' + url);
				});

		},

		createControl : function(n, cm) {
			return null;
		},

		getInfo : function() {
			return {
				longname : 'Quotationtool Example plugin',
				author : 'Christian Lück',
				authorurl : 'http://quotationtool.org',
				infourl : 'http://quotationtool.org/figuresng',
				version : "0.1"
			};
		}
	});

	// Register plugin
	tinymce.PluginManager.add('quotationtoolexample', tinymce.plugins.QuotationtoolExamplePlugin);
})();