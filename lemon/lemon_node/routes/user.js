
/*
 * GET users listing.
 */

exports.list = function(req, res){
  console.log(req.xhr);
  res.render('user', {group_name: 'love users'});
};