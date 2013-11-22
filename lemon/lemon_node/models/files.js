/*
*	Models for creating binary file collections
*
*/




var mongoose	= require('mongoose');
var models		= {};

var collectionFiles	= 'files'

var filesSchema	= {
	'chunk': String,
	'meta':	Number,
	'filename': String,
	'length': Number,
	'size': Number,
	'id': String
}

exports.init	= function(){
	models.files	= mongoose.model(collectionFiles, filesSchema, collectionFiles)
}

exports.getModels	= function(){
	return models
}