/**
 * 		/models/data/index.js
 * 
 * 		Loader for Data models
 */
module.exports	= function(){
	var prefix	= 'data';
	require('./data')(prefix);
	require('./trigger')(prefix);
	require('./contractor')(prefix);
}();
