
/*
 * GET home page.
 */

var mongoose = require('mongoose')
mongoose.connect('mongodb://test-note.kontur/mydb')
var db	= mongoose.connection

var user 	= mongoose.model('user', {
  name: String

});

var tester	= mongoose.model('testers', { name: String, num: String});

exports.index = function(req, res){
  //res.render('index', { title: 'Express' });
  tester.find(function(err, t){
	console.log(t);
	res.send(t);
  });
  
};

